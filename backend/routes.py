from fastapi import APIRouter
from backend.services import distribuir_pedidos

router = APIRouter()

@router.get("/distribuir")
def distribuir():
    return distribuir_pedidos()
