from sqlalchemy.orm import Session

from src.clients.models import ClientModel


def get_client_by_email(
        email: str,
        db: Session
):
    """
    Obtém um cliente pelo email.

    Args:
        email (str): Email do cliente a ser buscado.
        db (Session): Sessão do banco de dados.
    Returns:
        Optional[ClientModel]: Instância do modelo de cliente ou None se não
        encontrado.
    """
    return db.query(ClientModel).filter(ClientModel.email == email).first()


def get_client_by_id(
        client_id: int,
        db: Session
):
    """
    Obtém um cliente pelo ID.

    Args:
        client_id (int): ID do cliente a ser buscado.
        db (Session): Sessão do banco de dados.
    Returns:
        Optional[ClientModel]: Instância do modelo de cliente ou None se não
        encontrado.
    """
    return db.query(ClientModel).filter(ClientModel.id == client_id).first()


def get_client_by_cpf(
        cpf: str,
        db: Session
):
    """
    Obtém um cliente pelo CPF.

    Args:
        cpf (str): CPF do cliente a ser buscado.
        db (Session): Sessão do banco de dados.
    Returns:
        Optional[ClientModel]: Instância do modelo de cliente ou None se não
        encontrado.
    """
    return db.query(ClientModel).filter(ClientModel.cpf == cpf).first()
