from sqlalchemy.orm import Session

from src.products.models import ProductModel


def get_product_by_id(product_id: int, db: Session):
    """
    Get a product by its ID.
    """
    return db.query(ProductModel).filter(ProductModel.id == product_id).first()



