# Imports do sistema
from datetime import datetime, timedelta, timezone
from typing import Any, Union

# Imports de terceiros
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session

# Imports locais
from core.config import settings
from core.database import get_db
from src.auth.crud import get_user_by_id
from src.auth.models import UserModel
from src.auth.schemas import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
password_context = CryptContext(
    schemes=["bcrypt", "pbkdf2_sha256"],
    deprecated="auto"
)


def get_password(password: str) -> str:
    """
    Gera um hash para a senha fornecida.

    Args:
        password (str): A senha a ser hasheada.
    Returns:
        str: O hash da senha.
    """
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash armazenado.

    Args:
        password (str): A senha a ser verificada.
        hashed_password (str): O hash da senha armazenada.
    Returns:
        bool: True se a senha corresponder, False caso contrário.
    """
    return password_context.verify(password, hashed_password)


def create_access_token(
        subject: Union[str, Any],
        expires_delta: int = None
) -> str:
    """
    Cria um token de acesso JWT.

    Args:
        subject (Union[str, Any]): O assunto do token.
        expires_delta (int, optional): O tempo de expiração em minutos.
        Se None, usa o padrão.
    Returns:
        str: O token JWT de acesso.
    """
    if expires_delta:
        expires = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expires,
        "sub": str(subject)
    }

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def create_refresh_token(
        subject: Union[str, Any],
        expires_delta: int = None
) -> str:
    """
    Cria um token de atualização JWT.

    Args:
        subject (Union[str, Any]): O assunto do token.
        expires_delta (int, optional): O tempo de expiração em minutos.
        Se None, usa o padrão.
    Returns:
        str: O token JWT de atualização.
    """
    if expires_delta:
        expires = datetime.now(timezone.utc) + timedelta(minutes=expires_delta)
    else:
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expires,
        "sub": str(subject)
    }

    return jwt.encode(
        to_encode,
        settings.JWT_REFRESH_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserModel:
    """
    Obtém o usuário atual a partir do token JWT.

    Args:
        token (str): O token JWT do usuário.
        db (Session): A sessão do banco de dados.
    Returns:
        UserModel: O modelo do usuário atual.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        exp_datetime = datetime.fromtimestamp(token_data.exp, tz=timezone.utc)
        if exp_datetime < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = get_user_by_id(token_data.sub, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


def require_role(role: str):
    """
    Verifica se o usuário atual tem a função especificada.

    Args:
        role (str): A função necessária para acessar o recurso.
    Returns:
        Callable: Um callable que verifica a função do usuário.
    """
    def role_checker(current_user: UserModel = Depends(get_current_user)):
        """
        Verifica se o usuário atual tem a função especificada.

        Args:
            current_user (UserModel): O usuário atual.
        Raises:
            HTTPException: Se o usuário não tiver a função necessária.
        """
        if current_user.role.value != role:
            raise HTTPException(
                status_code=403,
                detail="Operation not permitted"
            )
        return current_user

    return role_checker
