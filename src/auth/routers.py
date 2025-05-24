# Imports de terceiros
from fastapi import APIRouter, Body, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

# Imports locais
from core.config import settings
from core.database import get_db
from core.exceptions import APIException, SuccessResponse
from src.auth.crud import get_user_by_email, get_user_by_id
from src.auth.jwt_auth import (create_access_token, create_refresh_token,
                               get_password, verify_password)
from src.auth.models import UserModel
from src.auth.schemas import TokenPayload, UserAuth
from src.clients.crud import get_client_by_email

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", summary="Registro de novo usuário")
async def create_user(user: UserAuth, db: Session = Depends(get_db)):
    """
    Cria um novo usuário.

    Args:
        user (UserAuth): Dados do usuário a ser criado.
        db (Session): Sessão do banco de dados.
    Returns:
        UserModel: Instância do modelo de usuário criado.
    """

    user_email = get_user_by_email(user.email, db)
    client_email = get_client_by_email(user.email, db)

    # Verifica se o email já está cadastrado
    if user_email or client_email:
        raise APIException(
            code=409,
            message="Email já cadastrado",
            description="O email informado já está cadastrado no sistema"
        )

    # Cria o modelo de usuário
    user_model = UserModel(
        email=user.email,
        hashed_password=get_password(user.password)
    )

    db.add(user_model)
    db.commit()
    db.refresh(user_model)

    return SuccessResponse(
        data=None,
        message="Usuário criado com sucesso"
    )


@router.post("/login", summary="Autenticação de usuário")
def authenticate(
        data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    """
    Autentica um usuário.

    Args:
        data (OAuth2PasswordRequestForm): Dados de autenticação do usuário.
        db (Session): Sessão do banco de dados.
    Returns:
        dict: Dicionário contendo o token de acesso e refresh token.
    """
    user = get_user_by_email(data.username, db)

    # Verifica se as credenciais estão corretas
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }


@router.post("/refresh-token", summary="Refresh de token JWT")
async def refresh_token(
        token_refresh: str = Body(...),
        db: Session = Depends(get_db),
):
    """
    Cria um novo token de acesso utilizando o refresh token.

    Args:
        token_refresh (str): Refresh token.
        db (Session): Sessão do banco de dados.
    Returns:
        dict: Dicionário contendo o novo token de acesso e refresh token.
    """
    try:
        payload = jwt.decode(
            token_refresh,
            settings.JWT_REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = get_user_by_id(token_data.sub, db)

    # Verifica se o usuário existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id)
    }
