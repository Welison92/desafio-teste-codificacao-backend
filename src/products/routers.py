# Imports de terceiros
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

# Imports locais
from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.products.crud import get_product_by_id
from src.products.schemas import ProductOutput

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

@router.get("/get_detail_product/{product_id}", summary="Obter informações de um produto específico")
async def get_product(
        product_id: int,
        db: Session = Depends(get_db),
        # current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Obtém um produto pelo ID.

    Args:
        product_id (int): ID do produto.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        ProductModel: Instância do modelo de produto.
    """
    product = get_product_by_id(product_id, db)

    if not product:
        raise APIException(
            code=404,
            message="Produto não encontrado",
            description="O produto com o ID informado não foi encontrado"
        )

    return SuccessResponse(
        data=ProductOutput(**product.__dict__),
        message="Dados do produto retornado com sucesso"
    )