# Imports do sistema
from datetime import datetime, timedelta
from typing import Annotated, Optional

# Imports de terceiros
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# Imports locais
from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.auth.jwt_auth import get_current_user
from src.clients.models import ClientModel
from src.orders.crud import (get_all_orders_detail, get_order_by_id,
                             get_order_detail_by_id)
from src.orders.models import OrderItemModel, OrderModel
from src.orders.schemas import (CreateOrder, OrderItem, OrderOutput,
                                StatusOrder, UpdateOrder)
from src.products.crud import get_product_by_id

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/get_detail_order/{order_id}",
    summary="Obter informações de um pedido específico"
)
def get_order(
        order_id: int, db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Obtém um pedido pelo ID.

    Args:
        order_id (int): ID do pedido.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        OrderOutput: Detalhes do pedido.
    """
    order = get_order_detail_by_id(order_id, db)

    # Verifica se o pedido existe
    if not order:
        raise APIException(
            code=404,
            message="Pedido não encontrado",
            description=f"O pedido com o ID {order_id} não foi encontrado"
        )

    # Calcular o total de itens e o preço total do pedido
    total_itens = sum(item.quantity for item in order.items)
    total_price = sum(item.quantity * item.unit_price for item in order.items)

    # Cria o objeto de saída com os detalhes do pedido
    order_output = OrderOutput(
        id=order.id,
        client_id=order.client_id,
        status=order.status,
        created_at=str(order.created_at),
        items=[OrderItem(**item.__dict__) for item in order.items],
        total_itens=total_itens,
        total_price=total_price
    )

    return SuccessResponse(
        data=order_output,
        message="Dados do pedido retornado com sucesso"
    )


@router.get(
    "/get_orders",
    summary="Listar todos os pedidos, incluindo os seguintes "
            "filtros: período, seção dos produtos, id_pedido, "
            "status do pedido e cliente"
)
def get_orders(
        order_id: int = None,
        client_id: int = None,
        status: Optional[StatusOrder] = None,
        category: str = None,
        start_date: str = None,
        end_date: str = None,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Obtém todos os pedidos com detalhes.

    Args:
        order_id (int): ID do pedido (opcional).
        client_id (int): ID do cliente (opcional).
        status (StatusOrder): Status do pedido (opcional).
        category (str): Categoria do produto (opcional).
        start_date (str): Data de início no formato YYYY-MM-DD (opcional).
        end_date (str): Data de término no formato YYYY-MM-DD (opcional).
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        List[OrderOutput]: Lista de pedidos com detalhes.
    """
    orders = get_all_orders_detail(db)

    # Verifica se há pedidos
    if not orders:
        raise APIException(
            code=404,
            message="Nenhum pedido encontrado",
            description="Nenhum pedido encontrado no sistema"
        )

    if order_id:
        orders = [order for order in orders if order.id == order_id]

        if not orders:
            raise APIException(
                code=404,
                message="Pedido não encontrado",
                description=f"Pedido com ID {order_id} não foi encontrado"
            )

    if client_id:
        orders = [order for order in orders if order.client_id == client_id]

        if not orders:
            raise APIException(
                code=404,
                message="Cliente não encontrado",
                description=f"Cliente com ID {client_id} não foi encontrado"
            )

    if status:
        orders = [order for order in orders if order.status == status]

        if not orders:
            raise APIException(
                code=404,
                message="Pedido não encontrado",
                description=f"Pedido com status {status} não foi encontrado"
            )

    if category:
        orders = [
            order for order in orders
            if any(
                item.product.section.upper() == category.upper()
                for item in order.items
            )
                  ]

        if not orders:
            raise APIException(
                code=404,
                message="Nenhum pedido encontrado",
                description=f"Nenhum pedido encontrado para "
                            f"a categoria {category}"
            )

    # Verifica se as datas de início e término foram fornecidas
    if start_date or end_date:
        try:
            filtered_orders = []
            # Converter start_date para datetime, se fornecida
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d") \
                if start_date else None

            # Converter end_date para datetime, incluindo o final do dia,
            # se fornecida
            end_datetime = (datetime.strptime(end_date, "%Y-%m-%d")
                            + timedelta(days=1)
                            - timedelta(seconds=1)) if end_date else None

            for order in orders:
                include_order = True
                # Filtro por start_date
                if start_datetime and order.created_at < start_datetime:
                    include_order = False
                # Filtro por end_date
                if end_datetime and order.created_at > end_datetime:
                    include_order = False
                if include_order:
                    filtered_orders.append(order)

            orders = filtered_orders

            if not orders:
                raise APIException(
                    code=404,
                    message="Nenhum pedido encontrado",
                    description=f"Nenhum pedido encontrado "
                                f"entre as datas {start_date} e {end_date}"
                )
        except ValueError:
            raise APIException(
                code=400,
                message="Formato de data inválido",
                description="As datas devem estar no formato YYYY-MM-DD"
            )

    # Calcular o total de itens e o preço total de cada pedido
    for order in orders:
        total_itens = sum(item.quantity for item in order.items)
        total_price = sum(
            item.quantity * item.unit_price for item in order.items
        )

        order.total_itens = total_itens
        order.total_price = total_price

    # Criar a lista de pedidos com os detalhes
    orders = [
        OrderOutput(
            id=order.id,
            client_id=order.client_id,
            status=order.status,
            created_at=str(order.created_at),
            items=[OrderItem(**item.__dict__) for item in order.items],
            total_itens=order.total_itens,
            total_price=order.total_price
        )
        for order in orders
    ]

    return SuccessResponse(
        data=orders,
        message="Pedidos retornado com sucesso"
    )


@router.post("/create_order", summary="Criar um novo pedido com itens")
def create_order(
        order: CreateOrder, db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Cria um novo pedido com itens.

    Args:
        order (CreateOrder): Dados do pedido a ser criado.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados do pedido criado.
    """
    # Validar estoque disponível
    for item in order.items:
        product = get_product_by_id(item.product_id, db)

        # Verifica se o produto existe
        if not product:
            raise APIException(
                code=404,
                message="Produto não encontrado",
                description=f"Produto com ID {item.product_id} não "
                            f"foi encontrado"
            )

        # Verifica se o estoque é suficiente
        if product.stock < item.quantity:
            raise APIException(
                code=400,
                message="Estoque insuficiente",
                description=f"Produto com ID {product.id} não tem estoque "
                            f"suficiente. Disponível: {product.stock}, "
                            f"Solicitado: {item.quantity}"
            )

    # Cria o modelo do pedido
    new_order = OrderModel(
        client_id=current_user.id,
        status=StatusOrder.PENDENTE,
        created_at=datetime.now()
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    # Cria os itens do pedido
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


@router.put(
    "/update_order/{order_id}",
    summary="Atualizar um pedido existente"
)
def update_order(
        order_id: int,
        order: UpdateOrder = None,
        status: StatusOrder = None,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Atualiza um pedido existente.

    Args:
        order_id (int): ID do pedido a ser atualizado.
        order (UpdateOrder): Dados do pedido a serem atualizados.
        status (StatusOrder): Novo status do pedido (opcional).
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados do pedido atualizado.
    """
    order_model = get_order_by_id(order_id, db)

    # Verifica se o pedido existe
    if not order_model:
        raise APIException(
            code=404,
            message="Pedido não encontrado",
            description=f"Pedido com ID {order_id} não foi encontrado"
        )

    # Verifica se o pedido pertence ao cliente autenticado
    if order_model.client_id != current_user.id:
        raise APIException(
            code=403,
            message="Acesso negado",
            description="Você não tem permissão para atualizar este pedido"
        )

    if status:
        if status == StatusOrder.ENTREGUE:
            db.delete(order_model)
            db.commit()
        elif status == StatusOrder.CANCELADO:
            # Reverter o estoque dos itens do pedido
            for item in order_model.items:
                product = get_product_by_id(item.product_id, db)
                product.stock += item.quantity
                db.add(product)

            db.delete(order_model)
            db.commit()

    if order and order.items:
        # Reverter o estoque dos itens atuais
        for item in order_model.items:
            product = get_product_by_id(item.product_id, db)
            product.stock += item.quantity
            db.add(product)

        # Remover itens antigos
        for item in order_model.items:
            db.delete(item)

        # Validar e adicionar novos itens
        for item in order.items:
            product = get_product_by_id(item.product_id, db)

            # Verifica se o produto existe
            if not product:
                raise APIException(
                    code=404,
                    message="Produto não encontrado",
                    description=f"Produto com ID {item.product_id} "
                                f"não foi encontrado"
                )

            # Verifica se o estoque é suficiente
            if product.stock < item.quantity:
                raise APIException(
                    code=400,
                    message="Estoque insuficiente",
                    description=f"Produto {product.name} não tem estoque "
                                f"suficiente. Disponível: {product.stock}, "
                                f"Solicitado: {item.quantity}"
                )

            # Cria o modelo do item do pedido
            order_item = OrderItemModel(
                order_id=order_model.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=product.price
            )
            db.add(order_item)

            # Atualizar estoque
            product.stock -= item.quantity
            db.add(product)

        db.commit()
        db.refresh(order_model)

    return SuccessResponse(
        data=None,
        message="Pedido atualizado com sucesso"
    )


@router.delete("/delete_order/{order_id}", summary="Excluir um pedido")
def delete_order(
        order_id: int,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Exclui um pedido existente.

    Args:
        order_id (int): ID do pedido a ser excluído.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados do pedido excluído.
    """
    order_model = get_order_by_id(order_id, db)

    # Verifica se o pedido existe
    if not order_model:
        raise APIException(
            code=404,
            message="Pedido não encontrado",
            description=f"Pedido com ID {order_id} não foi encontrado"
        )

    # Verifica se o pedido pertence ao cliente autenticado
    if order_model.client_id != current_user.id:
        raise APIException(
            code=403,
            message="Acesso negado",
            description="Você não tem permissão para excluir este pedido"
        )

    # Reverter o estoque dos itens do pedido
    for item in order_model.items:
        product = get_product_by_id(item.product_id, db)
        product.stock += item.quantity
        db.add(product)

    # Excluir o pedido
    db.delete(order_model)
    db.commit()

    return SuccessResponse(
        data=None,
        message="Pedido excluído com sucesso"
    )
