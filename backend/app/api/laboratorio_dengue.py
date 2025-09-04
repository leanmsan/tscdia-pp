from fastapi import APIRouter
from app.services.laboratorio_dengue_service import LaboratorioDengueService

router = APIRouter()

# Instancia del servicio
service = LaboratorioDengueService(max_workers=4, chunk_size=500)

@router.get('/laboratorio-dengue/raw')
async def laboratorio_dengue_raw():
    """Obtiene datos raw sin procesar."""
    return await service.obtener_datos_raw()

@router.get('/laboratorio-dengue/procesados')
async def laboratorio_dengue_procesados():
    """Obtiene datos procesados y normalizados usando Polars y ProcessPoolExecutor."""
    return await service.obtener_datos_procesados()

@router.get('/laboratorio-dengue/kpis')
async def laboratorio_dengue_kpis():
    """Obtiene KPIs básicos calculados sobre los datos procesados."""
    return await service.obtener_kpis_basicos()
