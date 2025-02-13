from typing import List

from fastapi import Depends, HTTPException

from dto.create_order_input_dto import CreateOrderInputDto
from dto.order_response_dto import OrderResponseDTO
from entity import order_entity
from entity.order_entity import OrderEntity
from service.order_service import OrderService, get_order_service
from uuid import UUID


class OrderController:
    def __init__(self, order_service: OrderService) -> None:
        self.order_service = order_service

    def create_order(self, order_dto: CreateOrderInputDto) -> OrderResponseDTO:
        entity = OrderEntity(
            weight=order_dto.weight,
        )
        return OrderResponseDTO.from_order_entity(self.order_service.create(entity))

    def find_by_id(self, order_id: UUID) -> OrderResponseDTO:
        entity = self.order_service.find_by_id(order_id)

        if entity is None:
            raise HTTPException(status_code=404, detail="Order not found")

        return OrderResponseDTO.from_order_entity(entity)

    def get_all_orders(self) -> List[OrderResponseDTO]:
        order_entities = self.order_service.get_all()
        return [OrderResponseDTO.from_order_entity(entity) for entity in order_entities]


def get_order_controller(
    order_service: OrderService = Depends(get_order_service),
) -> OrderController:
    return OrderController(order_service)
