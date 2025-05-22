from typing import Optional
from pydantic import BaseModel, Field
from datetime import date


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
