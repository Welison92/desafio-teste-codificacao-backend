# Imports do sistema
from typing import Optional

# Imports de terceiros
from pydantic import BaseModel, EmailStr, Field


class ClientCreate(BaseModel):
    """
    Schema para criação de um novo cliente.
    """
    name: str = Field(
        ..., min_length=3, max_length=20, description="Nome do cliente"
    )
    last_name: str = Field(
        ..., min_length=3, max_length=20, description="Sobrenome do cliente"
    )
    email: EmailStr = Field(
        ..., description="Email do cliente"
    )
    cpf: str = Field(
        ..., min_length=11, max_length=14, description="CPF do cliente"
    )
    phone: str = Field(
        ..., min_length=11, max_length=16, description="Telefone do cliente"
    )

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True


class ClientUpdate(BaseModel):
    """
    Schema para atualização de um cliente existente.
    """
    name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True


class ClientOutput(BaseModel):
    """
    Schema para saída de dados de um cliente.
    """
    id: int
    name: str
    last_name: str
    email: EmailStr
    cpf: str
    phone: str

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True
