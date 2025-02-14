from typing import List

from fastapi import Depends

from dto.create_order_dto import CreateOrderDto
from dto.order_response_dto import OrderResponseDTO
from entity.order_entity import OrderEntity
from service.order_service import OrderService, get_order_service


class OrderController:
    def __init__(self, order_service: OrderService) -> None:
        self.order_service = order_service

    def create_order(self, order_dto: CreateOrderDto) -> OrderResponseDTO:
        entity = OrderEntity(
            weight=order_dto.weight,
        )
        return OrderResponseDTO.from_order_entity(self.order_service.create(entity))

    def get_all_orders(self) -> List[OrderResponseDTO]:
        order_entities = self.order_service.get_all()
        return [OrderResponseDTO.from_order_entity(entity) for entity in order_entities]


def get_order_controller(
    order_service: OrderService = Depends(get_order_service),
) -> OrderController:
    return OrderController(order_service)
