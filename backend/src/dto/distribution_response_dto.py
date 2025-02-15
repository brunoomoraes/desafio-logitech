from typing import List

from pydantic import BaseModel

from src.dto.non_allocated_order_response_dto import NonAllocatedOrderResponseDTO
from src.dto.order_distribution_response_dto import OrderDistributionResponseDTO
from src.entity import OrderDistributionEntity, NonAllocatedOrderEntity


class DistributionResponseDTO(BaseModel):
    order_distribution: List[OrderDistributionResponseDTO]
    non_allocated_orders: List[NonAllocatedOrderResponseDTO]

    @classmethod
    def from_dict(
        cls,
        distribution_response_dict: dict[
            str, List[OrderDistributionEntity | NonAllocatedOrderEntity]
        ],
    ) -> "DistributionResponseDTO":
        return DistributionResponseDTO(
            order_distribution=[
                OrderDistributionResponseDTO.from_order_distribution_entity(
                    order_distribution
                )
                for order_distribution in distribution_response_dict.get(
                    "order_distribution"
                )
            ],
            non_allocated_orders=[
                NonAllocatedOrderResponseDTO.from_non_allocated_order_entity(
                    non_allocated_order
                )
                for non_allocated_order in distribution_response_dict.get(
                    "non_allocated_orders"
                )
            ],
        )
