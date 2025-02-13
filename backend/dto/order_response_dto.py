from pydantic import BaseModel
from uuid import UUID

from status.order_status import OrderStatus


class OrderResponseDTO(BaseModel):
    order_id: UUID
    weight: float
    status: OrderStatus