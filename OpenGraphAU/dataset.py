from PIL import Image


def pil_loader(path):
    with open(path, "rb") as f:
        with Image.open(f) as img:
            return img.convert("RGB")
