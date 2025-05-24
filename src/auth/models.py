from sqlalchemy import Column, Integer, String
from core.database import Base
import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class UserModel(Base):
    """
    Modelo de usuário para o banco de dados.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    # role = Column(Enum(UserRole), default=UserRole.USER)
