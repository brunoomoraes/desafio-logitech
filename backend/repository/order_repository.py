from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from database.postgres import get_db
from entity.order_entity import OrderEntity
from repository.generic_repository import GenericRepository


class OrderRepository(GenericRepository[OrderEntity]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, OrderEntity)


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)
