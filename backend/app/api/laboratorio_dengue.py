from fastapi import APIRouter
from app.data.repositories.laboratorio_dengue_repository import get_laboratorio_dengue_data

router = APIRouter()

@router.get('/laboratorio-dengue')
async def laboratorio_dengue():
    rows = await get_laboratorio_dengue_data()
    return [dict(row._mapping) for row in rows]
