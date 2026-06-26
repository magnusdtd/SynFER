import io
import json
import os
import random
import time
import uuid
import base64

import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from PIL import Image

from src.evaluate_synfer import ddim_inversion

from ..config import settings
from ..utils import determine_expression_category, make_au_vector, simulate_landmarks

router = APIRouter()


@router.post("/generate")
async def generate_expression(
    request: Request,
    prompt: str = Form(""),
    selectedFAUs: str = Form("[]"),
    uploadedFile: UploadFile = File(None),
):
    start_time = time.time()

    # 1. Parse manual FACS toggled selections
    try:
        selected_aus = json.loads(selectedFAUs)
        if not isinstance(selected_aus, list):
            selected_aus = []
    except Exception:
        selected_aus = []

    # 2. Get target expression configuration
    expr = determine_expression_category(prompt, selected_aus)

    # Preprocessing transforms matching SD & POSTER++ input requirements
    sd_transform = transforms.Compose(
        [
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ]
    )

    class_mapping = {
        "neutral": 0,
        "happy": 1,
        "sad": 2,
        "surprise": 3,
        "fear": 4,
        "disgust": 5,
        "Anger": 6,
        "Contempt": 7,
    }
    target_idx = class_mapping.get(expr, 0)

    # 3. Retrieve ML pipeline elements from app state
    pipe = request.app.state.pipe
    au_proj_model = request.app.state.au_proj_model
    og_model = request.app.state.og_model
    fer_model = request.app.state.fer_model
    og_transform = request.app.state.og_transform
    device = settings.device
    weight_dtype = torch.float16 if device == "cuda" else torch.bfloat16

    # 4. Read identity reference configuration
    try:
        if uploadedFile is not None:
            content = await uploadedFile.read()
            image_data = Image.open(io.BytesIO(content)).convert("RGB")
        else:
            raise HTTPException(status_code=400, detail="No reference image provided.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode uploaded image: {str(e)}")

    # Preprocess images for Diffusion VAE and OpenGraphAU network
    img_sd = sd_transform(image_data).unsqueeze(0).to(device, dtype=weight_dtype)
    img_og = og_transform(image_data).unsqueeze(0).to(device)

    # 5. Predict Action Units from reference and merge with manual select overrides
    with torch.no_grad():
        if uploadedFile is not None:
            predicted_au = og_model(img_og)
            predicted_au = (predicted_au >= 0.5).float().to(dtype=weight_dtype)
        else:
            # Baseline starts empty if no image provided
            predicted_au = torch.zeros((1, 41), device=device, dtype=weight_dtype)

        # Build custom overrides
        fau_vector_override = make_au_vector(selected_aus)
        fau_tensor_override = torch.tensor([fau_vector_override], device=device, dtype=weight_dtype)

        # Merge vectors using element-wise maximum (logical OR)
        au_vector = torch.max(predicted_au, fau_tensor_override)

    # 6. Encode prompts
    prompt_templates = {
        "neutral": "a photo of a face with a neutral expression",
        "happy": "a photo of a face with a happy expression",
        "sad": "a photo of a face with a sad expression",
        "surprise": "a photo of a face with a surprised expression",
        "fear": "a photo of a face with a fearful expression",
        "disgust": "a photo of a face with a disgusted expression",
        "Anger": "a photo of a face with an angry expression",
        "Contempt": "a photo of a face with a contempt expression",
    }
    target_prompt = prompt.strip() if prompt.strip() else prompt_templates.get(expr, "a photo of a face")

    prompt_embeds, neg_prompt_embeds = pipe.encode_prompt(
        prompt=[target_prompt],
        device=device,
        num_images_per_prompt=1,
        do_classifier_free_guidance=True,
        negative_prompt=["low quality, distortion, blur"],
    )

    # Neutral caption for DDIM inversion
    inv_prompt = "a photo of a face"
    inv_prompt_embeds, _ = pipe.encode_prompt(
        prompt=[inv_prompt],
        device=device,
        num_images_per_prompt=1,
        do_classifier_free_guidance=False,
    )

    # 7. Execute DDIM Inversion to map identity face to noise space
    with torch.no_grad():
        latent = pipe.vae.encode(img_sd).latent_dist.sample() * pipe.vae.config.scaling_factor

        z = ddim_inversion(
            pipe=pipe,
            unet=pipe.unet,
            au_proj_model=au_proj_model,
            latent=latent,
            text_embeddings=inv_prompt_embeds,
            num_steps=settings.num_inference_steps,
            invert_steps=settings.invert_steps,
        )

    # 8. Run Controlled Synthesis Denoising Loop with Semantic Guidance
    pipe.scheduler.set_timesteps(settings.num_inference_steps, device=device)
    timesteps_to_denoise = pipe.scheduler.timesteps[len(pipe.scheduler.timesteps) - settings.invert_steps :]

    text_embeddings = prompt_embeds.clone().detach()
    target_au_token = au_proj_model(au_vector)
    uncond_au_token = au_proj_model(torch.zeros_like(au_vector))
    target_label_tensor = torch.tensor([target_idx], device=device)

    for i, t in enumerate(timesteps_to_denoise):
        apply_sg = i >= settings.sg_start_step

        if apply_sg:
            # Enable gradient tracking on text embedding
            text_embeddings_grad = text_embeddings.clone().detach().requires_grad_(True)
            cond_pos = torch.cat([text_embeddings_grad, target_au_token], dim=1)

            # Predict noise
            noise_pred_cond = pipe.unet(z, t, cond_pos).sample

            # Estimate clean latent z0
            alpha_prod_t = pipe.scheduler.alphas_cumprod[t]
            beta_prod_t = 1.0 - alpha_prod_t
            hat_z0 = (z - beta_prod_t**0.5 * noise_pred_cond) / (alpha_prod_t**0.5)

            # Differentiable VAE decoding
            clean_image = pipe.vae.decode(hat_z0.to(dtype=weight_dtype) / pipe.vae.config.scaling_factor).sample

            # Rescale and normalize for POSTER++ input
            clean_image = (clean_image + 1.0) / 2.0
            clean_image_resized = F.interpolate(clean_image, size=(224, 224), mode="bilinear", align_corners=False)
            clean_image_resized = clean_image_resized.to(dtype=torch.float32)

            mean = torch.tensor([0.485, 0.456, 0.406], device=device).view(1, 3, 1, 1)
            std = torch.tensor([0.229, 0.224, 0.225], device=device).view(1, 3, 1, 1)
            clean_image_norm = (clean_image_resized - mean) / std

            # Backpropagate classifier loss to adjust conditional text embeddings
            logits = fer_model(clean_image_norm)
            loss = F.cross_entropy(logits, target_label_tensor)

            grads = torch.autograd.grad(loss, text_embeddings_grad)[0]
            grads_norm = grads / (torch.norm(grads, p=2, dim=-1, keepdim=True) + 1e-8)
            text_embeddings = text_embeddings - settings.sg_step_size * grads_norm

        # Standard Classifier-Free Guidance step
        with torch.no_grad():
            text_embeddings_all = torch.cat([neg_prompt_embeds, text_embeddings], dim=0)
            au_token_all = torch.cat([uncond_au_token, target_au_token], dim=0)
            cond_all = torch.cat([text_embeddings_all, au_token_all], dim=1)

            latent_model_input = torch.cat([z] * 2)
            latent_model_input = pipe.scheduler.scale_model_input(latent_model_input, t)

            noise_pred = pipe.unet(latent_model_input, t, cond_all).sample

            noise_pred_uncond, noise_pred_cond = noise_pred.chunk(2)
            noise_pred_cfg = noise_pred_uncond + settings.guidance_scale * (noise_pred_cond - noise_pred_uncond)

            z = pipe.scheduler.step(noise_pred_cfg, t, z).prev_sample

    # 9. Decode final latent and run real post-inference classifier evaluation
    with torch.no_grad():
        generated_img_tensor = pipe.vae.decode(z / pipe.vae.config.scaling_factor).sample

        # Predict real classification metrics on the final generated image
        clean_image_resized = F.interpolate(generated_img_tensor, size=(224, 224), mode="bilinear", align_corners=False)
        clean_image_resized = clean_image_resized.to(dtype=torch.float32)
        mean = torch.tensor([0.485, 0.456, 0.406], device=device).view(1, 3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225], device=device).view(1, 3, 1, 1)
        clean_image_norm = (clean_image_resized - mean) / std

        logits = fer_model(clean_image_norm)
        probs = F.softmax(logits, dim=1)
        confidence = probs.max(dim=1).values.item()
        pred_idx = probs.argmax(dim=1).item()

        inverse_class_mapping = {
            0: "neutral",
            1: "happy",
            2: "sad",
            3: "surprise",
            4: "fear",
            5: "disgust",
            6: "angry",
            7: "contempt",
        }
        detected_expr = inverse_class_mapping.get(pred_idx, "neutral")

        # Convert back to PIL Image
        generated_img = (generated_img_tensor / 2 + 0.5).clamp(0, 1)
        generated_img = generated_img.cpu().permute(0, 2, 3, 1).numpy()
        generated_img = (generated_img * 255).round().astype("uint8")
        out_img = Image.fromarray(generated_img[0])

    # 10. Persist synthesized artwork on host static directory
    os.makedirs(settings.static_dir, exist_ok=True)
    filename = f"synthesis_{uuid.uuid4().hex}.png"
    filepath = os.path.join(settings.static_dir, filename)
    out_img.save(filepath)

    # encode image to base64
    buffered = io.BytesIO()
    out_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # 11. Format final JSON response payload
    duration_ms = int((time.time() - start_time) * 1000)
    base_url = str(request.base_url)
    image_url = f"{base_url}static/{filename}"
    landmarks = simulate_landmarks(detected_expr, selected_aus)

    return {
        "success": True,
        "image_url": image_url,
        "image_b64": img_str,
        "metadata": {
            "expressionDetected": detected_expr,
            "confidence": f"{confidence:.3f}",
            "fauCountsApplied": len(selected_aus),
            "renderingTimeMs": duration_ms,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "landmarks": landmarks,
        },
    }
