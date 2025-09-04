import fastapi
from app.data.connection import engine
from app.api.routes import router as api_router

app = fastapi.FastAPI()

app.add_event_handler('startup', engine.connect)
app.add_event_handler('shutdown', engine.dispose)

@app.get('/')
def read_root():
    return {'Hello': 'World'}

app.include_router(api_router)