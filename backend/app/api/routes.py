from fastapi import APIRouter
from app.api.laboratorio_dengue import router as laboratorio_dengue_router

router = APIRouter()
router.include_router(laboratorio_dengue_router)
