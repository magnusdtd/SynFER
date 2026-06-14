import csv
import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


class AffectNetDataset(Dataset):
    def __init__(
        self,
        root_dir: str,
        tokenizer,
        transform=None,
        size: int = 512,
        split: str = "train",
    ):
        self.root_dir = root_dir
        self.tokenizer = tokenizer
        self.split = split
        self.size = size

        if transform is not None:
            self.transform = transform
        else:
            self.transform = transforms.Compose(
                [
                    transforms.Resize(self.size, interpolation=transforms.InterpolationMode.BILINEAR),
                    transforms.CenterCrop(self.size),
                    transforms.ToTensor(),
                    transforms.Normalize([0.5], [0.5]),
                ]
            )

        self.samples = []
        labels_csv_path = os.path.join(root_dir, "labels.csv")

        # split can be "train", "test", "both"
        splits_to_use = []
        if split == "train":
            splits_to_use = ["Train"]
        elif split in ["test", "val"]:
            splits_to_use = ["Test"]
        elif split == "both":
            splits_to_use = ["Train", "Test"]
        else:
            raise ValueError(f"Unknown split for AffectNet: {split}")

        if os.path.exists(labels_csv_path):
            with open(labels_csv_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header: ,path,label,relFCs
                for row in reader:
                    if not row or len(row) < 3:
                        continue
                    # row format: [index, path, label, relFCs]
                    path = row[1]
                    label = row[2]

                    # Search in configured splits
                    for split_dir in splits_to_use:
                        img_path = os.path.join(root_dir, split_dir, path)
                        if os.path.exists(img_path):
                            self.samples.append((img_path, label))
                            break

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        pixel_values = self.transform(image)

        caption = f"a photo of a face with a {label} expression"

        input_ids = self.tokenizer(
            caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids[0]

        return {"pixel_values": pixel_values, "input_ids": input_ids}


def affectnet_collate_fn(batch):
    pixel_values = torch.stack([example["pixel_values"] for example in batch])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}
