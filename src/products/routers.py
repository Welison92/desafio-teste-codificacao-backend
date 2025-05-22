# Imports de terceiros
from typing import Annotated

from fastapi import APIRouter, UploadFile, File
from fastapi.params import Depends
from sqlalchemy.orm import Session

# Imports locais
from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.auth.jwt_auth import get_current_user
from src.clients.models import ClientModel
from src.products.crud import get_product_by_id, get_product_by_barcode
from src.products.models import ProductModel
from src.products.schemas import ProductOutput
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
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Obtém um produto pelo ID.

    Args:
        product_id (int): ID do produto.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        ProductOutput: Detalhes do produto.
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
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
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
        current_user (ClientModel): Cliente autenticado.
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
        description : str,
        price : float,
        barcode : str,
        section : str,
        stock : int,
        expiry_date : str = None,
        db: Session = Depends(get_db),
        arquivo: UploadFile = File(...),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Cria um novo produto.

    Args:
        description (str): Descrição do produto.
        price (float): Preço do produto.
        barcode (str): Código de barras do produto.
        section (str): Seção do produto.
        stock (int): Estoque inicial do produto.
        expiry_date (str): Data de validade do produto (opcional).
        db (Session): Sessão do banco de dados.
        arquivo (UploadFile): Arquivo da imagem do produto.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso.
    """
    barcode_model = get_product_by_barcode(barcode, db)

    if barcode_model:
        raise APIException(
            code=400,
            message="Código de barras já cadastrado",
            description="O código de barras informado já está cadastrado no sistema"
        )

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
        description=description,
        price=price,
        barcode=barcode,
        section=section,
        stock=stock,
        expiry_date=expiry_date,
        image_url=caminho_arquivo
    )

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return SuccessResponse(
        data=None,
        message="Produto criado com sucesso"
    )


@router.put("/update_product/{product_id}", summary="Atualizar informações de um produto específico")
async def update_product(
        product_id: int,
        description: str = None,
        price: float = None,
        barcode: str = None,
        section: str = None,
        stock: int = None,
        expiry_date: str = None,
        db: Session = Depends(get_db),
        arquivo: UploadFile = File(None),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Atualiza um produto existente.

    Args:
        product_id (int): ID do produto a ser atualizado.
        description (str): Nova descrição do produto (opcional).
        price (float): Novo preço do produto (opcional).
        barcode (str): Novo código de barras do produto (opcional).
        section (str): Nova seção do produto (opcional).
        stock (int): Novo estoque do produto (opcional).
        expiry_date (str): Nova data de validade do produto (opcional).
        db (Session): Sessão do banco de dados.
        arquivo (UploadFile): Novo arquivo da imagem do produto (opcional).
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso.
    """
    product = get_product_by_id(product_id, db)

    if not product:
        raise APIException(
            code=404,
            message="Produto não encontrado",
            description="O produto com o ID informado não foi encontrado"
        )

    if description:
        product.description = description

    if price:
        product.price = price

    if barcode:
        barcode_model = get_product_by_barcode(barcode, db)

        if barcode_model:
            raise APIException(
                code=400,
                message="Código de barras já cadastrado",
                description="O código de barras informado já está cadastrado no sistema"
            )

        product.barcode = barcode

    if section:
        product.section = section

    if stock:
        product.stock = stock

    if expiry_date:
        product.expiry_date = expiry_date

    if arquivo:
        # Evita sobreposição de arquivos com o mesmo nome
        arquivo.filename = f'{product_id}_{arquivo.filename}'

        # Constroi o caminho completo do arquivo
        caminho_arquivo = f'{IMAGES_DIR / arquivo.filename}'

        with open(caminho_arquivo, "wb+") as objeto_arquivo:
            objeto_arquivo.write(arquivo.file.read())

        # Deleta o arquivo antigo se existir
        if Path(product.image_url).exists():
            Path(product.image_url).unlink()

        # Atualiza a URL da imagem no banco de dados
        product.image_url = caminho_arquivo

    db.commit()
    db.refresh(product)

    return SuccessResponse(
        data=None,
        message="Produto atualizado com sucesso"
    )


@router.delete("/delete_product/{product_id}", summary="Excluir um produto")
async def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Exclui um produto existente.

    Args:
        product_id (int): ID do produto a ser excluído.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso.
    """
    product = get_product_by_id(product_id, db)

    if not product:
        raise APIException(
            code=404,
            message="Produto não encontrado",
            description="O produto com o ID informado não foi encontrado"
        )

    # Deleta o arquivo da imagem se existir
    if Path(product.image_url).exists():
        Path(product.image_url).unlink()

    db.delete(product)
    db.commit()

    return SuccessResponse(
        data=None,
        message="Produto excluído com sucesso"
    )
