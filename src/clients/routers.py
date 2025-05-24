# Imports de terceiros
import re
from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

# Imports locais
from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.auth.crud import get_user_by_email
from src.auth.jwt_auth import get_current_user
from src.clients.crud import get_client_by_email, get_client_by_cpf, get_client_by_id
from src.clients.models import ClientModel
from src.clients.schemas import ClientCreate, ClientOutput, ClientUpdate
from src.orders.models import OrderModel
from src.products.crud import get_product_by_id

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_detail_client", summary="Obter informações de um cliente específico")
async def get_client(
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Obtém um cliente pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        ClientModel: Instância do modelo de cliente.
    """
    client = get_client_by_id(current_user.id, db)

    if not client:
        raise APIException(
            code=404,
            message="Cliente não encontrado",
            description=f"O cliente com o ID {current_user.id} não foi encontrado"
        )

    return SuccessResponse(
        data=ClientOutput(**client.__dict__),
        message="Dados do cliente retornado com sucesso"
    )


@router.get("/get_clients", summary="Listar todos os clientes, com suporte a"
                         "paginação e filtro por nome e email")
async def get_clients(
        name: str = None,
        email: str = None,
        page: int = 1,
        limit: int = 10,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Obtém uma lista de clientes.

    Args:
        name (str): Nome do cliente a ser buscado.
        email (str): Email do cliente a ser buscado.
        page (int): Número da página para paginação.
        limit (int): Limite de resultados por página.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados dos clientes encontrados.
    """
    clients = db.query(ClientModel)

    if name:
        clients = clients.filter(ClientModel.name.ilike(f"%{name}%"))

    if email:
        clients = clients.filter(ClientModel.email.ilike(f"%{email}%"))

    clients = clients.offset((page - 1) * limit).limit(limit).all()

    return SuccessResponse(
        data=[ClientOutput(**client.__dict__) for client in clients],
        message="Clientes retornados com sucesso"
    )


@router.post("/create_client", summary=" Criar um novo cliente, validando email e CPF")
async def create_client(
        client: ClientCreate,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Cria um novo cliente.

    Args:
        client (ClientCreate): Dados do cliente a ser criado.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados do cliente criado.
    """
    client_email = get_client_by_email(client.email, db)
    client_cpf = get_client_by_cpf(
        client.cpf.replace(".", "").replace("-", ""),
        db
    )

    # Verifica duplicidade de email e CPF
    if client_email or client_cpf:
        raise APIException(
            code=409,
            message="Email ou CPF já cadastrado",
            description="Já existe um cliente com esse email ou cpf"
        )

    user_email = get_user_by_email(client.email, db)

    # Verifica se o email está associado a um usuário
    if not user_email:
        raise APIException(
            code=404,
            message="Email não cadastrado",
            description="O email informado não está cadastrado no sistema. Cadastre o usuário antes de cadastrar o cliente"
        )

    # Expressão regular para CPF
    # Aceita: 123.456.789-09 ou 12345678909
    cpf_regex = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'

    # Verifica se o CPF está no formato correto
    if not re.match(cpf_regex, client.cpf):
        raise APIException(
            code=400,
            message="CPF inválido",
            description="O CPF deve estar no formato 123.456.789-09 ou 12345678909"
        )

    # Expressão regular para telefone
    # Aceita: (12) 934567-8901 ou 129345678901
    phone_regex = r'^\(?\d{2}\)? ?\d{4,5}-?\d{4}$'

    # Verifica se o telefone está no formato correto
    if not re.match(phone_regex, client.phone):
        raise APIException(
            code=400,
            message="Telefone inválido",
            description = "O telefone deve estar no formato (12) 93456-7890 ou 12934567890",
        )

    # Cria o modelo de cliente
    client_model = ClientModel(
        name=client.name,
        last_name=client.last_name,
        email=client.email,
        cpf=client.cpf.replace(".", "").replace("-", ""),
        phone=client.phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    )

    db.add(client_model)
    db.commit()
    db.refresh(client_model)

    return SuccessResponse(
        data=None,
        message="Cliente criado com sucesso"
    )


@router.put("/update_client", summary="Atualizar informações de um cliente específico")
async def update_client(
        client: ClientUpdate,
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Atualiza as informações de um cliente.

    Args:
        client (ClientUpdate): Dados do cliente a serem atualizados.
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados do cliente atualizado.
    """
    client_model = get_client_by_id(current_user.id, db)

    # Verifica se o cliente existe
    if not client_model:
        raise APIException(
            code=404,
            message="Cliente não encontrado",
            description=f"O cliente com o ID {current_user.id} não foi encontrado"
        )

    # Verifica duplicidade de email
    if client.email:
        client_email = get_client_by_email(client.email, db)
        user_email = get_user_by_email(client.email, db)

        if client_email or user_email:
            raise APIException(
                code=409,
                message="Email já cadastrado",
                description = "Já existe um cliente ou usuário com esse email"
            )

    # Verifica duplicidade de CPF
    if client.cpf:
        cleaned_cpf = client.cpf.replace(".", "").replace("-", "")
        client_cpf = get_client_by_cpf(cleaned_cpf, db)

        if client_cpf:
            raise APIException(
                code=409,
                message="CPF já cadastrado",
                description="Já existe um cliente com esse CPF"
            )

        # Valida formato do CPF
        cpf_regex = r'^\d{3}\.?\d{3}\.?\d{3}-?\d{2}$'

        # Verifica se o CPF está no formato correto
        if not re.match(cpf_regex, client.cpf):
            raise APIException(
                code=400,
                description="CPF inválido",
                message="O CPF deve estar no formato 123.456.789-09 ou 12345678909"
            )

    # Valida formato do telefone
    if client.phone:
        phone_regex = r'^\(?\d{2}\)? ?\d{4,5}-?\d{4}$'

        # Verifica se o telefone está no formato correto
        if not re.match(phone_regex, client.phone):
            raise APIException(
                code=400,
                message="Telefone inválido",
                description="O telefone deve estar no formato (12) 93456-7890 ou 12934567890",
            )

    # Atualiza os dados do cliente
    if client.name:
        client_model.name = client.name

    if client.last_name:
        client_model.last_name = client.last_name

    if client.email:
        user_mail = get_user_by_email(client_model.email, db)
        client_model.email = client.email

        # Se o cliente já tem um usuário associado, atualiza o email do usuário
        if user_mail:
            user_mail.email = client.email
            db.commit()
            db.refresh(user_mail)

    if client.cpf:
        client_model.cpf = client.cpf.replace(".", "").replace("-", "")

    if client.phone:
        client_model.phone = client.phone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")

    db.commit()
    db.refresh(client_model)

    return SuccessResponse(
        data=None,
        message="Cliente atualizado com sucesso"
    )


@router.delete("/delete_client", summary="Excluir um cliente")
async def delete_client(
        db: Session = Depends(get_db),
        current_user: Annotated[ClientModel, Depends(get_current_user)] = None
):
    """
    Deleta um cliente.

    Args:
        db (Session): Sessão do banco de dados.
        current_user (ClientModel): Cliente autenticado.
    Returns:
        SuccessResponse: Resposta de sucesso com os dados do cliente deletado.
    """
    client_model = get_client_by_id(current_user.id, db)

    # Verifica se o cliente existe
    if not client_model:
        raise APIException(
            code=404,
            message="Cliente não encontrado",
            description=f"O cliente com o ID {current_user.id} não foi encontrado"
        )

    # Buscar todos os pedidos associados ao cliente
    orders = db.query(OrderModel).filter(OrderModel.client_id == client_model.id).all()

    if orders:
        for order in orders:
            # Reverter o estoque dos itens do pedido
            for item in order.items:
                product = get_product_by_id(item.product_id, db)
                product.stock += item.quantity
                db.add(product)

    # Verifica se o cliente está associado a algum usuário
    user = get_user_by_email(client_model.email, db)

    # Se estiver um usuário associado, deve deletar o usuário também
    if user:
        db.delete(user)
        db.commit()

    db.delete(client_model)
    db.commit()

    return SuccessResponse(
        data=None,
        message="Cliente deletado com sucesso"
    )
