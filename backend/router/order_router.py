from fastapi import APIRouter, Depends

from controller.order_controller import OrderController, get_order_controller
from dto.create_order_input_dto import CreateOrderInputDto

order_router = APIRouter(prefix="/order", tags=["order"])

@order_router.post("")
def create_order(dto: CreateOrderInputDto, order_controller: OrderController = Depends(get_order_controller)):
    return order_controller.create_order(dto)