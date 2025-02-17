from pydantic import BaseModel
from uuid import UUID

from src.entity.order_entity import OrderEntity
from src.status.order_status import OrderStatus


class OrderResponseDTO(BaseModel):
    order_id: UUID
    weight: float
    status: OrderStatus

    @classmethod
    def from_order_entity(cls, order_entity: OrderEntity) -> "OrderResponseDTO":
        return cls(
            order_id=order_entity.order_id,
            weight=order_entity.weight,
            status=order_entity.status,
        )
