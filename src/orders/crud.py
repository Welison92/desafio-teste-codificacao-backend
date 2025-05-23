from sqlalchemy.orm import Session, joinedload

from src.orders.models import OrderModel


def get_order_by_id(order_id: int, db: Session):
    """
    Obtém um pedido pelo ID.
    """
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()


def get_order_detail_by_id(order_id: int, db: Session):
    """
    Obtém os detalhes de um pedido pelo ID.
    """
    return (
        db.query(OrderModel)
        .options(joinedload(OrderModel.items))
        .filter(OrderModel.id == order_id)
        .first()
    )


def get_all_orders_detail(db: Session):
    """
    Obtém todos os pedidos com detalhes.
    """
    return (
        db.query(OrderModel)
        .options(joinedload(OrderModel.items))
        .all()
    )
