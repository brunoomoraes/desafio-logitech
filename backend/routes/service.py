from fastapi import APIRouter

from backend.service import distribuir_pedidos

router = APIRouter()


@router.get("/")
def distribuir():
    return distribuir_pedidos()
