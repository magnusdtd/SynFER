import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


class CelebAHQDataset(Dataset):
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

        # split can be "train", "val", "both"
        splits_to_use = []
        if split == "train":
            splits_to_use = ["train"]
        elif split == "val":
            splits_to_use = ["val"]
        elif split == "both":
            splits_to_use = ["train", "val"]
        else:
            raise ValueError(f"Unknown split for CelebA-HQ: {split}")

        for split_dir in splits_to_use:
            split_path = os.path.join(root_dir, split_dir)
            if os.path.exists(split_path):
                for gender in ["female", "male"]:
                    gender_dir = os.path.join(split_path, gender)
                    if os.path.isdir(gender_dir):
                        for fname in os.listdir(gender_dir):
                            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                                img_path = os.path.join(gender_dir, fname)
                                self.samples.append((img_path, gender))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, gender = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        pixel_values = self.transform(image)

        gender_word = "woman" if gender == "female" else "man"
        caption = f"a photo of a {gender_word}"

        input_ids = self.tokenizer(
            caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids[0]

        return {"pixel_values": pixel_values, "input_ids": input_ids}


def celeba_hq_collate_fn(batch):
    pixel_values = torch.stack([example["pixel_values"] for example in batch])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}
