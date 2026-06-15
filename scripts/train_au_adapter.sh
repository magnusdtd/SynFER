#!/bin/bash

export HF_TOKEN=...
export WANDB_TOKEN=...
export WANDB_PROJECT=SynFER
export WANDB_DISABLED=false
export MODEL_NAME="outputs/sd-fetext-model-lora"
export DATASET_NAME="fetext"
export DATA_DIR="datasets"
export OUTPUT_DIR="outputs/sd-fetext-model-au-adapter"

# Make sure local ip_adapter can be imported
export PYTHONPATH=src:$PYTHONPATH

OUT_DIR="outputs/logs"
mkdir -p "$OUT_DIR"

JOB_ID=$(date +%Y%m%d_%H%M%S)

LOG_FILE="${OUT_DIR}/sd_au_adapter_${JOB_ID}.log"
ERR_FILE="${OUT_DIR}/sd_au_adapter_${JOB_ID}.err"

export OMP_NUM_THREADS=10
export NVIDIA_TF32_OVERRIDE=1

MPLBACKEND=Agg uv run accelerate launch \
  --multi_gpu \
  --num_machines 1 \
  --num_processes 2 \
  --mixed_precision bf16 \
  --dynamo_backend no \
  -m src.train_au_adapter \
  --pretrained_model_name_or_path="$MODEL_NAME" \
  --dataset_name="$DATASET_NAME" \
  --train_data_dir="$DATA_DIR" \
  --hf_token ${HF_TOKEN} \
  --wb_token ${WANDB_TOKEN} \
  --dataset_split="train" \
  --resolution=512 \
  --random_flip \
  --train_batch_size=32 \
  --num_train_epochs=50 \
  --checkpointing_steps=2000 \
  --learning_rate=1e-04 \
  --lr_scheduler="constant" \
  --lr_warmup_steps=0 \
  --seed=3407 \
  --output_dir="$OUTPUT_DIR" \
  --validation_prompt="a photo of an happy face" \
  --report_to="wandb" \
  --allow_tf32 \
  > >(tee -a "$LOG_FILE") 2> >(tee -a "$ERR_FILE" >&2)