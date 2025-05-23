from pydantic import BaseModel
from typing import List

from enum import Enum


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


class UpdateOrder(BaseModel):
    """
    Schema para atualização de um pedido existente.
    """
    items: List[OrderItem] = None

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True


class OrderOutput(BaseModel):
    """
    Schema para a saída de um pedido.
    """
    id: int
    client_id: int
    status: str
    created_at: str
    items: List[OrderItem]
    total_itens: int
    total_price: float

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
