from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


class ProductOutput(BaseModel):
    """
    Modelo de saída para produtos.
    """
    id: int
    description: str
    price: float
    barcode: str
    section: str
    stock: int
    expiry_date: Optional[date]
    image_url: str

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True
