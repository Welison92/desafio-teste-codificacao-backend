from sqlalchemy.orm import Session

from src.products.models import ProductModel


def get_product_by_id(product_id: int, db: Session):
    """
    Obtém um produto pelo ID.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()


def get_product_by_barcode(barcode: str, db: Session):
    """
    Obtém um produto pelo código de barras.
    """
    return db.query(ProductModel).filter(ProductModel.barcode == barcode).first()