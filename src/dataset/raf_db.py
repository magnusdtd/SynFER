import csv
import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

RAF_DB_EMOTIONS = {
    1: "surprised",
    2: "fear",
    3: "disgust",
    4: "happy",
    5: "sad",
    6: "angry",
    7: "neutral",
}


class RAFDBDataset(Dataset):
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

        # split can be "train", "test", "both"
        splits_to_use = []
        if split == "train":
            splits_to_use = [("train", "train_labels.csv")]
        elif split in ["test", "val"]:
            splits_to_use = [("test", "test_labels.csv")]
        elif split == "both":
            splits_to_use = [("train", "train_labels.csv"), ("test", "test_labels.csv")]
        else:
            raise ValueError(f"Unknown split for RAF-DB: {split}")

        for split_dir_name, labels_file_name in splits_to_use:
            labels_path = os.path.join(root_dir, labels_file_name)
            split_dir = os.path.join(root_dir, split_dir_name)

            if os.path.exists(labels_path) and os.path.exists(split_dir):
                with open(labels_path, encoding="utf-8") as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Skip header: image,label
                    for row in reader:
                        if not row or len(row) < 2:
                            continue
                        img_name = row[0]
                        try:
                            label_idx = int(row[1])
                        except ValueError:
                            continue

                        img_path = os.path.join(split_dir, img_name)
                        if os.path.exists(img_path):
                            self.samples.append((img_path, label_idx))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label_idx = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        pixel_values = self.transform(image)

        emotion = RAF_DB_EMOTIONS.get(label_idx, "neutral")
        caption = f"a photo of a {emotion} face"

        input_ids = self.tokenizer(
            caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids[0]

        return {"pixel_values": pixel_values, "input_ids": input_ids}


def raf_db_collate_fn(batch):
    pixel_values = torch.stack([example["pixel_values"] for example in batch])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}
