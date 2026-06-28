import torch
from pydantic import BaseModel


class SystemSettings(BaseModel):
    base_model_dir: str = "outputs/sd-fetext-model-lora"
    au_adapter_dir: str = "outputs/sd-fetext-model-au-adapter"
    opengraphau_checkpoint: str = "models/OpenGraphAU/OpenGprahAU-ResNet50_second_stage.pth"
    poster_checkpoint: str = "models/POSTER_V2/affectnet-8-model_best.pth"
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    static_dir: str = "backend/static"
    port: int = 8000
    host: str = "0.0.0.0"

    num_inference_steps: int = 50
    invert_steps: int = 35
    sg_start_step: int = 15
    sg_step_size: float = 0.1
    guidance_scale: float = 7.5
    seed: int = 3407


settings = SystemSettings()
