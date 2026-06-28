# ___***[ICCV'25] SynFER: Towards Boosting Facial Expression Recognition with Synthetic Data (Reproduced version)***___

This repository aims to reproduce the results in the [SynFER](https://openaccess.thecvf.com/content/ICCV2025/papers/He_SynFER_Towards_Boosting_Facial_Expression_Recognition_with_Synthetic_Data_ICCV_2025_paper.pdf) paper.

> **Final Project: Pattern Recognition**
> Tech Stack: PyTorch · FastAPI · Next.js · Stable Diffusion · Diffusers

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-2.7+-EE4C2C?logo=pytorch&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white) ![Next.js](https://img.shields.io/badge/Next.js-14-000000?logo=next.js&logoColor=white) ![LaTeX](https://img.shields.io/badge/LaTeX-Project-008080?logo=latex&logoColor=white) ![Hugging Face](https://img.shields.io/badge/Hugging_Face-Diffusers-FFD21E?logo=huggingface&logoColor=black)

---

## Installation
Install [uv](https://docs.astral.sh/uv/) then run:
```bash
uv sync
```

## Training and Evaluating Commands

Run the following commands to LoRA fine-tune Stable Diffusion v1.5 and train the AU Adapter:
```bash
./scripts/train_lora.sh
./scripts/train_au_adapter.sh
```

Run the following command to evaluate the model:
```bash
./scripts/evaluate_synfer.sh
```

You can adjust the memory usage, path, ... by modifying these Bash scripts.

## To-Do list
- [X] Fine-tuning SD on the FEText dataset
- [X] Continue fine-tuning on the CelebA-HQ and FFHQ
- [X] Use this tool (https://github.com/lingjivoo/OpenGraphAU) to generate facial action units 
- [X] Train the AU-Adapter
- [X] Inference
- [X] Table 1: Generation quality comparisons
- [X] Demo web application with a controller for writing prompts and setting FAUs

## Running the Demo Web Application

This repository includes a web application demo consisting of a FastAPI backend and a Next.js frontend.

### 1. Backend
The backend serves the expression synthesis endpoints. It automatically detects GPU availability and loads the deep learning models (Stable Diffusion, OpenGraphAU, POSTER++).

To start the backend from the repository root:
```bash
uv run -m backend.main
```
The backend server runs on `http://localhost:8000`. (Checkpoints/weights configuration and mock execution settings can be adjusted in `backend/config.py`).

### 2. Frontend
To start the interactive frontend dashboard:
```bash
cd frontend
npm install
npm run dev
```
The development server will be hosted on `http://localhost:3000`.

#### Configuring a Custom Backend URL
If your backend is running on a different port or host (e.g. on a remote server), set the `NEXT_PUBLIC_BACKEND_URL` environment variable when starting or building the frontend:
```bash
NEXT_PUBLIC_BACKEND_URL="http://your-remote-ip:8000" npm run dev
```

## Demo video

[![Demo Video](https://img.youtube.com/vi/gp4ISudSgzY/0.jpg)](https://youtu.be/gp4ISudSgzY)

## Resources:
 - [SynFER](https://github.com/C0notSilly/SynFER)
 - [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter/)
 - [Diffusers - Fine-tuning Text-to-Image Model](https://github.com/huggingface/diffusers/tree/main/examples/text_to_image)
 - [POSTER++](https://github.com/Talented-Q/POSTER_V2)
 - [clean-fid for Evaluating Generative Models](https://github.com/GaParmar/clean-fid)
 - [HPSv2](https://github.com/tgxs002/HPSv2)
 - [MPS](https://github.com/Kwai-Kolors/MPS)
 - [FaceScore](https://github.com/OPPO-Mente-Lab/FaceScore)