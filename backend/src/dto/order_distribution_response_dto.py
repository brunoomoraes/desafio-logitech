from uuid import UUID

from pydantic import BaseModel

from src.entity import OrderDistributionEntity


class OrderDistributionResponseDTO(BaseModel):
    distribution_id: UUID
    order_id: UUID
    truck_id: UUID
    order_weight: float
    truck_max_weight: float

    @classmethod
    def from_order_distribution_entity(
        cls, order_distribution_entity: OrderDistributionEntity
    ) -> "OrderDistributionResponseDTO":
        return cls(
            distribution_id=order_distribution_entity.distribution_id,
            order_id=order_distribution_entity.order_id,
            truck_id=order_distribution_entity.truck_id,
            order_weight=order_distribution_entity.order.weight,
            truck_max_weight=order_distribution_entity.truck.max_weight,
        )
