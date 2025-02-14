from uuid import UUID

from fastapi import APIRouter, Depends

from controller.order_controller import OrderController, get_order_controller
from dto.create_order_dto import CreateOrderDto

order_router = APIRouter(prefix="/order", tags=["order"])


@order_router.get("")
def get_all_orders(order_controller: OrderController = Depends(get_order_controller)):
    return order_controller.get_all_orders()


@order_router.post("")
def create_order(
    dto: CreateOrderDto,
    order_controller: OrderController = Depends(get_order_controller),
):
    return order_controller.create_order(dto)
