from collections import defaultdict
from typing import List, Tuple
from uuid import UUID

from src.entity import (
    OrderEntity,
    TruckEntity,
    OrderDistributionEntity,
    NonAllocatedOrderEntity,
)
from src.status.order_status import OrderStatus


"""
    The problem we are trying to solve is a bin package problem, more specifically the variable bin package problem.
    I have studied this problem in college in my operational research course. there are some implementation that 
    are greedy, and some solutions that use metaheuristics, and not necessarily returns the optimal solution.
    This is a NP-HARD problem. So there is no polynomial solution. 
    In my research i found some solution for this problem, the one that its implemented here is the BFD.
    It's a greedy algorithm, that is based on putting the next order in the best fit truck,
    that in this case is the truck with the least amount of space remaining.
    The BFD is a good solution, but for large datasets, is costly, and a metaheuristics algorithm is probably better.
"""
class BinPackingService:
    def __init__(
        self,
        orders: List[OrderEntity],
        trucks: List[TruckEntity],
        distribution_id: UUID,
    ):
        self.orders = orders
        self.trucks = trucks
        self.distribution_id = distribution_id
        self.order_distribution: List[OrderDistributionEntity] = []
        self.non_allocated_orders: List[NonAllocatedOrderEntity] = []

    def _add_order_distribution(self, order: OrderEntity, truck: TruckEntity):
        order.status = OrderStatus.ALLOCATED

        self.order_distribution.append(
            OrderDistributionEntity(
                distribution_id=self.distribution_id,
                truck_id=truck.truck_id,
                order_id=order.order_id,
            )
        )

    def _add_non_allocated_order(self, order, reason):
        order.status = OrderStatus.NON_ALLOCATED

        self.non_allocated_orders.append(
            NonAllocatedOrderEntity(
                order_id=order.order_id,
                distribution_id=self.distribution_id,
                reason=reason,
            )
        )

    def best_fit_decreasing(
        self,
    ) -> Tuple[List[OrderDistributionEntity], List[NonAllocatedOrderEntity]]:
        sorted_orders = sorted(self.orders, key=lambda x: x.weight, reverse=True)
        sorted_trucks = sorted(self.trucks, key=lambda x: x.max_weight, reverse=True)

        truck_loads = defaultdict(float)  # Track the current load based on truck_id
        truck_max_capacity = max(truck.max_weight for truck in self.trucks)

        for order in sorted_orders:
            if order.weight > truck_max_capacity:
                self._add_non_allocated_order(
                    order, "Order weight exceeds maximum truck capacity"
                )

            best_truck = None  # Track if order can be put in a truck
            min_remaining_weight = float("inf")

            for truck in sorted_trucks:
                remaining_weight = truck.max_weight - truck_loads[truck.truck_id]
                if order.weight <= remaining_weight < min_remaining_weight:
                    best_truck = truck
                    min_remaining_weight = remaining_weight

            if best_truck:
                truck_loads[best_truck.truck_id] += order.weight
                self._add_order_distribution(order, best_truck)

            else:
                self._add_non_allocated_order(order, "Cannot fit order")

        return self.order_distribution, self.non_allocated_orders
