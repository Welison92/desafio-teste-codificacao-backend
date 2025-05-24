from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from core.database import Base


class ProductModel(Base):
    """
    Modelo de produto para o banco de dados.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    barcode = Column(String, unique=True, nullable=False)
    section = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    expiry_date = Column(Date, nullable=True)

    # Relacionamento com a tabela de imagens
    images = relationship(
        "ProductImageModel",
        back_populates="product",
        cascade="all, delete-orphan"
    )


class ProductImageModel(Base):
    """
    Modelo para imagens associadas a um produto.
    """
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    image_url = Column(String, nullable=False)

    # Relacionamento com o modelo de produto
    product = relationship("ProductModel", back_populates="images")
