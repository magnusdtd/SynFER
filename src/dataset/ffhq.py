import os

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms


class FFHQDataset(Dataset):
    def __init__(
        self,
        root_dir: str,
        tokenizer,
        transform=None,
        size: int = 512,
        default_caption: str = "a photo of a face",
    ):
        self.root_dir = root_dir
        self.tokenizer = tokenizer
        self.size = size
        self.default_caption = default_caption

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
        if os.path.exists(root_dir):
            for fname in os.listdir(root_dir):
                if fname.lower().endswith((".png", ".jpg", ".jpeg")):
                    self.samples.append(os.path.join(root_dir, fname))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        pixel_values = self.transform(image)

        input_ids = self.tokenizer(
            self.default_caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids[0]

        return {"pixel_values": pixel_values, "input_ids": input_ids}


def ffhq_collate_fn(batch):
    pixel_values = torch.stack([example["pixel_values"] for example in batch])
    pixel_values = pixel_values.to(memory_format=torch.contiguous_format).float()
    input_ids = torch.stack([example["input_ids"] for example in batch])
    return {"pixel_values": pixel_values, "input_ids": input_ids}
