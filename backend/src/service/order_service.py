from typing import List

from fastapi import Depends

from src.entity.order_entity import OrderEntity
from src.repository.order_repository import OrderRepository, get_order_repository


class OrderService:
    def __init__(self, order_repository: OrderRepository) -> None:
        self.order_repository = order_repository

    def create(self, order: OrderEntity) -> OrderEntity:
        return self.order_repository.create(order)

    def get_all(self) -> List[OrderEntity]:
        return self.order_repository.get_all()


def get_order_service(
    order_repository: OrderRepository = Depends(get_order_repository),
) -> OrderService:
    return OrderService(order_repository)
