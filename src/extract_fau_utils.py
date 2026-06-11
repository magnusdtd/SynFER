import argparse
import os

from PIL import Image
from torch.utils.data import Dataset


class OpenGraphAUDataset(Dataset):
    def __init__(self, hf_dataset, transform, images_dir):
        self.dataset = hf_dataset
        self.transform = transform
        self.images_dir = images_dir
        os.makedirs(self.images_dir, exist_ok=True)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        item = self.dataset[idx]
        image = item["image"]
        if not isinstance(image, Image.Image):
            image = Image.open(image).convert("RGB")
        else:
            image = image.convert("RGB")

        # Get base name for the image
        image_path = item.get("image_path", None)
        if image_path:
            base_name = os.path.basename(image_path)
        else:
            base_name = f"{idx:05d}.png"

        # Save image to disk if it doesn't exist already
        save_path = os.path.join(self.images_dir, base_name)
        if not os.path.exists(save_path):
            image.save(save_path)

        # Preprocess image for OpenGraphAU model
        tensor_img = self.transform(image)
        caption = item.get("caption", "")

        return {
            "tensor": tensor_img,
            "base_name": base_name,
            "caption": caption,
        }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract FEText images, captions, and predict FAUs using OpenGraphAU.",
    )
    parser.add_argument(
        "--parquet_pattern",
        type=str,
        default="datasets/FEText/data/train-*.parquet",
        help="Glob pattern matching FEText parquet files.",
    )
    parser.add_argument(
        "--arc",
        type=str,
        default="resnet50",
        choices=["resnet50", "swin_transformer_tiny"],
        help="Backbone architecture for OpenGraphAU.",
    )
    parser.add_argument(
        "--resume",
        type=str,
        default="models/OpenGraphAU/OpenGprahAU-ResNet50_second_stage.pth",
        help="Path to the checkpoint to load.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="datasets/FEText",
        help="Directory to save extracted images, captions.json, and fau_labels.json.",
    )
    parser.add_argument("--batch_size", type=int, default=64, help="Inference batch size.")
    parser.add_argument("--num_workers", type=int, default=4, help="DataLoader number of workers.")
    parser.add_argument(
        "--limit", type=int, default=-1, help="Limit number of samples to process (for testing). -1 means no limit."
    )
    args = parser.parse_args()
    return args
