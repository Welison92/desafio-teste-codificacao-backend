# Imports do sistema
from datetime import date
from typing import List, Optional

# Imports de terceiros
from pydantic import BaseModel


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
    url_images: List

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True
