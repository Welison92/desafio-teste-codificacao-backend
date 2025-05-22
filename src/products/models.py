from sqlalchemy import Column, Integer, String, Float, Date
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
    image_url = Column(String, nullable=False)
