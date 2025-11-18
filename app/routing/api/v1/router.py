from fastapi import APIRouter
from .endpoints.minecraft import router as minecraft_router

router = APIRouter()
router.include_router(minecraft_router)
