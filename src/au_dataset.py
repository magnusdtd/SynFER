import json
import os
import random

import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from transformers import CLIPImageProcessor

from .utils import logger


class MyDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        json_file_path: str,
        tokenizer,
        size: int = 512,
        t_drop_rate: float = 0.05,
        i_drop_rate: float = 0.05,
        ti_drop_rate: float = 0.05,
        image_root_path: str = "",
    ):
        super().__init__()

        self.tokenizer = tokenizer
        self.size = size
        self.i_drop_rate = i_drop_rate
        self.t_drop_rate = t_drop_rate
        self.ti_drop_rate = ti_drop_rate
        self.image_root_path = image_root_path

        self.data = json.load(open(json_file_path))  # list of dict: [{"image_file": "1.png", "text": "A dog"}]

        self.transform = transforms.Compose(
            [
                transforms.Resize(self.size, interpolation=transforms.InterpolationMode.BILINEAR),
                transforms.CenterCrop(self.size),
                transforms.ToTensor(),
                transforms.Normalize([0.5], [0.5]),
            ]
        )
        self.clip_image_processor = CLIPImageProcessor()

    def __getitem__(self, idx):
        item = self.data[idx]
        text = item["text"]
        image_file = item["image_file"]

        # read image
        raw_image = Image.open(os.path.join(self.image_root_path, image_file))
        image = self.transform(raw_image.convert("RGB"))
        clip_image = self.clip_image_processor(images=raw_image, return_tensors="pt").pixel_values

        # drop
        drop_image_embed = 0
        rand_num = random.random()
        if rand_num < self.i_drop_rate:
            drop_image_embed = 1
        elif rand_num < (self.i_drop_rate + self.t_drop_rate):
            text = ""
        elif rand_num < (self.i_drop_rate + self.t_drop_rate + self.ti_drop_rate):
            text = ""
            drop_image_embed = 1

        # get text and tokenize
        text_input_ids = self.tokenizer(
            text,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids

        return {
            "image": image,
            "text_input_ids": text_input_ids,
            "clip_image": clip_image,
            "drop_image_embed": drop_image_embed,
        }

    def __len__(self):
        return len(self.data)


class HybridDataset(torch.utils.data.Dataset):
    def __init__(
        self,
        img_file_list: list,
        txt_file_list: list,
        au_file_list: list,
        tokenizer,
        t_drop_rate: float = 0.05,
        size: int = 512,
    ):
        self.img_path = []
        self.captions = []
        self.au_list = []

        self.tokenizer = tokenizer
        self.t_drop_rate = t_drop_rate
        self.size = size

        self.transform = transforms.Compose(
            [
                transforms.Resize(self.size, interpolation=transforms.InterpolationMode.BILINEAR),
                transforms.CenterCrop(self.size),
                transforms.ToTensor(),
                transforms.Normalize([0.5], [0.5]),
            ]
        )
        self.to_tensor = transforms.ToTensor()

        for img_folder, caption_path, au_path in zip(img_file_list, txt_file_list, au_file_list):
            au_labels = json.load(open(au_path))
            if caption_path is not None:
                captions = json.load(open(caption_path))

                for i in range(len(captions)):
                    k = list(captions[i].keys())[0]
                    img_path = os.path.join(img_folder, k.split("/")[-1])
                    v = captions[i][k]

                    try:
                        au_label = au_labels[k.split("/")[-1]]
                        au_label = np.array(au_label.split(), dtype=int)

                        self.img_path.append(img_path)
                        self.captions.append(v)
                        self.au_list.append(au_label)
                    except Exception:
                        pass
            else:
                for au_k in au_labels.keys():
                    img_path = os.path.join(img_folder, au_k)
                    text = ""
                    au_label = au_labels[au_k]
                    au_label = np.array(au_label.split(), dtype=int)

                    self.img_path.append(img_path)
                    self.captions.append(text)
                    self.au_list.append(au_label)

        random_indices = np.random.choice(len(self.img_path), size=int(len(self.img_path)), replace=False)
        self.img_path = [self.img_path[i] for i in random_indices]
        self.captions = [self.captions[i] for i in random_indices]
        self.au_list = [self.au_list[i] for i in random_indices]
        logger.info(f"Total training images cnt: {len(self.img_path)}")

    def __len__(self):
        return len(self.img_path)

    def __getitem__(self, idx):
        img_path = self.img_path[idx]
        img = Image.open(img_path)
        img = self.transform(img)

        rand_num = random.random()
        if rand_num < self.t_drop_rate:
            caption = ""
        else:
            caption = self.captions[idx]

        caption = self.tokenizer(
            caption,
            max_length=self.tokenizer.model_max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        ).input_ids

        au_label = self.au_list[idx]
        au_label = torch.from_numpy(au_label)
        au_label = au_label.unsqueeze(dim=0)  # .unsqueeze(dim=0)

        return dict(image=img, text=caption, au_label=au_label)


def collate_fn(data):
    images = torch.stack([example["image"] for example in data])
    text_input_ids = torch.cat([example["text_input_ids"] for example in data], dim=0)
    clip_images = torch.cat([example["clip_image"] for example in data], dim=0)
    drop_image_embeds = [example["drop_image_embed"] for example in data]

    return {
        "images": images,
        "text_input_ids": text_input_ids,
        "clip_images": clip_images,
        "drop_image_embeds": drop_image_embeds,
    }


def au_collate_fn(data):
    images = torch.stack([example["image"] for example in data])
    text_input_ids = torch.cat([example["text"] for example in data], dim=0)
    au_labels = torch.cat([example["au_label"] for example in data], dim=0)

    return {
        "images": images,
        "text_input_ids": text_input_ids,
        "au_label": au_labels,
    }
