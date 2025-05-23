from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.clients.crud import get_client_by_id
from src.clients.models import ClientModel
from src.orders.models import OrderModel, OrderItemModel
from src.orders.schemas import CreateOrder, StatusOrder
from src.products.crud import get_product_by_id
from src.products.models import ProductModel

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create_order", summary="Criar um novo pedido com itens")
def create_order(order: CreateOrder, db: Session = Depends(get_db)):
    # Validar se o cliente existe (não mostrado aqui para simplicidade)

    # Validar estoque disponível
    for item in order.items:
        product = get_product_by_id(item.product_id, db)

        if not product:
            raise APIException(
                code=404,
                message="Produto não encontrado",
                description=f"Produto com id {item.product_id} não encontrado"
            )
        if product.stock < item.quantity:
            raise APIException(
                code=400,
                message="Estoque insuficiente",
                description=f"Produto {product.name} não tem estoque suficiente. "
                            f"Disponível: {product.stock}, Solicitado: {item.quantity}"
            )

    # Criar pedido e itens
    # new_order = OrderModel(client_id=order.client_id, status="pending", created_at=datetime.now())
    new_order = OrderModel(
        client_id=order.client_id,
        status=StatusOrder.PENDENTE,
        created_at=datetime.now()
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    for item in order.items:
        order_item = OrderItemModel(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=get_product_by_id(item.product_id, db).price
        )
        db.add(order_item)

        # Atualizar estoque
        product = get_product_by_id(item.product_id, db)
        product.stock -= item.quantity
        db.add(product)

    db.commit()

    return SuccessResponse(
        data=None,
        message="Pedido criado com sucesso"
    )
