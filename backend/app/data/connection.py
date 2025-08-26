from sqlalchemy import create_engine, URL, text
from app.core.config import settings

username = settings.DB_USERNAME
password = settings.DB_PASSWORD
host = settings.DB_HOST
port = settings.DB_PORT
database = settings.DB_NAME

url = URL.create(
    drivername='mysql+pymysql',
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.all())