import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

from datasets import load_dataset


class FETextDataset(Dataset):
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

        parquet_pattern = os.path.join(root_dir, "data", "train-*.parquet")
        self.dataset = load_dataset("parquet", data_files=parquet_pattern, split="train")

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        image = item["image"]
        if not isinstance(image, Image.Image):
            image = Image.open(image).convert("RGB")
        else:
            image = image.convert("RGB")

        pixel_values = self.transform(image)
        caption = item["caption"]

        input_ids = self.tokenizer(
            caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids[0]

        return {"pixel_values": pixel_values, "input_ids": input_ids}


def fetex_collate_fn(batch):
    pixel_values = torch.stack([example["pixel_values"] for example in batch])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}
