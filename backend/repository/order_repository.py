from typing import Type, Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from database.postgres import get_db
from entity.order_entity import OrderEntity


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, order: OrderEntity) -> OrderEntity:
        try:
            self.db.add(order)
            self.db.commit()
            self.db.refresh(order)
            return order
        except Exception as e:
            self.db.rollback()
            raise e

    def find_by_id(self, order_id: UUID) -> Optional[OrderEntity]:
        return (
            self.db.query(OrderEntity).filter(OrderEntity.order_id == order_id).first()
        )

    def get_all(self) -> list[OrderEntity]:
        return self.db.query(OrderEntity).all()

    def update(self, order: OrderEntity) -> OrderEntity:
        self.db.refresh(order)
        return order

    def delete(self, order: OrderEntity) -> None:
        self.db.delete(order)
        self.db.commit()


def get_order_repository(db: Session = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)
