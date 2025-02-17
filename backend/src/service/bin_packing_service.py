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
                order=order,
                truck=truck,
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
        self, max_iterations: int = 100, tabu_tenure: int = 25
    ) -> Tuple[List[OrderDistributionEntity], List[NonAllocatedOrderEntity]]:
        self.non_allocated_orders.clear()
        self.order_distribution.clear()

        initial_order_distribution, initial_non_allocated_orders = self.best_fit_decreasing()

        best_solution = self.copy_list_of_order_distribution_entity(initial_order_distribution)
        best_allocated_count = len(initial_order_distribution)
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
            best_neighbor_allocated_count = -1
            best_neighbor_truck_count = float("inf")

            for neighbor in neighbors:
                allocated_count = len(neighbor)
                truck_count = len(set(dist.truck_id for dist in neighbor))

                if (
                    (allocated_count > best_neighbor_allocated_count)
                    or (
                        allocated_count == best_neighbor_allocated_count
                        and truck_count < best_neighbor_truck_count
                    )
                ) and neighbor not in tabu_list:
                    best_neighbor = neighbor
                    best_neighbor_allocated_count = allocated_count
                    best_neighbor_truck_count = truck_count

            if best_neighbor and (
                    (best_neighbor_allocated_count > best_allocated_count)
                    or (
                        best_allocated_count == best_neighbor_allocated_count
                        and best_truck_count < best_neighbor_truck_count
                    )
            ):
                best_solution = best_neighbor
                best_truck_count = best_neighbor_truck_count
                tabu_list.append(best_neighbor)

                if len(tabu_list) > tabu_tenure:
                    tabu_list.pop(0)

            iteration += 1

        self.order_distribution = best_solution
        self.non_allocated_orders = self._get_non_allocated_orders(best_solution, initial_non_allocated_orders)
        return self.order_distribution, self.non_allocated_orders

    def _generate_neighbors(
        self, current_solution: List[OrderDistributionEntity]
    ) -> List[List[OrderDistributionEntity]]:
        neighbors = []

        # Single order move
        for current_distribution in current_solution:
            for truck in self.trucks:
                if truck.truck_id != current_distribution.truck_id:
                    new_solution = self.copy_list_of_order_distribution_entity(current_solution)

                    new_order_distribution = [
                        OrderDistributionEntity(
                            distribution_id=order_distribution_entity.distribution_id,
                            order_id=order_distribution_entity.order_id,
                            order=order_distribution_entity.order,
                            truck_id=(
                                truck.truck_id
                                if order_distribution_entity.order_id
                                == current_distribution.order_id
                                else order_distribution_entity.truck_id
                            ),
                            truck=(
                                truck
                                if order_distribution_entity.order_id
                                == current_distribution.order_id
                                else order_distribution_entity.truck
                           )
                        )
                        for order_distribution_entity in new_solution
                    ]

                    if self._is_valid_solution(new_order_distribution):
                        neighbors.append(new_order_distribution)

        # Swap order between trucks
        for order_distribution_i in current_solution:
            for order_distribution_j in current_solution:
                if order_distribution_i != order_distribution_j and order_distribution_i.truck_id != order_distribution_j.truck_id:
                    new_solution = []

                    for order_distribution_entity in self.copy_list_of_order_distribution_entity(current_solution):
                        if order_distribution_entity.order_id == order_distribution_i.order_id:
                            order_distribution_entity.truck_id = order_distribution_j.truck_id
                            order_distribution_entity.truck = order_distribution_j.truck
                            new_solution.append(order_distribution_entity)
                        elif order_distribution_entity.order_id == order_distribution_j.order_id:
                            order_distribution_entity.truck_id = order_distribution_i.truck_id
                            order_distribution_entity.truck = order_distribution_i.truck
                            new_solution.append(order_distribution_entity)
                        else:
                            new_solution.append(order_distribution_entity)


                    if self._is_valid_solution(new_solution):
                        neighbors.append(new_solution)

        # Try to squeeze another order that was previously not allocated
        for neighbor in neighbors.copy():
            for non_allocated in self.non_allocated_orders:
                non_allocated_order = next(order for order in self.orders if order.order_id == non_allocated.order_id)
                truck_loads = self._get_truck_loads(neighbor)
                for truck in self.trucks:
                    if truck_loads[truck.truck_id] + non_allocated_order.weight <= truck.max_weight:
                        new_solution = self.copy_list_of_order_distribution_entity(neighbor)
                        new_order_distribution = new_solution + [
                            OrderDistributionEntity(
                                distribution_id=self.distribution_id,
                                order_id=non_allocated.order_id,
                                truck_id=truck.truck_id,
                                order=non_allocated_order,
                                truck=truck,
                            )
                        ]
                        neighbors.append(new_order_distribution)

        return sample(neighbors, len(neighbors))

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
                order_distribution_entity
            )
        return truck_loads

    @staticmethod
    def _get_order_weight(order_distribution_entity: OrderDistributionEntity) -> float:
        return order_distribution_entity.order.weight

    @staticmethod
    def copy_list_of_order_distribution_entity(order_distribution: List[OrderDistributionEntity]) -> List[OrderDistributionEntity]:
        return [
            OrderDistributionEntity(
                distribution_id=order_distribution_entity.distribution_id,
                order_id=order_distribution_entity.order_id,
                order=order_distribution_entity.order,
                truck_id=order_distribution_entity.truck_id,
                truck=order_distribution_entity.truck,
            )
            for order_distribution_entity in order_distribution
        ]

    def _get_non_allocated_orders(
        self, order_distribution: List[OrderDistributionEntity], initial_non_allocated_orders: List[NonAllocatedOrderEntity]
    ) -> List[NonAllocatedOrderEntity]:
        non_allocated_orders = []

        allocated_orders = [
            order_distribution_entity.order_id
            for order_distribution_entity in order_distribution
        ]

        dict_of_initial_non_allocated_orders = defaultdict(NonAllocatedOrderEntity)
        for non_allocated_order in initial_non_allocated_orders:
            dict_of_initial_non_allocated_orders[non_allocated_order.order_id] = non_allocated_order

        for order in self.orders:
            if order.order_id in allocated_orders: continue

            if order.order_id in dict_of_initial_non_allocated_orders.keys():
                non_allocated_orders.append(dict_of_initial_non_allocated_orders[order.order_id])
            else:
                non_allocated_orders.append(
                    NonAllocatedOrderEntity(
                        order_id=order.order_id,
                        distribution_id=self.distribution_id,
                        reason="Not allocated",
                    )
                )

        return non_allocated_orders
