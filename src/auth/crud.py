from sqlalchemy.orm import Session


from src.auth.models import UserModel



def get_user_by_email(
        email: str,
        db: Session
):
    """
    Obtém um usuário pelo email.

    Args:
        email (str): Email do usuário a ser buscado.
        db (Session): Sessão do banco de dados.
    Returns:
        Optional[UserModel]: Instância do modelo de usuário ou None se não
        encontrado.
    """
    return db.query(UserModel).filter(UserModel.email == email).first()


def get_user_by_id(user_id: int, db: Session):
    """
    Obtém um usuário pelo ID.

    Args:
        user_id (int): ID do usuário a ser buscado.
        db (Session): Sessão do banco de dados.
    Returns:
        Optional[UserModel]: Instância do modelo de usuário ou None se não
        encontrado.
    """
    return db.query(UserModel).filter(UserModel.id == user_id).first()

