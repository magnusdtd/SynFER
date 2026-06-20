#!/bin/bash

OUT_DIR="outputs/logs"
mkdir -p "$OUT_DIR"

JOB_ID=$(date +%Y%m%d_%H%M%S)

LOG_FILE="${OUT_DIR}/eva_synfer_${JOB_ID}.log"
ERR_FILE="${OUT_DIR}/eva_synfer_${JOB_ID}.err"

# Customizable Configuration Arguments
BATCH_SIZE=4
NUM_WORKERS=10
NUM_PROCESSES=2
LIMIT=""

PYTHONPATH=.:src:OpenGraphAU:POSTER_V2 uv run accelerate launch \
    --multi_gpu \
    --num_machines 1 \
    --num_processes "$NUM_PROCESSES" \
    --mixed_precision bf16 \
    --dynamo_backend no \
    -m src.evaluate_synfer \
    --au_adapter_dir outputs/sd-fetext-model-au-adapter \
    --base_model_dir outputs/sd-fetext-model-lora \
    --ref_dataset_dir datasets/AffectNet/Test \
    --output_dir outputs/synthetic_affectnet_test \
    --batch_size "$BATCH_SIZE" \
    --num_workers "$NUM_WORKERS" \
    $LIMIT \
    "$@" \
  > >(tee -a "$LOG_FILE") 2> >(tee -a "$ERR_FILE" >&2)
