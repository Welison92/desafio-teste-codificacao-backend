from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class ProductCreate(BaseModel):
    description: str = Field(
        ..., min_length=20, max_length=50, description="Descrição do produto"
    )
    price: float = Field(
        ..., description="Preço do produto"
    )
    barcode: str = Field(
        ..., description="Código de barras do produto"
    )
    section: str = Field(
        ..., description="Seção do produto"
    )
    stock: int = Field(
        ..., description="Quantidade em estoque do produto"
    )
    expiry_date: Optional[date] = Field(
        None, description="Data de validade do produto"
    )

    class Config:
        from_attributes = True


class ProductUpdate(BaseModel):
    description: Optional[str] = None
    price: Optional[float] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    expiry_date: Optional[date] = None
    image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ProductOutput(BaseModel):
    id: int
    description: str
    price: float
    barcode: str
    section: str
    stock: int
    expiry_date: Optional[date]
    image_url: str

    class Config:
        from_attributes = True
