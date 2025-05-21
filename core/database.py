# Imports de terceiros
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Imports locais
from core.config import settings

# Criar o engine de conexão
engine = create_engine(settings.DATABASE_URL)

# Criar uma fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


# Função para obter uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
