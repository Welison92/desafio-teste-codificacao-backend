# Imports do sistema
import os

# Imports de terceiros
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Carregando as variáveis de ambiente do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '../env/.env'))


class Settings(BaseSettings):
    """
    Configurações do projeto.
    """
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

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_REFRESH_SECRET_KEY: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # 30 minutos
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 dias

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '../env/.env')
        env_file_encoding = 'utf-8'


settings = Settings()
