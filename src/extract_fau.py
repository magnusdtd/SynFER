import json
import os

import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from datasets import load_dataset
from OpenGraphAU.model.MEFL import MEFARG
from OpenGraphAU.utils import image_eval, load_state_dict

from .extract_fau_utils import OpenGraphAUDataset, parse_args


def main():

    args = parse_args()

    print(f"Loading parquet dataset from pattern: {args.parquet_pattern}")
    hf_dataset = load_dataset("parquet", data_files=args.parquet_pattern, split="train")
    if args.limit > 0:
        print(f"Limiting dataset to first {args.limit} samples for testing.")
        hf_dataset = hf_dataset.select(range(min(args.limit, len(hf_dataset))))
    print(f"Loaded dataset with {len(hf_dataset)} examples.")

    print(f"Initializing OpenGraphAU Model ({args.arc})...")
    net = MEFARG(
        num_main_classes=27,
        num_sub_classes=14,
        backbone=args.arc,
    )
    print(f"Resuming model checkpoint from: {args.resume}")
    net = load_state_dict(net, args.resume)
    net.eval()

    if torch.cuda.is_available():
        print("CUDA is available. Running inference on GPU.")
        net = net.cuda()
    else:
        print("CUDA is not available. Running inference on CPU.")

    images_dir = os.path.join(args.output_dir, "images")
    print(f"Target images directory: {images_dir}")

    # Initialize PyTorch dataset and loader
    dataset = OpenGraphAUDataset(hf_dataset, image_eval(), images_dir)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)

    fau_labels = {}
    captions = []

    print("Starting processing and extraction...")
    with torch.no_grad():
        for batch in tqdm(dataloader, desc="Extracting & Predicting FAUs"):
            tensors = batch["tensor"]
            base_names = batch["base_name"]
            batch_captions = batch["caption"]

            if torch.cuda.is_available():
                tensors = tensors.cuda()

            # Batch model prediction
            preds = net(tensors)
            # Threshold predictions at 0.5 to get binary labels (0 or 1)
            preds = (preds >= 0.5).int().cpu().numpy()

            for i in range(len(base_names)):
                name = base_names[i]
                cap = batch_captions[i]
                pred_val = preds[i]

                # Format prediction as a space-separated string of binary labels
                pred_str = " ".join(map(str, pred_val))
                fau_labels[name] = pred_str

                # Caption dictionary entry in format: {"image_name": "caption"}
                captions.append({name: cap})

    # Save captions JSON
    captions_path = os.path.join(args.output_dir, "captions.json")
    print(f"Saving captions to: {captions_path}")
    with open(captions_path, "w") as f:
        json.dump(captions, f, indent=4)

    # Save FAU labels JSON
    fau_labels_path = os.path.join(args.output_dir, "fau_labels.json")
    print(f"Saving FAU labels to: {fau_labels_path}")
    with open(fau_labels_path, "w") as f:
        json.dump(fau_labels, f, indent=4)

    print("Extraction and prediction completed successfully!")


if __name__ == "__main__":
    main()
