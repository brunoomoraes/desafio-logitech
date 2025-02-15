from uuid import UUID

from pydantic import BaseModel

from entity import OrderDistributionEntity


class OrderDistributionResponseDTO(BaseModel):
    distribution_id: UUID
    order_id: UUID
    truck_id: UUID

    @classmethod
    def from_order_distribution_entity(
        cls, order_distribution_entity: OrderDistributionEntity
    ) -> "OrderDistributionResponseDTO":
        return cls(
            distribution_id=order_distribution_entity.distribution_id,
            order_id=order_distribution_entity.order_id,
            truck_id=order_distribution_entity.truck_id,
        )
