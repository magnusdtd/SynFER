import os
from contextlib import nullcontext

import torch
from accelerate.logging import get_logger
from diffusers.utils.hub_utils import (
    load_or_create_model_card,
    populate_model_card,
)

import wandb

logger = get_logger(__name__, log_level="INFO")


def save_model_card(
    repo_id: str,
    images: list = None,
    base_model: str = None,
    dataset_name: str = None,
    repo_folder: str = None,
):
    img_str = ""
    if images is not None:
        for i, image in enumerate(images):
            image.save(os.path.join(repo_folder, f"image_{i}.png"))
            img_str += f"![img_{i}](./image_{i}.png)\n"

    model_description = f"""
# Fine-tuned text2image model - {repo_id}
This is a stable diffusion model fine-tuned on the {dataset_name} dataset using LoRA, with the LoRA adapter weights merged/fused back into the original base model. You can find some example images in the following. \n
{img_str}
"""

    model_card = load_or_create_model_card(
        repo_id_or_path=repo_id,
        from_training=True,
        license="creativeml-openrail-m",
        base_model=base_model,
        model_description=model_description,
        inference=True,
    )

    tags = [
        "stable-diffusion",
        "stable-diffusion-diffusers",
        "text-to-image",
        "diffusers",
        "diffusers-training",
        "lora",
        "merged",
    ]
    model_card = populate_model_card(model_card, tags=tags)

    model_card.save(os.path.join(repo_folder, "README.md"))


def log_validation(
    pipeline,
    args,
    accelerator,
    epoch,
    is_final_validation=False,
):
    logger.info(
        f"Running validation... \n Generating {args.num_validation_images} images with prompt:"
        f" {args.validation_prompt}."
    )
    if hasattr(pipeline, "safety_checker") and pipeline.safety_checker is not None:
        pipeline.safety_checker = None
    pipeline = pipeline.to(accelerator.device)
    pipeline.set_progress_bar_config(disable=True)
    generator = torch.Generator(device=accelerator.device)
    if args.seed is not None:
        generator = generator.manual_seed(args.seed)
    images = []
    if torch.cuda.is_available():
        autocast_ctx = torch.autocast(accelerator.device.type)
    else:
        autocast_ctx = nullcontext()

    with autocast_ctx:
        for _ in range(args.num_validation_images):
            images.append(
                pipeline(
                    args.validation_prompt,
                    num_inference_steps=50,
                    generator=generator,
                ).images[0]
            )

    for tracker in accelerator.trackers:
        phase_name = "test" if is_final_validation else "validation"
        if tracker.name == "wandb":
            tracker.log(
                {
                    phase_name: [
                        wandb.Image(image, caption=f"{i}: {args.validation_prompt}") for i, image in enumerate(images)
                    ]
                }
            )
    return images
