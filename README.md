# ___***[ICCV'25] SynFER: Towards Boosting Facial Expression Recognition with Synthetic Data (Reproduced version)***___

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
- [ ] Train the AU-Adapter
- [ ] Inference
- [ ] Table 5. Ablation study on AU injection and semantic guidance (SG) on both generation quality and supervised learning. SD denotes Stable Diffusion, which is used as a baseline.
- [ ] Figure 5. Example of generated samples: Stable Diffusion, +FEText, +FEText+FAUs, +FEText+FAUs+SG.
- [ ] Table 1. Generation quality comparisons. Ours vs.’ shows the proportion of users who prefer our method over the alternative. An MPS above 1.00 and results above 50% in the user study indicate SynFER outplays the counterpart. FS, FER Acc., FAU Acc., EA and FF denote FaceScore, FER accuracy, facial action unit accuracy, expression alignment and face fidelity, respectively.
- [ ] Demo web app có controller để viết câu prompt + set FAUs

## Notes:
- Diffusers' EMMAAModel

# Tasks:
- Save images of the log validation into disk
- Add tqdm in the "for step, batch in enumerate(train_dataloader):"
- 

## Resources:
 - [SynFER](https://github.com/C0notSilly/SynFER)
 - [IP-Adapter](https://github.com/tencent-ailab/IP-Adapter/)
 - [Diffusers - Fine-tuning Text-to-Image Model](https://github.com/huggingface/diffusers/tree/main/examples/text_to_image)