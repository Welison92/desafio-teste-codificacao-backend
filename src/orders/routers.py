
from fastapi import APIRouter


router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def get_orders():
    return {"message": "List of orders"}
