from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.engine.url import URL
from sqlalchemy import text
from app.core.config import settings

username = settings.DB_USERNAME
password = settings.DB_PASSWORD
host = settings.DB_HOST
port = settings.DB_PORT
database = settings.DB_NAME

url = URL.create(
    drivername='mysql+aiomysql',
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_async_engine(url)