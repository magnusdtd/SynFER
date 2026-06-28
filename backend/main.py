import contextlib
import os

import torch
import uvicorn
from diffusers import DDIMScheduler, StableDiffusionPipeline
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from OpenGraphAU.utils import image_eval
from src.evaluate_synfer import load_au_adapter, load_opengraphau_model, load_poster_v2

from .api.generate import router as generate_router
from .api.health import router as health_router
from .config import settings


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    print("[Main] Initializing backend system state...")

    print(f"[Main] Loading deep learning checkpoints on device: {settings.device}")

    device = torch.device(settings.device)
    weight_dtype = torch.float16 if settings.device == "cuda" else torch.bfloat16

    # 1. Load base Stable Diffusion Pipeline with memory optimizations
    pipe = StableDiffusionPipeline.from_pretrained(
        settings.base_model_dir,
        torch_dtype=weight_dtype,
        safety_checker=None,
        low_cpu_mem_usage=True,
    ).to(device)
    pipe.set_progress_bar_config(disable=True)
    pipe.enable_attention_slicing()

    # 2. Instantiate custom IP-Adapter processing structures on UNet
    au_proj_model = load_au_adapter(pipe.unet, settings.au_adapter_dir, device, weight_dtype)

    # 3. Load pre-trained OpenGraphAU and configuration
    og_model = load_opengraphau_model(device)
    og_transform = image_eval()

    # 4. Load POSTER++ classification models
    fer_model = load_poster_v2(device)

    # 5. Configure DDIM Scheduler for deterministic generation
    pipe.scheduler = DDIMScheduler.from_pretrained(settings.base_model_dir, subfolder="scheduler")

    # Store loaded states on FastAPI app state
    app.state.pipe = pipe
    app.state.au_proj_model = au_proj_model
    app.state.og_model = og_model
    app.state.fer_model = fer_model
    app.state.og_transform = og_transform

    # Ensure static directory exists
    os.makedirs(settings.static_dir, exist_ok=True)

    print("[Main] Backend system state initialized successfully!")
    yield

    print("[Main] Shutting down backend system...")


app = FastAPI(
    title="SynFER Backend API",
    description="FastAPI backend designed to serve SynFER framework for facial expression synthesis.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static serving
os.makedirs(settings.static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

# Mount API endpoints
app.include_router(health_router, prefix="/api")
app.include_router(generate_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=settings.host, port=settings.port, reload=False)
