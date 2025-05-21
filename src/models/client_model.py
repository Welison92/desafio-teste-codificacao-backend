from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from core.database import Base

class ClientModel(Base):
    """
    Modelo de cliente para o banco de dados.
    """
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)

    orders = relationship("Order", back_populates="client", cascade="all, delete-orphan")