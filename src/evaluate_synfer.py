import argparse
import fcntl
import glob
import json
import os
import random

import numpy as np
import torch
import torch.nn.functional as F
from accelerate import Accelerator
from cleanfid import fid
from diffusers import DDIMScheduler, StableDiffusionPipeline
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from tqdm import tqdm

from OpenGraphAU.model.MEFL import MEFARG
from OpenGraphAU.utils import image_eval
from OpenGraphAU.utils import load_state_dict as og_load_state_dict
from POSTER_V2.models.PosterV2 import pyramid_trans_expr2

from .au_adapter import AUProjModel
from .ip_adapter.attention_processor import AttnProcessor2_0 as AttnProcessor
from .ip_adapter.attention_processor import IPAttnProcessor2_0 as IPAttnProcessor
from .utils import set_seed


# Dummy classes for torch.load unpickler to succeed when loading POSTER++ checkpoints
class RecorderMeter:
    def __init__(self, *args, **kwargs):
        pass


class RecorderMeter1:
    def __init__(self, *args, **kwargs):
        pass


class AffectNetEvalDataset(Dataset):
    def __init__(self, source_files, sd_transform, og_transform, class_mapping):
        self.source_files = source_files
        self.sd_transform = sd_transform
        self.og_transform = og_transform
        self.class_mapping = class_mapping

    def __len__(self):
        return len(self.source_files)

    def __getitem__(self, idx):
        img_path, category = self.source_files[idx]
        img = Image.open(img_path).convert("RGB")

        img_sd = self.sd_transform(img)
        img_og = self.og_transform(img)
        category_idx = self.class_mapping[category]

        return {
            "img_sd": img_sd,
            "img_og": img_og,
            "img_path": img_path,
            "category": category,
            "category_idx": category_idx,
        }


def parse_args():
    parser = argparse.ArgumentParser(description="Evaluate SynFER model with DDIM inversion and Semantic Guidance.")
    parser.add_argument(
        "--au_adapter_dir",
        type=str,
        default="outputs/sd-fetext-model-au-adapter",
        help="Path to the trained AU-Adapter weights directory.",
    )
    parser.add_argument(
        "--base_model_dir",
        type=str,
        default="outputs/sd-fetext-model-lora",
        help="Path to the base model with LoRA weights merged.",
    )
    parser.add_argument(
        "--ref_dataset_dir",
        type=str,
        default="datasets/AffectNet/Test",
        help="Reference test dataset directory.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="outputs/synthetic_affectnet_test",
        help="Directory to save generated synthetic images.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the total number of images to generate (for debugging/testing).",
    )
    parser.add_argument(
        "--guidance_scale",
        type=float,
        default=7.5,
        help="Classifier-free guidance scale.",
    )
    parser.add_argument(
        "--num_inference_steps",
        type=int,
        default=50,
        help="Number of denoising inference steps.",
    )
    parser.add_argument(
        "--invert_steps",
        type=int,
        default=35,
        help="Number of DDIM inversion steps.",
    )
    parser.add_argument(
        "--sg_start_step",
        type=int,
        default=15,
        help="Backward step index at which to start applying Semantic Guidance.",
    )
    parser.add_argument(
        "--sg_step_size",
        type=float,
        default=0.1,
        help="Step size for Semantic Guidance gradient updates.",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=8,
        help="Batch size for parallel inference.",
    )
    parser.add_argument(
        "--num_workers",
        type=int,
        default=10,
        help="Number of data loader worker processes.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=3407,
        help="Random seed for generation.",
    )
    return parser.parse_args()


