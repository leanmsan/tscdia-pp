import os
import dotenv

dotenv.load_dotenv()

class Settings:
    DB_USERNAME: str = os.getenv('DB_USERNAME')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: int = os.getenv('DB_PORT')
    DB_NAME: str = os.getenv('DB_NAME')


settings = Settings()