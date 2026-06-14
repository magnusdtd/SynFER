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
- [ ] Fine-tuning on the CelebA-HQ and FFHQ
- [X] Use this tool (https://github.com/lingjivoo/OpenGraphAU) generate facial action units 
- [ ] Train the AU-Adapter

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