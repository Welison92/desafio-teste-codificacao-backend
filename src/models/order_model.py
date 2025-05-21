from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base

class OrderModel(Base):
    """
    Modelo de pedido para o banco de dados.
    """
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)

    client = relationship("ClientModel", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

