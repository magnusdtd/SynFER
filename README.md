# ___***[ICCV'25] SynFER: Towards Boosting Facial Expression Recognition with Synthetic Data (Reproduced version)***___

This repo aims to reproduce the result in the [SynFER](https://openaccess.thecvf.com/content/ICCV2025/papers/He_SynFER_Towards_Boosting_Facial_Expression_Recognition_with_Synthetic_Data_ICCV_2025_paper.pdf) paper.

## Training Command: 
```bash
accelerate launch src/train_text_to_image_lora.py \
  --pretrained_model_name_or_path="CompVis/stable-diffusion-v1-4" \
  --dataset_name="fetext" \
  --train_data_dir="/media/ltnghia34/SynFER/datasets" \
  --resolution=512 \
  --train_batch_size=1 \
  --learning_rate=1e-04 \
  --output_dir="sd-sfew-model"
```

## To-Do list:
- [X] Fine-tuning SD on the FEText dataset
- [ ] Continue fine-tuning on the CelebA-HQ and FFHQ
- [X] Use this tool (https://github.com/lingjivoo/OpenGraphAU) generate facial action units 
- [X] Train the AU-Adapter
- [ ] Inference
- [ ] Table 5. Ablation study on AU injection and semantic guidance (SG) on both generation quality and supervised learning. SD denotes Stable Diffusion, which is used as a baseline.
- [ ] Figure 5. Example of generated samples: Stable Diffusion, +FEText, +FEText+FAUs, +FEText+FAUs+SG.
- [ ] Table 1. Generation quality comparisons. Ours vs.’ shows the proportion of users who prefer our method over the alternative. An MPS above 1.00 and results above 50% in the user study indicate SynFER outplays the counterpart. FS, FER Acc., FAU Acc., EA and FF denote FaceScore, FER accuracy, facial action unit accuracy, expression alignment and face fidelity, respectively.
- [ ] Demo web app có controller để viết câu prompt + set FAUs

## Notes:
- Diffusers' EMMAAModel

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

## Resources:
 - [SynFER](https://github.com/C0notSilly/SynFER)
 - [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter/)
 - [Diffusers - Fine-tuning Text-to-Image Model](https://github.com/huggingface/diffusers/tree/main/examples/text_to_image)
 - [POSTER++](https://github.com/Talented-Q/POSTER_V2)
 - [clean-fid for Evaluating Generative Models](https://github.com/GaParmar/clean-fid)
 - [HPSv2](https://github.com/tgxs002/HPSv2)
