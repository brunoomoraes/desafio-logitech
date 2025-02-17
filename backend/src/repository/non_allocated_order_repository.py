from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.postgres import get_db
from src.entity import NonAllocatedOrderEntity
from src.repository.generic_repository import GenericRepository


class NonAllocatedOrderRepository(GenericRepository[NonAllocatedOrderEntity]):
    def __init__(self, db: Session):
        super().__init__(db, NonAllocatedOrderEntity)


def get_non_allocated_order_repository(db: Session = Depends(get_db)):
    return NonAllocatedOrderRepository(db)
