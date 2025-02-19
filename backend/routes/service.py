from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.service import distribuir_pedidos

router = APIRouter()


@router.get("/")
def distribuir(db: Session = Depends(get_db)):
    return distribuir_pedidos(db)
