from uuid import UUID

from pydantic import BaseModel

from entity import NonAllocatedOrderEntity


class NonAllocatedOrderResponseDTO(BaseModel):
    non_allocated_order_id: UUID
    reason: str
    order_id: UUID

    @classmethod
    def from_non_allocated_order_entity(
        cls, non_allocated_order_entity: NonAllocatedOrderEntity
    ) -> "NonAllocatedOrderResponseDTO":
        return cls(
            non_allocated_order_id=non_allocated_order_entity.non_allocated_order_id,
            reason=non_allocated_order_entity.reason,
            order_id=non_allocated_order_entity.order_id,
        )
