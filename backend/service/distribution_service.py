from datetime import datetime
from typing import List, TypedDict
from uuid import UUID

from fastapi import Depends

from dto.distribute_order_service_response_dto import DistributeOrderServiceResponseDTO
from entity import (
    DistributionEntity,
    OrderEntity,
    TruckEntity,
    OrderDistributionEntity,
    NonAllocatedOrderEntity,
)
from repository.distribution_repository import (
    DistributionRepository,
    get_distribution_repository,
)
from repository.non_allocated_order_repository import (
    NonAllocatedOrderRepository,
    get_non_allocated_order_repository,
)
from repository.order_distribution_repository import OrderDistributionRepository
from repository.order_repository import OrderRepository, get_order_repository
from repository.truck_repository import TruckRepository, get_truck_repository

"""
    The problem we are trying to solve is a bin package problem, more specifically the variable bin package problem.
    I have studied this problem in college in my operational research course. there are some implementation that 
    are gready, and some solutions that use heuristics, and not necessarily returns the optimal solution.
    This is a NP-HARD problem. So there is no polynomial solution. 
    In my research i found some solution for this problem, the one that its implemented here is the BFD.
    It's a greedy algorithm, that is based on putting the next order in the best fit truck,
    that in this case is the truck with the least amount of space remaining.
"""


class DistributionService:
    def __init__(
        self,
        truck_repository: TruckRepository,
        order_repository: OrderRepository,
        distribution_repository: DistributionRepository,
        non_allocated_order_repository: NonAllocatedOrderRepository,
        order_distribution_repository: OrderDistributionRepository,
    ):
        self.truck_repository = truck_repository
        self.order_repository = order_repository
        self.distribution_repository = distribution_repository
        self.non_allocated_order_repository = non_allocated_order_repository
        self.order_distribution_repository = order_distribution_repository

    def distribute_orders(self) -> DistributeOrderServiceResponseDTO:
        orders = (
            self.order_repository.get_all_orders_that_status_is_different_than_allocated()
        )
        trucks = self.truck_repository.get_all()

        distribution_id = self.distribution_repository.create(
            DistributionEntity(date=datetime.now())
        ).distribution_id

        return self.best_fit_decreasing(orders, trucks, distribution_id)

    @staticmethod
    def best_fit_decreasing(
        orders: List[OrderEntity], trucks: List[TruckEntity], distribution_id: UUID
    ) -> DistributeOrderServiceResponseDTO:
        pass


def get_distribution_service(
    truck_repository: TruckRepository = Depends(get_truck_repository),
    order_repository: OrderRepository = Depends(get_order_repository),
    distribution_repository: DistributionRepository = Depends(
        get_distribution_repository
    ),
    non_allocated_order_repository: NonAllocatedOrderRepository = Depends(
        get_non_allocated_order_repository
    ),
    order_distribution_repository: OrderDistributionRepository = Depends(
        get_non_allocated_order_repository
    ),
) -> DistributionService:
    return DistributionService(
        truck_repository=truck_repository,
        order_repository=order_repository,
        distribution_repository=distribution_repository,
        non_allocated_order_repository=non_allocated_order_repository,
        order_distribution_repository=order_distribution_repository,
    )
