from collections import defaultdict
from datetime import datetime
from typing import List, TypedDict
from uuid import UUID

from fastapi import Depends

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
from status.order_status import OrderStatus

"""
    The problem we are trying to solve is a bin package problem, more specifically the variable bin package problem.
    I have studied this problem in college in my operational research course. there are some implementation that 
    are gready, and some solutions that use metaheuristics, and not necessarily returns the optimal solution.
    This is a NP-HARD problem. So there is no polynomial solution. 
    In my research i found some solution for this problem, the one that its implemented here is the BFD.
    It's a greedy algorithm, that is based on putting the next order in the best fit truck,
    that in this case is the truck with the least amount of space remaining.
    The BFD is a good solution, but for large datasets, is costly, and a metaheuristics algorithm is probably better.
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

    def distribute_orders(self) -> dict[str, List[OrderDistributionEntity | NonAllocatedOrderEntity]]:
        orders = (
            self.order_repository.get_all_orders_that_status_is_different_than_allocated()
        )
        trucks = self.truck_repository.get_all()

        distribution_id = self.distribution_repository.create(
            DistributionEntity(date=datetime.now())
        ).distribution_id

        return self.best_fit_decreasing(orders, trucks, distribution_id)

    def best_fit_decreasing(
        self, orders: List[OrderEntity], trucks: List[TruckEntity], distribution_id: UUID
    ) -> dict[str, List[OrderDistributionEntity | NonAllocatedOrderEntity]]:
        sorted_orders = sorted(orders, key=lambda x: x.weight, reverse=True)
        sorted_trucks = sorted(trucks, key=lambda x: x.max_weight, reverse=True)

        truck_loads = defaultdict(float) # Track the current load based on truck_id
        order_distribution = []
        non_allocated_orders = []

        for order in sorted_orders:
            best_truck = None # Track if order can be put in a truck
            min_remaining_weight = float("inf")

            for truck in sorted_trucks:
                remaining_weight = truck.max_weight - truck_loads[truck.truck_id]
                if order.weight <= remaining_weight < min_remaining_weight:
                    best_truck = truck
                    min_remaining_weight = remaining_weight

            if best_truck:
                truck_loads[best_truck.truck_id] += order.weight

                order.status = OrderStatus.ALLOCATED
                self.order_repository.update(order)

                order_distribution.append(
                    self.order_distribution_repository.create(
                        OrderDistributionEntity(
                            distribution_id=distribution_id,
                            truck_id=best_truck.truck_id,
                            order_id=order.order_id,
                        )
                    )
                )
            else:
                order.status = OrderStatus.NON_ALLOCATED
                self.order_repository.update(order)

                non_allocated_orders.append(
                    self.non_allocated_order_repository.create(
                        NonAllocatedOrderEntity(
                            order_id=order.order_id,
                            distribution_id=distribution_id,
                            reason="Cannot fit order"
                        )
                    )
                )


        return {
            "order_distribution": order_distribution,
            "non_allocated_orders": non_allocated_orders,
        }

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