def load_au_adapter(unet, au_adapter_dir, device, weight_dtype):
    au_dim = 41
    # 1. Initialize AUProjModel
    au_proj_model = AUProjModel(
        au_dim=au_dim,
        cross_attention_dim=unet.config.cross_attention_dim,
    ).to(device, dtype=weight_dtype)

    # 2. Set attn processors in UNet
    attn_procs = {}
    unet_sd = unet.state_dict()
    for name in unet.attn_processors.keys():
        cross_attention_dim = None if name.endswith("attn1.processor") else unet.config.cross_attention_dim
        if name.startswith("mid_block"):
            hidden_size = unet.config.block_out_channels[-1]
        elif name.startswith("up_blocks"):
            block_id = int(name[len("up_blocks.")])
            hidden_size = list(reversed(unet.config.block_out_channels))[block_id]
        elif name.startswith("down_blocks"):
            block_id = int(name[len("down_blocks.")])
            hidden_size = unet.config.block_out_channels[block_id]

        if cross_attention_dim is None:
            attn_procs[name] = AttnProcessor()
        else:
            layer_name = name.split(".processor")[0]
            weights = {
                "to_k_ip.weight": unet_sd[layer_name + ".to_k.weight"],
                "to_v_ip.weight": unet_sd[layer_name + ".to_v.weight"],
            }
            attn_procs[name] = IPAttnProcessor(
                hidden_size=hidden_size,
                cross_attention_dim=cross_attention_dim,
                num_tokens=1,
            )
            attn_procs[name].load_state_dict(weights)
    unet.set_attn_processor(attn_procs)
    adapter_modules = torch.nn.ModuleList(unet.attn_processors.values()).to(device, dtype=weight_dtype)

    # 3. Load checkpoint
    ckpt_path = os.path.join(au_adapter_dir, "model.safetensors")
    if not os.path.exists(ckpt_path):
        ckpt_path = os.path.join(au_adapter_dir, "ip_adapter.bin")

    print(f"Loading AU-Adapter weights from {ckpt_path}...")
    state_dict = torch.load(ckpt_path, map_location="cpu", weights_only=False)
    au_proj_model.load_state_dict(state_dict["image_proj"], strict=True)
    adapter_modules.load_state_dict(state_dict["ip_adapter"], strict=True)

    return au_proj_model


def load_opengraphau_model(device):
    print("Loading OpenGraphAU model...")
    net = MEFARG(
        num_main_classes=27,
        num_sub_classes=14,
        backbone="resnet50",
    )
    checkpoint_path = "models/OpenGraphAU/OpenGprahAU-ResNet50_second_stage.pth"
    net = og_load_state_dict(net, checkpoint_path)
    net = net.to(device)
    net.eval()
    return net


def load_poster_v2(device):
    print("Loading POSTER++ model...")
    model = pyramid_trans_expr2(img_size=224, num_classes=8)
    checkpoint_path = "models/POSTER_V2/affectnet-8-model_best.pth"
    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    state_dict = checkpoint["state_dict"] if "state_dict" in checkpoint else checkpoint

    new_state_dict = {}
    for k, v in state_dict.items():
        if k.startswith("module."):
            new_state_dict[k[7:]] = v
        else:
            new_state_dict[k] = v

    model.load_state_dict(new_state_dict)
    model = model.to(device)
    model.eval()
    return model


def ddim_inversion(pipe, unet, au_proj_model, latent, text_embeddings, num_steps=50, invert_steps=35):
    # Set the DDIM scheduler timesteps
    pipe.scheduler.set_timesteps(num_steps)
    full_timesteps = list(reversed(pipe.scheduler.timesteps))  # from 0 to 999

    # The denoising loop starts at: pipe.scheduler.timesteps[len(pipe.scheduler.timesteps) - invert_steps]
    start_denoise_t = pipe.scheduler.timesteps[len(pipe.scheduler.timesteps) - invert_steps]

    z = latent.clone()
    batch_size = z.shape[0]
    for i, t in enumerate(full_timesteps):
        if t >= start_denoise_t:
            break

        # Construct neutral prompt + zero AU condition for the entire batch
        zero_au = torch.zeros((batch_size, 41), device=z.device, dtype=z.dtype)
        au_token = au_proj_model(zero_au)
        cond = torch.cat([text_embeddings, au_token], dim=1)

        # Predict the noise using UNet
        noise_pred = unet(z, t, cond).sample

        # DDIM forward step calculation
        alpha_prod_t = pipe.scheduler.alphas_cumprod[t]
        t_next = full_timesteps[i + 1]
        alpha_prod_t_next = pipe.scheduler.alphas_cumprod[t_next]

        # DDIM inversion formula
        z0_estimate = (z - (1.0 - alpha_prod_t) ** 0.5 * noise_pred) / (alpha_prod_t**0.5)
        z = (alpha_prod_t_next**0.5) * z0_estimate + (1.0 - alpha_prod_t_next) ** 0.5 * noise_pred

    return z


