import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

SFEW_EMOTIONS = {
    "Angry": "angry",
    "Disgust": "disgust",
    "Fear": "fear",
    "Happy": "happy",
    "Neutral": "neutral",
    "Sad": "sad",
    "Surprise": "surprised",
}


class SFEWDataset(Dataset):
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
            splits_to_use = ["Train"]
        elif split in ["val", "validation"]:
            splits_to_use = ["Validation"]
        elif split == "both":
            splits_to_use = ["Train", "Validation"]
        else:
            raise ValueError(f"Unknown split for SFEW: {split}")

        for split_dir_name in splits_to_use:
            split_dir = os.path.join(root_dir, split_dir_name)
            if os.path.exists(split_dir):
                for folder_name in os.listdir(split_dir):
                    folder_path = os.path.join(split_dir, folder_name)
                    if os.path.isdir(folder_path):
                        emotion = SFEW_EMOTIONS.get(folder_name, folder_name.lower())
                        for fname in os.listdir(folder_path):
                            if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                                img_path = os.path.join(folder_path, fname)
                                self.samples.append((img_path, emotion))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, emotion = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        pixel_values = self.transform(image)

        caption = f"a photo of a {emotion} face"

        input_ids = self.tokenizer(
            caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids[0]

        return {"pixel_values": pixel_values, "input_ids": input_ids}


def sfew_collate_fn(batch):
    pixel_values = torch.stack([example["pixel_values"] for example in batch])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}
