from typing import List

from pydantic import BaseModel

from entity import OrderDistributionEntity, NonAllocatedOrderEntity


class DistributeOrderServiceResponseDTO(BaseModel):
    order_distribution: List[OrderDistributionEntity]
    non_allocated_orders: List[NonAllocatedOrderEntity]
