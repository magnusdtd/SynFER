from pathlib import Path

from huggingface_hub import snapshot_download

save_dir = Path("datasets/FEText")
save_dir.mkdir(parents=True, exist_ok=True)

local_path = snapshot_download(
    repo_id="connorxian/aff_sup",
    repo_type="dataset",
    local_dir=save_dir,
)
print(f"Downloaded to: {local_path}")
