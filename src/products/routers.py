# Imports de terceiros
from typing import Annotated

from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session

# Imports locais
from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.products.crud import get_product_by_id
from src.products.models import ProductModel
from src.products.schemas import ProductOutput, ProductCreate
from pathlib import Path
from sqlalchemy.sql import func

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Raiz do projeto
IMAGES_DIR = BASE_DIR / "static" / "images"  # Diretório das imagens


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


@router.get("/get_products", summary="Listar todos os produtos, com suporte a paginação e filtros por categoria, preço e disponibilidade")
async def get_products(
        category: str = None,
        price: float = None,
        available: bool = None,
        page: int = 1,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    Obtém uma lista de produtos com suporte a paginação e filtros.

    Args:
        category (str): Categoria do produto.
        price (float): Preço do produto.
        available (bool): Disponibilidade do produto.
        page (int): Número da página.
        limit (int): Limite de produtos por página.
        db (Session): Sessão do banco de dados.
    Returns:
        list[ProductModel]: Lista de produtos filtrados e paginados.
    """
    products = db.query(ProductModel)

    if category:
        products = products.filter(ProductModel.section == category)

    if price:
        products = products.filter(ProductModel.price <= price)

    if available is not None:
        products = products.filter(ProductModel.stock > 0) if available else products.filter(ProductModel.stock == 0)

    products = products.offset((page - 1) * limit).limit(limit).all()

    return SuccessResponse(
        data=[ProductOutput(**product.__dict__) for product in products],
        message="Lista de produtos retornada com sucesso"
    )


@router.post("/create_product", summary="Criar um novo produto, contendo os seguintes atributos: descrição, valor de venda, código de barras, seção, estoque inicial, e data de validade (quando aplicável) e imagens.")
async def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db),
        arquivo: UploadFile = File(...)
):
    """
    Cria um novo produto.

    Args:
        product (ProductCreate): Dados do produto a ser criado.
        db (Session): Sessão do banco de dados.
        arquivo (UploadFile): Arquivo de imagem do produto.
    Returns:
        ProductModel: Instância do modelo de produto criado.
    """
    # Certifique-se de que o diretório de imagens existe
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Obtém o maior ID existente ou 0 se a tabela estiver vazia
    ultimo_id = db.query(func.max(ProductModel.id)).scalar() or 0

    # Evita sobreposição de arquivos com o mesmo nome
    arquivo.filename = f'{ultimo_id + 1}_{arquivo.filename}'

    # Constroi o caminho completo do arquivo
    caminho_arquivo = f'{IMAGES_DIR / arquivo.filename}'

    # Salva o arquivo no diretório de imagens
    with open(caminho_arquivo, "wb+") as objeto_arquivo:
        objeto_arquivo.write(arquivo.file.read())
    
    novo_produto = ProductModel(
        description=product.description,
        price=product.price,
        barcode=product.barcode,
        section=product.section,
        stock=product.stock,
        expiry_date=product.expiry_date,
        image_url=caminho_arquivo
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    print(novo_produto.__dict__)
    return SuccessResponse(
        data=None,
        message="Produto criado com sucesso"
    )
