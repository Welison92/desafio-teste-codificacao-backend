from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
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

    # Relacionamento com o cliente
    client = relationship("ClientModel", back_populates="orders")

    # Relacionamento com os itens do pedido
    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")


class OrderItemModel(Base):
    """
    Modelo de item de pedido para o banco de dados.
    """
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    # Relacionamento com o pedido e o produto
    order = relationship("OrderModel", back_populates="items")

    # Relacionamento com o produto
    product = relationship("ProductModel")
