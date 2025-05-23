from pydantic import BaseModel
from typing import List

from sqlalchemy import Enum


class OrderItem(BaseModel):
    """
    Schema para um item do pedido.
    """
    product_id: int
    quantity: int


class CreateOrder(BaseModel):
    """
    Schema para criação de um novo pedido.
    """
    client_id: int
    items: List[OrderItem]

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True


class StatusOrder(str, Enum):
    """
    Enumeração de status do pedido.
    """
    PENDENTE = "PENDENTE"
    ENTREGUE = "ENTREGUE"
    CANCELADO = "CANCELADO"

    @classmethod
    def list(cls):
        """
        Retorna uma lista com os valores dos status do pedido.
        """
        return [status.value for status in cls]
