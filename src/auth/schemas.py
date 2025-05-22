# Imports de terceiros
from pydantic import BaseModel, EmailStr, Field


class UserAuth(BaseModel):
    """
    Schema para autenticação de usuário.
    """
    email: EmailStr = Field(..., description="E-mail Usuário")
    password: str = Field(
        ..., min_length=5, max_length=20, description="Senha Usuário"
    )

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True


class Token(BaseModel):
    """
    Schema para o token de autenticação.
    """
    access_token: str
    refresh_token: str

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True


class TokenPayload(BaseModel):
    """
    Schema para o payload do token.
    """
    sub: int = None
    exp: int = None

    class Config:
        """
        Configurações adicionais para o modelo.
        """
        from_attributes = True
