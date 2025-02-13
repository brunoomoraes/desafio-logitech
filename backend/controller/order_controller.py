from fastapi import Depends

from dto.create_order_input_dto import CreateOrderInputDto
from dto.create_order_response_dto import CreateOrderResponseDTO
from entity.order_entity import OrderEntity
from service.order_service import OrderService, get_order_service


class OrderController:
    def __init__(self, order_service: OrderService) -> None:
        self.order_service = order_service

    def create_order(self, order_dto: CreateOrderInputDto) -> CreateOrderResponseDTO:
        order_entity = OrderEntity(
            weight=order_dto.weight,
        )

        order_entity = self.order_service.create(order_entity)
        return CreateOrderResponseDTO(
            order_id=order_entity.order_id,
            weight=order_entity.weight,
            status=order_entity.status,
        )

def get_order_controller(order_service: OrderService = Depends(get_order_service)) -> OrderController:
    return OrderController(order_service)