import os

from torch.utils.data import ConcatDataset

from .affectnet import AffectNetDataset, affectnet_collate_fn
from .celeba_hq import CelebAHQDataset, celeba_hq_collate_fn
from .fetext import FETextDataset, fetex_collate_fn
from .ffhq import FFHQDataset, ffhq_collate_fn
from .raf_db import RAFDBDataset, raf_db_collate_fn
from .sfew import SFEWDataset, sfew_collate_fn

__all__ = [
    "AffectNetDataset",
    "affectnet_collate_fn",
    "CelebAHQDataset",
    "celeba_hq_collate_fn",
    "FETextDataset",
    "fetex_collate_fn",
    "FFHQDataset",
    "ffhq_collate_fn",
    "RAFDBDataset",
    "raf_db_collate_fn",
    "SFEWDataset",
    "sfew_collate_fn",
    "get_combined_dataset",
]


def get_combined_dataset(
    root_dir: str,
    tokenizer,
    transform=None,
    size: int = 512,
    split: str = "train",
):
    """
    Creates and returns a ConcatDataset combining all 6 datasets.
    root_dir is the path to the directory containing all the datasets.
    """
    datasets = []

    # AffectNet
    affectnet_path = os.path.join(root_dir, "AffectNet")
    if os.path.exists(affectnet_path):
        # AffectNet supports "train", "test", "both"
        aff_split = "test" if split == "val" else split
        datasets.append(AffectNetDataset(affectnet_path, tokenizer, transform, size, aff_split))

    # CelebA-HQ
    celeba_path = os.path.join(root_dir, "CelebA-HQ")
    if os.path.exists(celeba_path):
        # CelebA-HQ supports "train", "val", "both"
        datasets.append(CelebAHQDataset(celeba_path, tokenizer, transform, size, split))

    # FEText
    fetext_path = os.path.join(root_dir, "FEText")
    if os.path.exists(fetext_path):
        datasets.append(FETextDataset(fetext_path, tokenizer, transform, size, split))

    # FFHQ
    ffhq_path = os.path.join(root_dir, "FFHQ")
    if os.path.exists(ffhq_path):
        # FFHQ dataset doesn't have split
        datasets.append(FFHQDataset(ffhq_path, tokenizer, transform, size))

    # RAF-DB
    raf_db_path = os.path.join(root_dir, "RAF-DB")
    if os.path.exists(raf_db_path):
        # RAF-DB supports "train", "test", "both"
        raf_split = "test" if split == "val" else split
        datasets.append(RAFDBDataset(raf_db_path, tokenizer, transform, size, raf_split))

    # SFEW
    sfew_path = os.path.join(root_dir, "SFEW")
    if os.path.exists(sfew_path):
        # SFEW supports "train", "val", "both"
        datasets.append(SFEWDataset(sfew_path, tokenizer, transform, size, split))

    return ConcatDataset(datasets)
