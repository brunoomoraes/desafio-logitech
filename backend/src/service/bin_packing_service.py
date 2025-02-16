from collections import defaultdict
from random import sample
from typing import List, Tuple, Dict
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
    The BFD is a good initial solution, but can miss easy improvements.
    So i ended up implementing a tabu search, to help optimize the distribution in hopes to fit more orders and use less trucks
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
        if len(self.orders) == 0:
            return [], []

        if len(self.trucks) == 0:
            [
                self._add_non_allocated_order(order, "No truck available")
                for order in self.orders
            ]
            return [], self.non_allocated_orders

        sorted_orders = sorted(self.orders, key=lambda x: x.weight, reverse=True)
        sorted_trucks = sorted(self.trucks, key=lambda x: x.max_weight, reverse=True)

        truck_loads = defaultdict(float)  # Track the current load based on truck_id
        truck_max_capacity = max(truck.max_weight for truck in self.trucks)

        for order in sorted_orders:
            if order.weight > truck_max_capacity:
                self._add_non_allocated_order(
                    order, "Order weight exceeds maximum truck capacity"
                )
                continue

            best_truck = None
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

    def tabu_search(
        self, max_iterations: int = 100, tabu_tenure: int = 10
    ) -> Tuple[List[OrderDistributionEntity], List[NonAllocatedOrderEntity]]:
        initial_order_distribution, _ = self.best_fit_decreasing()

        best_solution = initial_order_distribution.copy()
        best_truck_count = len(
            set(
                order_distribution_entity.truck_id
                for order_distribution_entity in best_solution
            )
        )

        tabu_list = []
        iteration = 0

        while iteration < max_iterations:
            neighbors = self._generate_neighbors(best_solution)

            best_neighbor = None
            best_allocated_count = -1
            best_neighbor_truck_count = float("inf")

            for neighbor in neighbors:
                allocated_count = len(neighbor)
                truck_count = len(set(dist.truck_id for dist in neighbor))

                if (
                    (allocated_count > best_allocated_count)
                    or (
                        allocated_count == best_allocated_count
                        and truck_count < best_neighbor_truck_count
                    )
                ) and neighbor not in tabu_list:
                    best_neighbor = neighbor
                    best_allocated_count = allocated_count
                    best_neighbor_truck_count = truck_count

            if best_neighbor:
                best_solution = best_neighbor
                best_truck_count = best_neighbor_truck_count
                tabu_list.append(best_neighbor)

                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)

            iteration += 1

        self.order_distribution = best_solution
        self.non_allocated_orders = self._get_non_allocated_orders(best_solution)
        return self.order_distribution, self.non_allocated_orders

    def _generate_neighbors(
        self, current_solution: List[OrderDistributionEntity]
    ) -> List[List[OrderDistributionEntity]]:
        neighbors = []

        for current_distribution in current_solution:

            for truck in self.trucks:
                if truck.truck_id != current_distribution.truck_id:
                    new_solution = current_solution.copy()

                    new_order_distribution = [
                        OrderDistributionEntity(
                            distribution_id=order_distribution_entity.distribution_id,
                            order_id=order_distribution_entity.order_id,
                            truck_id=(
                                truck.truck_id
                                if order_distribution_entity.order_id
                                == current_distribution.order_id
                                else order_distribution_entity.truck_id
                            ),
                        )
                        for order_distribution_entity in new_solution
                    ]

                    if self._is_valid_solution(new_order_distribution):
                        neighbors.append(new_order_distribution)

        for non_allocated in self.non_allocated_orders:
            for truck in self.trucks:
                if self._can_add_order_to_truck(non_allocated.order_id, truck):
                    new_solution = current_solution.copy()
                    new_order_distribution = new_solution + [
                        OrderDistributionEntity(
                            distribution_id=self.distribution_id,
                            order_id=non_allocated.order_id,
                            truck_id=truck.truck_id,
                        )
                    ]
                    if self._is_valid_solution(new_order_distribution):
                        neighbors.append(new_order_distribution)

        return sample(neighbors, len(neighbors))

    def _can_add_order_to_truck(self, order_id: UUID, truck: TruckEntity) -> bool:
        order_weight = self._get_order_weight(order_id)
        current_load = self._get_truck_loads(self.order_distribution).get(
            truck.truck_id, 0
        )
        return current_load + order_weight <= truck.max_weight

    def _is_valid_solution(
        self, order_distribution: List[OrderDistributionEntity]
    ) -> bool:
        truck_loads = self._get_truck_loads(order_distribution)
        return all(
            truck_loads[truck.truck_id] <= truck.max_weight for truck in self.trucks
        )

    def _get_truck_loads(
        self, order_distribution: List[OrderDistributionEntity]
    ) -> Dict[UUID, float]:
        truck_loads = defaultdict(float)
        for order_distribution_entity in order_distribution:
            truck_loads[order_distribution_entity.truck_id] += self._get_order_weight(
                order_distribution_entity.order_id
            )
        return truck_loads

    def _get_order_weight(self, order_id: UUID) -> float:
        return next(order.weight for order in self.orders if order.order_id == order_id)

    def _get_non_allocated_orders(
        self, order_distribution: List[OrderDistributionEntity]
    ) -> List[NonAllocatedOrderEntity]:
        allocated_orders = {
            order_distribution_entity.order_id
            for order_distribution_entity in order_distribution
        }

        non_allocated_orders = [
            NonAllocatedOrderEntity(
                order_id=order.order_id,
                distribution_id=self.distribution_id,
                reason="Not allocated",
            )
            for order in self.orders
            if order.order_id not in allocated_orders
        ]
        return non_allocated_orders
