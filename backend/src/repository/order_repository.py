from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.postgres import get_db
from src.entity.order_entity import OrderEntity
from src.repository.generic_repository import GenericRepository
from src.status.order_status import OrderStatus


class OrderRepository(GenericRepository[OrderEntity]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, OrderEntity)

    def get_all_orders_that_status_is_different_than_allocated(
        self,
    ) -> List[OrderEntity]:
        return (
            self.db.query(OrderEntity)
            .filter(OrderEntity.status != OrderStatus.ALLOCATED)
            .all()
        )


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)
