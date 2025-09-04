from app.data.connection import engine
from sqlalchemy import text

selected_columns = [
    'id',
    'edad',
    'establecimiento_notificador',
    'centro_derivador',
    'localidad',
    'departamento',
    'fecha_recepcion',
    'fecha_procesamiento',
    'fecha_inicio_fiebre',
    'dias_evolucion',
    'ns1_elisa',
    'ns1_test_rapido',
    'ig_m_dengue_elisa',
    'ig_m_test_rapido',
    'igg_test_rapido',
    'rt_pcr_tiempo_real_dengue',
    'serotipo_virus_dengue',
    'created_at'
]

async def get_laboratorio_dengue_data():
    async with engine.connect() as connection:
        result = await connection.execute(text(f'SELECT {", ".join(selected_columns)} FROM laboratorio_dengue WHERE edad IS NOT NULL'))
        rows = result.fetchall()
        return rows