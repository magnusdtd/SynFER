#!/bin/bash

# Configuration
ARC="resnet50"
RESUME="models/OpenGraphAU/OpenGprahAU-ResNet50_second_stage.pth"
PARQUET_PATTERN="datasets/FEText/data/train-*.parquet"
OUTPUT_DIR="datasets/FEText"
BATCH_SIZE=64
NUM_WORKERS=10

OUT_DIR="outputs/logs"
mkdir -p "$OUT_DIR"

JOB_ID=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${OUT_DIR}/extract_fau_${JOB_ID}.log"
ERR_FILE="${OUT_DIR}/extract_fau_${JOB_ID}.err"

echo "Starting FAU extraction using OpenGraphAU..."
echo "Architecture: $ARC"
echo "Checkpoint: $RESUME"
echo "Output Directory: $OUTPUT_DIR"
echo "Logging to $LOG_FILE and $ERR_FILE"

uv run -m src.extract_fau \
  --parquet_pattern "$PARQUET_PATTERN" \
  --arc "$ARC" \
  --resume "$RESUME" \
  --output_dir "$OUTPUT_DIR" \
  --batch_size $BATCH_SIZE \
  --num_workers $NUM_WORKERS \
  > >(tee -a "$LOG_FILE") 2> >(tee -a "$ERR_FILE" >&2)

echo "FAU extraction script finished."
