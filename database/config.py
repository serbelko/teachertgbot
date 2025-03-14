from dotenv import load_dotenv
from pydantic_settings import BaseSettings  # Используем правильный импорт
import os

class Config(BaseSettings):
    load_dotenv()
    
    PORT: int = int(os.getenv("POSTGRES_PORT", 5433))
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "2284")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "test15")

config = Config()