def load_tracker(tracker_path):
    if not os.path.exists(tracker_path):
        return set()
    with open(tracker_path) as f:
        try:
            fcntl.flock(f, fcntl.LOCK_SH)
            return set(line.strip() for line in f if line.strip())
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def append_to_tracker(tracker_path, lines):
    with open(tracker_path, "a") as f:
        try:
            fcntl.flock(f, fcntl.LOCK_EX)
            for line in lines:
                f.write(line + "\n")
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def main():
    args = parse_args()

    # Initialize Hugging Face Accelerate
    accelerator = Accelerator()
    device = accelerator.device

    # Set seed based on rank to keep processes diversified if needed, or deterministic
    set_seed(args.seed + accelerator.process_index)

    weight_dtype = torch.float32
    if accelerator.mixed_precision == "fp16":
        weight_dtype = torch.float16
    elif accelerator.mixed_precision == "bf16":
        weight_dtype = torch.bfloat16

    if accelerator.is_main_process:
        print(f"Loading Base SD model from {args.base_model_dir}...")
    pipe = StableDiffusionPipeline.from_pretrained(
        args.base_model_dir,
        torch_dtype=weight_dtype,
        safety_checker=None,
    ).to(device)
    pipe.set_progress_bar_config(disable=True)

    # Instantiate custom IP-Adapter processing structures on base UNet
    au_proj_model = load_au_adapter(pipe.unet, args.au_adapter_dir, device, weight_dtype)

    # Load pre-trained OpenGraphAU and POSTER++ models
    og_model = load_opengraphau_model(device)
    og_transform = image_eval()

    fer_model = load_poster_v2(device)

    # Configure DDIM Scheduler for deterministic generation
    pipe.scheduler = DDIMScheduler.from_pretrained(args.base_model_dir, subfolder="scheduler")

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
    inverse_class_mapping = {v: k for k, v in class_mapping.items()}

    # Prompt template map
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

    # Preprocessing transform for SD input
    sd_transform = transforms.Compose(
        [
            transforms.Resize((512, 512)),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ]
    )

    # Scan datasets/AffectNet/Test to build source files list
    source_files = []
    for category in class_mapping.keys():
        category_dir = os.path.join(args.ref_dataset_dir, category)
        if os.path.exists(category_dir):
            files = sorted(glob.glob(os.path.join(category_dir, "*.*")))
            # filter only image files
            img_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
            for f in img_files:
                source_files.append((f, category))

    if args.limit is not None and args.limit > 0:
        if accelerator.is_main_process:
            print(f"Limiting evaluation to {args.limit} random samples.")
        rng = random.Random(args.seed)
        rng.shuffle(source_files)
        source_files = source_files[: args.limit]

    if accelerator.is_main_process:
        os.makedirs(args.output_dir, exist_ok=True)
        for category in class_mapping.keys():
            os.makedirs(os.path.join(args.output_dir, category), exist_ok=True)
    accelerator.wait_for_everyone()

    tracker_path = os.path.join(args.output_dir, "processed_tracker.txt")
    target_identifiers = set(f"{cat}/{os.path.basename(f)}" for f, cat in source_files)

    processed_set = load_tracker(tracker_path)
    if len(processed_set) > 0:
        original_count = len(source_files)
        source_files = [(f, cat) for f, cat in source_files if f"{cat}/{os.path.basename(f)}" not in processed_set]
        if accelerator.is_main_process:
            print(
                f"Automatically resuming: skipped {original_count - len(source_files)} "
                f"already generated images. {len(source_files)} remaining."
            )

    if accelerator.is_main_process:
        print(f"Total source images to process: {len(source_files)}")

    # Prepare custom Dataset and DataLoader with preloading
    dataset = AffectNetEvalDataset(source_files, sd_transform, og_transform, class_mapping)
    dataloader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        num_workers=args.num_workers,
        pin_memory=True,
        shuffle=False,
    )

    # Accelerate wraps DataLoader with DistributedSampler automatically
    dataloader = accelerator.prepare(dataloader)

    if accelerator.is_main_process:
        print("Starting controlled generation loop...")

    # Denoising loop
    for batch in tqdm(dataloader, desc="Generating", disable=not accelerator.is_main_process):
        img_sd = batch["img_sd"].to(device, dtype=weight_dtype)
        img_og = batch["img_og"].to(device)
        img_paths = batch["img_path"]
        categories = batch["category"]
        category_idx = batch["category_idx"].to(device)

        batch_size = img_sd.shape[0]

        # 1. Dynamically extract AU labels using OpenGraphAU
        with torch.no_grad():
            au_vector = og_model(img_og)
            au_vector = (au_vector >= 0.5).float().to(dtype=weight_dtype)

        # 2. Get target expression configurations
        target_label_tensor = category_idx

        # 3. Encode prompts in batch
        prompts = [prompt_templates[cat] for cat in categories]
        negative_prompts = ["low quality, distortion, blur"] * batch_size

        prompt_embeds, neg_prompt_embeds = pipe.encode_prompt(
            prompt=prompts,
            device=device,
            num_images_per_prompt=1,
            do_classifier_free_guidance=True,
            negative_prompt=negative_prompts,
        )

        # Encode inversion source prompts (neutral captions)
        inv_prompts = ["a photo of a face"] * batch_size
        inv_prompt_embeds, _ = pipe.encode_prompt(
            prompt=inv_prompts,
            device=device,
            num_images_per_prompt=1,
            do_classifier_free_guidance=False,
        )

        # 4. Prepare early noisy latent using VAE & DDIM Inversion
        with torch.no_grad():
            latent = pipe.vae.encode(img_sd).latent_dist.sample() * pipe.vae.config.scaling_factor

            # DDIM Inversion to get noisy latent at intermediate step
            z = ddim_inversion(
                pipe=pipe,
                unet=pipe.unet,
                au_proj_model=au_proj_model,
                latent=latent,
                text_embeddings=inv_prompt_embeds,
                num_steps=args.num_inference_steps,
                invert_steps=args.invert_steps,
            )

        # 5. Denoising loop with Semantic Guidance (SG)
        pipe.scheduler.set_timesteps(args.num_inference_steps, device=device)
        timesteps_to_denoise = pipe.scheduler.timesteps[len(pipe.scheduler.timesteps) - args.invert_steps :]

        # Text embeddings we can backpropagate through for SG
        text_embeddings = prompt_embeds.clone().detach()

        target_au_token = au_proj_model(au_vector)
        uncond_au_token = au_proj_model(torch.zeros_like(au_vector))

        for i, t in enumerate(timesteps_to_denoise):
            apply_sg = i >= args.sg_start_step

            if apply_sg:
                # Enable gradient tracking on text embedding
                text_embeddings_grad = text_embeddings.clone().detach().requires_grad_(True)
                cond_pos = torch.cat([text_embeddings_grad, target_au_token], dim=1)

                # Forward pass to predict noise
                noise_pred_cond = pipe.unet(z, t, cond_pos).sample

                # Estimate clean latent z0
                alpha_prod_t = pipe.scheduler.alphas_cumprod[t]
                beta_prod_t = 1.0 - alpha_prod_t
                hat_z0 = (z - beta_prod_t**0.5 * noise_pred_cond) / (alpha_prod_t**0.5)

                # Differentiable VAE decoding
                clean_image = pipe.vae.decode(hat_z0.to(dtype=weight_dtype) / pipe.vae.config.scaling_factor).sample

                # Preprocess for POSTER++ classifier
                clean_image = (clean_image + 1.0) / 2.0
                clean_image_resized = F.interpolate(clean_image, size=(224, 224), mode="bilinear", align_corners=False)
                clean_image_resized = clean_image_resized.to(dtype=torch.float32)

                mean = torch.tensor([0.485, 0.456, 0.406], device=device).view(1, 3, 1, 1)
                std = torch.tensor([0.229, 0.224, 0.225], device=device).view(1, 3, 1, 1)
                clean_image_norm = (clean_image_resized - mean) / std

                # Classifier forward pass & gradient step
                logits = fer_model(clean_image_norm)
                loss = F.cross_entropy(logits, target_label_tensor)

                grads = torch.autograd.grad(loss, text_embeddings_grad)[0]
                grads_fp32 = grads.to(torch.float32)
                grads_norm = grads_fp32 / (torch.norm(grads_fp32, p=2, dim=-1, keepdim=True) + 1e-8)
                text_embeddings = text_embeddings - args.sg_step_size * grads_norm.to(text_embeddings.dtype)

            # Standard CFG denoising step with updated embeddings
            with torch.no_grad():
                text_embeddings_all = torch.cat([neg_prompt_embeds, text_embeddings], dim=0)
                au_token_all = torch.cat([uncond_au_token, target_au_token], dim=0)
                cond_all = torch.cat([text_embeddings_all, au_token_all], dim=1)

                latent_model_input = torch.cat([z] * 2)
                latent_model_input = pipe.scheduler.scale_model_input(latent_model_input, t)

                noise_pred = pipe.unet(latent_model_input, t, cond_all).sample

                noise_pred_uncond, noise_pred_cond = noise_pred.chunk(2)
                noise_pred_cfg = noise_pred_uncond + args.guidance_scale * (noise_pred_cond - noise_pred_uncond)

                z = pipe.scheduler.step(noise_pred_cfg, t, z).prev_sample

        # 6. Decode final generated latent and save
        with torch.no_grad():
            generated_img = pipe.vae.decode(z / pipe.vae.config.scaling_factor).sample
            generated_img = (generated_img / 2 + 0.5).clamp(0, 1)
            generated_img = generated_img.to(torch.float32).cpu().permute(0, 2, 3, 1).numpy()
            generated_img = (generated_img * 255).round().astype(np.uint8)

            saved_identifiers = []
            for b in range(batch_size):
                out_img = Image.fromarray(generated_img[b])
                img_basename = os.path.basename(img_paths[b])
                out_img_path = os.path.join(args.output_dir, categories[b], img_basename)
                out_img.save(out_img_path)
                saved_identifiers.append(f"{categories[b]}/{img_basename}")
            append_to_tracker(tracker_path, saved_identifiers)

    # 7. Evaluate Metrics
    # Ensure all processes finish generation before main process evaluates metrics
    accelerator.wait_for_everyone()

    if accelerator.is_main_process:
        print("\nGeneration finished. Calculating metrics...")

        # Delete tracker file if all target images have been generated
        final_processed = load_tracker(tracker_path)
        if target_identifiers.issubset(final_processed):
            if os.path.exists(tracker_path):
                os.remove(tracker_path)
                print(f"All {len(target_identifiers)} images generated. Processed tracker file deleted.")

        # 7.1 FID Calculation
        print("Calculating FID score...")
        fid_score = fid.compute_fid(args.output_dir, args.ref_dataset_dir)
        print(f"FID Score: {fid_score:.4f}")

        # 7.2 FER Accuracy Calculation
        print("Calculating FER Accuracy on synthetic dataset...")
        fer_transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ]
        )

        synthetic_files = []
        for category in class_mapping.keys():
            category_dir = os.path.join(args.output_dir, category)
            if os.path.exists(category_dir):
                files = sorted(glob.glob(os.path.join(category_dir, "*.*")))
                img_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))]
                for f in img_files:
                    synthetic_files.append((f, category))

        correct = 0
        total = len(synthetic_files)
        class_correct = {k: 0 for k in class_mapping.keys()}
        class_total = {k: 0 for k in class_mapping.keys()}

        with torch.no_grad():
            for f, category in tqdm(synthetic_files, desc="Evaluating Acc"):
                img = Image.open(f).convert("RGB")
                tensor_img = fer_transform(img).unsqueeze(0).to(device)
                output = fer_model(tensor_img)
                pred_idx = output.argmax(dim=1).item()
                pred_label = inverse_class_mapping[pred_idx]

                class_total[category] += 1
                if pred_label == category:
                    correct += 1
                    class_correct[category] += 1

        overall_acc = (correct / total) * 100 if total > 0 else 0
        print(f"\nOverall FER Accuracy on Synthetic Dataset: {overall_acc:.2f}%")
        print("Class-wise accuracies:")
        for category in class_mapping.keys():
            correct_cat = class_correct[category]
            total_cat = class_total[category]
            acc_cat = (correct_cat / total_cat) * 100 if total_cat > 0 else 0
            print(f"  {category}: {acc_cat:.2f}% ({correct_cat}/{total_cat})")

        # 7.3 HPSv2 Score Calculation
        print("Calculating HPSv2 score...")
        import sys

        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        import HPSv2

        hps_scores = {k: [] for k in class_mapping.keys()}
        for f, category in tqdm(synthetic_files, desc="Evaluating HPSv2"):
            prompt = prompt_templates[category]
            score_list = HPSv2.score(f, prompt)
            hps_scores[category].extend(score_list)

        overall_hps = (
            float(np.mean([s for scores in hps_scores.values() for s in scores])) if len(synthetic_files) > 0 else 0.0
        )
        print(f"\nOverall HPSv2 on Synthetic Dataset: {overall_hps:.4f}")
        print("Class-wise HPSv2 scores:")
        class_hps_dict = {}
        for category in class_mapping.keys():
            avg_score = float(np.mean(hps_scores[category])) if len(hps_scores[category]) > 0 else 0.0
            class_hps_dict[category] = avg_score
            print(f"  {category}: {avg_score:.4f}")

        # Save validation results JSON
        results_path = os.path.join(args.output_dir, "validation_results.json")
        results = {
            "fid": fid_score,
            "overall_accuracy": overall_acc,
            "class_accuracies": {
                k: (class_correct[k] / class_total[k] * 100 if class_total[k] > 0 else 0) for k in class_mapping.keys()
            },
            "overall_hps": overall_hps,
            "class_hps": class_hps_dict,
            "parameters": vars(args),
        }
        with open(results_path, "w") as f:
            json.dump(results, f, indent=4)
        print(f"Saved validation results to {results_path}")


if __name__ == "__main__":
    main()
