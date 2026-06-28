from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def get_health():
    # Check something here, like DB connection, ...abs
    return {"backend": "ok"}