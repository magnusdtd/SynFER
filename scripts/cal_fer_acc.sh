#!/bin/bash

OUT_DIR="outputs/logs"
mkdir -p "$OUT_DIR"

JOB_ID=$(date +%Y%m%d_%H%M%S)

LOG_FILE="${OUT_DIR}/cal_fer_acc_${JOB_ID}.log"
ERR_FILE="${OUT_DIR}/cal_fer_acc_${JOB_ID}.err"

PYTHONPATH=POSTER_V2 uv run -m POSTER_V2.main \
    --data "datasets/AffectNet/Test" \
    --evaluate "models/POSTER_V2/affectnet-8-model_best.pth" \
  > >(tee -a "$LOG_FILE") 2> >(tee -a "$ERR_FILE" >&2)
