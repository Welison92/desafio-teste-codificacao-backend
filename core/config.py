# Imports do sistema
import os

# Imports de terceiros
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carregando as variáveis de ambiente do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '../env/.env'))


class Settings(BaseSettings):
    # Development
    DEBUG: bool = False

    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")

    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT")
    DATABASE_URL: str = os.getenv("DATABASE_URL",
                                  f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
                                  f"{DATABASE_HOST}:{DATABASE_PORT}/{POSTGRES_DB}"
                                  )

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '../env/.env')
        env_file_encoding = 'utf-8'


settings = Settings()
