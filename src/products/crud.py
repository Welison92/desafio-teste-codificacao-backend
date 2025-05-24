# Imports de terceiros
from sqlalchemy.orm import Session

# Imports locais
from src.products.models import ProductModel


def get_product_by_id(product_id: int, db: Session):
    """
    Obtém um produto pelo ID.

    Args:
        product_id (int): O ID do produto a ser obtido.
        db (Session): A sessão do banco de dados.
    Returns:
        ProductModel: O produto correspondente ao ID fornecido.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_product_by_barcode(barcode: str, db: Session):
    """
    Obtém um produto pelo código de barras.

    Args:
        barcode (str): O código de barras do produto a ser obtido.
        db (Session): A sessão do banco de dados.
    Returns:
        ProductModel: O produto correspondente ao código de barras fornecido.
    """
    return db.query(ProductModel).filter(
        ProductModel.barcode == barcode
    ).first()
