import itertools
import math
import os
import shutil
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from accelerate import Accelerator
from accelerate.utils import ProjectConfiguration
from diffusers import AutoencoderKL, DDPMScheduler, StableDiffusionPipeline, UNet2DConditionModel
from diffusers.optimization import get_scheduler
from tqdm.auto import tqdm
from transformers import CLIPTextModel, CLIPTokenizer

from .ip_adapter.utils import is_torch2_available

if is_torch2_available():
    from .ip_adapter.attention_processor import AttnProcessor2_0 as AttnProcessor
    from .ip_adapter.attention_processor import IPAttnProcessor2_0 as IPAttnProcessor
else:
    from .ip_adapter.attention_processor import AttnProcessor, IPAttnProcessor

from .au_adapter import AUAdapter, AUProjModel
from .au_dataset import HybridDataset, au_collate_fn
from .train_lora_args import parse_args
from .utils import logger, set_seed, setup_logging


@torch.no_grad()
def log_validation_au(
    vae,
    text_encoder,
    tokenizer,
    unet,
    au_proj_model,
    args,
    accelerator,
    weight_dtype,
    epoch,
    is_final_validation=False,
):
    logger.info(f"Running validation for epoch {epoch}...")

    pipeline = StableDiffusionPipeline.from_pretrained(
        args.pretrained_model_name_or_path,
        vae=vae,
        text_encoder=text_encoder,
        tokenizer=tokenizer,
        unet=unet,
        safety_checker=None,
        torch_dtype=weight_dtype,
    )
    pipeline = pipeline.to(accelerator.device)
    pipeline.set_progress_bar_config(disable=True)

    # Define validation AU labels and prompts
    validation_prompts = [
        "a photo of a face with happy expression",
        "a photo of a face with angry expression",
        "a photo of a face with sad expression",
        "a photo of a face with surprised expression",
    ]
    # Corresponding AU labels (41 dimensions)
    validation_aus = [
        # Happy: AU6, AU12 (index 4 and 9)
        [0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        # Angry: AU4, AU7, AU9, AU24 (indices 2, 5, 7, 23)
        [0,0,1,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        # Sad: AU1, AU4, AU15 (indices 0, 2, 14)
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        # Surprised: AU1, AU2, AU5, AU26 (indices 0, 1, 3, 25)
        [1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    generator = torch.Generator(device=accelerator.device)
    if args.seed is not None:
        generator = generator.manual_seed(args.seed)

    images = []
    with accelerator.autocast():
        for prompt, au_list in zip(validation_prompts, validation_aus):
            # Construct the prompt embeds and append the AU tokens
            pos_prompt_embeds, neg_prompt_embeds = pipeline.encode_prompt(
                prompt=prompt,
                device=accelerator.device,
                num_images_per_prompt=1,
                do_classifier_free_guidance=True,
                negative_prompt="low quality, distortion, blur",
            )

            # Project the AU label
            au_tensor = torch.tensor([au_list], device=accelerator.device, dtype=weight_dtype)  # shape (1, 41)
            au_embed = au_proj_model(au_tensor)  # shape (1, 1, cross_attention_dim)

            # Construct unconditional AU embed (zeros)
            uncond_au_tensor = torch.zeros_like(au_tensor)
            uncond_au_embed = au_proj_model(uncond_au_tensor)

            # Concatenate them to prompt_embeds
            pos_combined = torch.cat([pos_prompt_embeds, au_embed], dim=1)  # shape (1, 78, cross_attention_dim)
            neg_combined = torch.cat([neg_prompt_embeds, uncond_au_embed], dim=1)  # shape (1, 78, cross_attention_dim)

            image = pipeline(
                prompt_embeds=pos_combined,
                negative_prompt_embeds=neg_combined,
                num_inference_steps=50,
                generator=generator,
            ).images[0]
            images.append(image)

    # Log to trackers
    for tracker in accelerator.trackers:
        phase_name = "test" if is_final_validation else "validation"
        if tracker.name == "wandb":
            import wandb

            tracker.log(
                {
                    phase_name: [
                        wandb.Image(image, caption=f"{prompt}") for image, prompt in zip(images, validation_prompts)
                    ]
                }
            )

    del pipeline
    torch.cuda.empty_cache()

    return images


def main():
    args = parse_args()

    if args.seed is not None:
        set_seed(args.seed)
    setup_logging(False)

    au_dim = 41

    logging_dir = Path(args.output_dir, args.logging_dir)
    accelerator_project_config = ProjectConfiguration(project_dir=args.output_dir, logging_dir=logging_dir)

    accelerator = Accelerator(
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        mixed_precision=args.mixed_precision,
        log_with=args.report_to,
        project_config=accelerator_project_config,
    )

    if accelerator.is_main_process:
        if args.output_dir is not None:
            os.makedirs(args.output_dir, exist_ok=True)

    # Load scheduler, tokenizer and models from pretrained path
    logger.info(f"Loading base model from {args.pretrained_model_name_or_path}...")
    noise_scheduler = DDPMScheduler.from_pretrained(args.pretrained_model_name_or_path, subfolder="scheduler")
    tokenizer = CLIPTokenizer.from_pretrained(args.pretrained_model_name_or_path, subfolder="tokenizer")
    text_encoder = CLIPTextModel.from_pretrained(args.pretrained_model_name_or_path, subfolder="text_encoder")
    vae = AutoencoderKL.from_pretrained(args.pretrained_model_name_or_path, subfolder="vae")
    unet = UNet2DConditionModel.from_pretrained(args.pretrained_model_name_or_path, subfolder="unet")

    # freeze parameters of models to save more memory
    unet.requires_grad_(False)
    vae.requires_grad_(False)
    text_encoder.requires_grad_(False)

    # Set up AU Proj Model and decouple cross-attention layers
    au_proj_model = AUProjModel(
        au_dim=au_dim,
        cross_attention_dim=unet.config.cross_attention_dim,
    )

    # init adapter modules with num_tokens=1
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
                num_tokens=1
            )
            attn_procs[name].load_state_dict(weights)
    unet.set_attn_processor(attn_procs)
    adapter_modules = torch.nn.ModuleList(unet.attn_processors.values())

    ip_adapter = AUAdapter(unet, au_proj_model, adapter_modules)

    weight_dtype = torch.float32
    if accelerator.mixed_precision == "fp16":
        weight_dtype = torch.float16
    elif accelerator.mixed_precision == "bf16":
        weight_dtype = torch.bfloat16

    vae.to(accelerator.device, dtype=weight_dtype)
    text_encoder.to(accelerator.device, dtype=weight_dtype)

    # optimizer
    params_to_opt = itertools.chain(ip_adapter.au_proj_model.parameters(), ip_adapter.adapter_modules.parameters())
    optimizer = torch.optim.AdamW(
        params_to_opt,
        lr=args.learning_rate,
        betas=(args.adam_beta1, args.adam_beta2),
        weight_decay=args.adam_weight_decay,
        eps=args.adam_epsilon,
    )

    # dataset loading
    if args.dataset_name == "fetext":
        img_folder = os.path.join(args.train_data_dir, "FEText", "images")
        caption_path = os.path.join(args.train_data_dir, "FEText", "captions.json")
        au_path = os.path.join(args.train_data_dir, "FEText", "fau_labels.json")

        if not os.path.exists(img_folder):
            raise FileNotFoundError(f"Image folder not found: {img_folder}")
        if not os.path.exists(caption_path):
            raise FileNotFoundError(f"Caption file not found: {caption_path}")
        if not os.path.exists(au_path):
            raise FileNotFoundError(f"FAU labels file not found: {au_path}")

        img_file_list = [img_folder]
        txt_file_list = [caption_path]
        au_file_list = [au_path]
    else:
        raise ValueError(f"Unknown dataset_name: {args.dataset_name}. Must be 'fetext'")

    train_dataset = HybridDataset(
        img_file_list, 
        txt_file_list, 
        au_file_list, 
        tokenizer, 
        size=args.resolution,
    )

    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        shuffle=True,
        collate_fn=au_collate_fn,
        batch_size=args.train_batch_size,
        num_workers=args.dataloader_num_workers,
    )

    # Enable TF32 for faster training on Ampere GPUs
    if args.allow_tf32:
        torch.backends.cuda.matmul.allow_tf32 = True

    # Scheduler and math around the number of training steps.
    num_warmup_steps_for_scheduler = args.lr_warmup_steps * accelerator.num_processes
    if args.max_train_steps is None:
        len_train_dataloader_after_sharding = math.ceil(len(train_dataloader) / accelerator.num_processes)
        num_update_steps_per_epoch = math.ceil(len_train_dataloader_after_sharding / args.gradient_accumulation_steps)
        num_training_steps_for_scheduler = (
            args.num_train_epochs * num_update_steps_per_epoch * accelerator.num_processes
        )
    else:
        num_training_steps_for_scheduler = args.max_train_steps * accelerator.num_processes

    lr_scheduler = get_scheduler(
        args.lr_scheduler,
        optimizer=optimizer,
        num_warmup_steps=num_warmup_steps_for_scheduler,
        num_training_steps=num_training_steps_for_scheduler,
    )

    # Unwrap helper
    def unwrap_model(model):
        from diffusers.utils.torch_utils import is_compiled_module

        model = accelerator.unwrap_model(model)
        model = model._orig_mod if is_compiled_module(model) else model
        return model

    # Custom save and load state hooks to only write adapter weights
    def save_model_hook(models, weights, output_dir):
        if accelerator.is_main_process:
            for model in models:
                unwrapped = unwrap_model(model)
                if isinstance(unwrapped, AUAdapter):
                    state_dict = {
                        "image_proj": unwrapped.au_proj_model.state_dict(),
                        "ip_adapter": unwrapped.adapter_modules.state_dict(),
                    }
                    torch.save(state_dict, os.path.join(output_dir, "model.safetensors"))
                    weights.pop()

    def load_model_hook(models, input_dir):
        for model in models:
            unwrapped = unwrap_model(model)
            if isinstance(unwrapped, AUAdapter):
                state_dict = torch.load(os.path.join(input_dir, "model.safetensors"), map_location="cpu")
                unwrapped.au_proj_model.load_state_dict(state_dict["image_proj"])
                unwrapped.adapter_modules.load_state_dict(state_dict["ip_adapter"])

    accelerator.register_save_state_pre_hook(save_model_hook)
    accelerator.register_load_state_pre_hook(load_model_hook)

    # Prepare everything with our `accelerator`.
    ip_adapter, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
        ip_adapter, optimizer, train_dataloader, lr_scheduler
    )

    # We need to recalculate our total training steps as the size of the training dataloader may have changed.
    num_update_steps_per_epoch = math.ceil(len(train_dataloader) / args.gradient_accumulation_steps)
    if args.max_train_steps is None:
        args.max_train_steps = args.num_train_epochs * num_update_steps_per_epoch
    # Afterwards we recalculate our number of training epochs
    args.num_train_epochs = math.ceil(args.max_train_steps / num_update_steps_per_epoch)

    # We need to initialize the trackers we use, and also store our configuration.
    if accelerator.is_main_process:
        accelerator.init_trackers("SynFER", config=vars(args))

    total_batch_size = args.train_batch_size * accelerator.num_processes * args.gradient_accumulation_steps

    logger.info("***** Running training *****")
    logger.info(f"  Num examples = {len(train_dataset)}")
    logger.info(f"  Num Epochs = {args.num_train_epochs}")
    logger.info(f"  Instantaneous batch size per device = {args.train_batch_size}")
    logger.info(f"  Total train batch size (w. parallel, distributed & accumulation) = {total_batch_size}")
    logger.info(f"  Gradient Accumulation steps = {args.gradient_accumulation_steps}")
    logger.info(f"  Total optimization steps = {args.max_train_steps}")

    global_step = 0
    first_epoch = 0

    # Potentially load in the weights and states from a previous save
    if args.resume_from_checkpoint:
        if args.resume_from_checkpoint != "latest":
            path = os.path.basename(args.resume_from_checkpoint)
        else:
            # Get the most recent checkpoint
            dirs = os.listdir(args.output_dir)
            dirs = [d for d in dirs if d.startswith("checkpoint")]
            dirs = sorted(dirs, key=lambda x: int(x.split("-")[1]))
            path = dirs[-1] if len(dirs) > 0 else None

        if path is None:
            accelerator.print(
                f"Checkpoint '{args.resume_from_checkpoint}' does not exist. Starting a new training run."
            )
            args.resume_from_checkpoint = None
            initial_global_step = 0
        else:
            accelerator.print(f"Resuming from checkpoint {path}")
            accelerator.load_state(os.path.join(args.output_dir, path))
            global_step = int(path.split("-")[1])
            initial_global_step = global_step
            first_epoch = global_step // num_update_steps_per_epoch
    else:
        initial_global_step = 0

    progress_bar = tqdm(
        range(0, args.max_train_steps),
        initial=initial_global_step,
        desc="Steps",
        disable=not accelerator.is_local_main_process,
    )

    for epoch in range(first_epoch, args.num_train_epochs):
        ip_adapter.train()
        train_loss = 0.0
        for step, batch in enumerate(train_dataloader):
            begin = time.perf_counter()
            with accelerator.accumulate(ip_adapter):
                # Convert images to latent space
                with torch.no_grad():
                    latents = vae.encode(batch["images"].to(dtype=weight_dtype)).latent_dist.sample()
                    latents = latents * vae.config.scaling_factor

                # Sample noise that we'll add to the latents
                noise = torch.randn_like(latents)
                bsz = latents.shape[0]
                # Sample a random timestep for each image
                timesteps = torch.randint(0, noise_scheduler.config.num_train_timesteps, (bsz,), device=latents.device)
                timesteps = timesteps.long()

                # Add noise to the latents according to the noise magnitude at each timestep
                noisy_latents = noise_scheduler.add_noise(latents, noise, timesteps)

                # Get the text embedding for conditioning
                with torch.no_grad():
                    encoder_hidden_states = text_encoder(batch["text_input_ids"])[0]

                au_labels = batch["au_label"].to(dtype=weight_dtype)

                # Predict the noise residual
                noise_pred = ip_adapter(noisy_latents, timesteps, encoder_hidden_states, au_labels)

                loss = F.mse_loss(noise_pred.float(), noise.float(), reduction="mean")

                # Gather the losses across all processes for logging
                avg_loss = accelerator.gather(loss.repeat(args.train_batch_size)).mean()
                train_loss += avg_loss.item() / args.gradient_accumulation_steps

                # Backpropagate
                accelerator.backward(loss)
                if accelerator.sync_gradients:
                    # Clip grads only for trainable parameters (au_proj_model and adapter_modules)
                    accelerator.clip_grad_norm_(params_to_opt, args.max_grad_norm)
                optimizer.step()
                lr_scheduler.step()
                optimizer.zero_grad()

            # Checks if the accelerator has performed an optimization step behind the scenes
            if accelerator.sync_gradients:
                progress_bar.update(1)
                global_step += 1
                accelerator.log({"train_loss": train_loss}, step=global_step)
                train_loss = 0.0

                if global_step % args.checkpointing_steps == 0:
                    if accelerator.is_main_process:
                        if args.checkpoints_total_limit is not None:
                            checkpoints = os.listdir(args.output_dir)
                            checkpoints = [d for d in checkpoints if d.startswith("checkpoint")]
                            checkpoints = sorted(checkpoints, key=lambda x: int(x.split("-")[1]))

                            if len(checkpoints) >= args.checkpoints_total_limit:
                                num_to_remove = len(checkpoints) - args.checkpoints_total_limit + 1
                                removing_checkpoints = checkpoints[0:num_to_remove]
                                for removing_checkpoint in removing_checkpoints:
                                    removing_checkpoint = os.path.join(args.output_dir, removing_checkpoint)
                                    shutil.rmtree(removing_checkpoint)

                        save_path = os.path.join(args.output_dir, f"checkpoint-{global_step}")
                        accelerator.save_state(save_path)
                        logger.info(f"Saved state to {save_path}")

            logs = {
                "step_loss": loss.detach().item(),
                "lr": lr_scheduler.get_last_lr()[0],
                "data_time": time.perf_counter() - begin,
            }
            progress_bar.set_postfix(**logs)

            if global_step >= args.max_train_steps:
                break

        # Epoch-level validation
        if accelerator.is_main_process:
            if args.validation_prompt is not None and epoch % args.validation_epochs == 0:
                unwrapped_ip_adapter = unwrap_model(ip_adapter)
                log_validation_au(
                    vae=vae,
                    text_encoder=text_encoder,
                    tokenizer=tokenizer,
                    unet=unet,
                    au_proj_model=unwrapped_ip_adapter.au_proj_model,
                    args=args,
                    accelerator=accelerator,
                    weight_dtype=weight_dtype,
                    epoch=epoch,
                )

    # Save the final adapter weights
    accelerator.wait_for_everyone()
    if accelerator.is_main_process:
        unwrapped_ip_adapter = unwrap_model(ip_adapter)
        state_dict = {
            "image_proj": unwrapped_ip_adapter.au_proj_model.state_dict(),
            "ip_adapter": unwrapped_ip_adapter.adapter_modules.state_dict(),
        }
        # Save both for maximum compatibility with any checkpoint reader
        torch.save(state_dict, os.path.join(args.output_dir, "model.safetensors"))
        torch.save(state_dict, os.path.join(args.output_dir, "ip_adapter.bin"))
        logger.info(f"Saved final AU-Adapter weights to {args.output_dir}")

        # Final validation
        if args.validation_prompt is not None:
            log_validation_au(
                vae=vae,
                text_encoder=text_encoder,
                tokenizer=tokenizer,
                unet=unet,
                au_proj_model=unwrapped_ip_adapter.au_proj_model,
                args=args,
                accelerator=accelerator,
                weight_dtype=weight_dtype,
                epoch=epoch,
                is_final_validation=True,
            )

    accelerator.end_training()


if __name__ == "__main__":
    main()
