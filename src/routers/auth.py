# Imports de terceiros
from fastapi import APIRouter, File, UploadFile
from fastapi.params import Depends
from sqlalchemy.orm import Session

# Imports locais
from core.database import get_db
from core.exceptions import APIException, SuccessResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.get('/teste')
async def teste():
    return {"message": "Hello World"}
