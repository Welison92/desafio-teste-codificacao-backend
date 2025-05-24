# Imports de terceiros
from sqlalchemy.orm import Session, joinedload

# Imports locais
from src.orders.models import OrderModel


def get_order_by_id(order_id: int, db: Session):
    """
    Obtém um pedido pelo ID.

    Args:
        order_id (int): O ID do pedido a ser obtido.
        db (Session): A sessão do banco de dados.
    Returns:
        OrderModel: O pedido correspondente ao ID fornecido.
    """
    return db.query(OrderModel).filter(OrderModel.id == order_id).first()


def get_order_detail_by_id(order_id: int, db: Session):
    """
    Obtém os detalhes de um pedido pelo ID.

    Args:
        order_id (int): O ID do pedido a ser obtido.
        db (Session): A sessão do banco de dados.
    Returns:
        OrderModel: O pedido correspondente ao ID fornecido,
        incluindo os itens do pedido.
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

    Args:
        db (Session): A sessão do banco de dados.
    Returns:
        list[OrderModel]: Uma lista de todos os pedidos,
        incluindo os itens do pedido.
    """
    return (
        db.query(OrderModel)
        .options(joinedload(OrderModel.items))
        .all()
    )
