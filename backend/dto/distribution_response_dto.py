from typing import List

from pydantic import BaseModel

from dto.distribute_order_service_response_dto import DistributeOrderServiceResponseDTO
from dto.non_allocated_order_response_dto import NonAllocatedOrderResponseDTO
from dto.order_distribution_response_dto import OrderDistributionResponseDTO


class DistributionResponseDTO(BaseModel):
    order_distribution: List[OrderDistributionResponseDTO]
    non_allocated_orders: List[NonAllocatedOrderResponseDTO]

    @classmethod
    def from_distribution_order_service_dto(
        cls, dto: DistributeOrderServiceResponseDTO
    ) -> "DistributionResponseDTO":
        return DistributionResponseDTO(
            order_distribution=[
                OrderDistributionResponseDTO.from_order_distribution_entity(
                    order_distribution
                )
                for order_distribution in dto.order_distribution
            ],
            non_allocated_orders=[
                NonAllocatedOrderResponseDTO.from_non_allocated_order_entity(
                    non_allocated_order
                )
                for non_allocated_order in dto.non_allocated_orders
            ],
        )
