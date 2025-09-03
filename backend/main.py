import fastapi
from app.data.connection import engine
from app.data.repositories.laboratorio_dengue_repository import get_laboratorio_dengue_data
import asyncio

app = fastapi.FastAPI()

app.add_event_handler('startup', engine.connect)
app.add_event_handler('shutdown', engine.dispose)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

@app.get('/laboratorio-dengue')
async def laboratorio_dengue():
    rows = await get_laboratorio_dengue_data()
    # Convert SQLAlchemy Row objects to dicts
    return [dict(row._mapping) for row in rows]