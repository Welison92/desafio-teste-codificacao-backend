# Imports do sistema
from typing import Generic, List, Optional, TypeVar, Union

# Imports de terceiros
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T', bound=BaseModel)


class APIException(Exception):
    """
        Execption para tratamento de erros na API
    """
    def __init__(
            self, status: str = "error", message: str = "",
            code: int = 500, description: str = ""
    ):
        self.status: str = status
        self.message: str = message
        self.code: int = code
        self.description: str = description
        self.data: Optional[Union[T, List[T], List[str], None, dict]] = {}


class SuccessResponse(GenericModel, Generic[T]):
    """
        Modelo de resposta de sucesso da API
    """
    status: str = "success"
    data: Optional[Union[T, None, List[T], List[str]]] = None
    message: str = "Requisição bem-sucedida."
