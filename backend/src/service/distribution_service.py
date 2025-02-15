from datetime import datetime
from typing import List

from fastapi import Depends

from src.entity import (
    DistributionEntity,
    OrderDistributionEntity,
    NonAllocatedOrderEntity,
)
from src.repository.distribution_repository import (
    DistributionRepository,
    get_distribution_repository,
)
from src.repository.non_allocated_order_repository import (
    NonAllocatedOrderRepository,
    get_non_allocated_order_repository,
)
from src.repository.order_distribution_repository import OrderDistributionRepository
from src.repository.order_repository import OrderRepository, get_order_repository
from src.repository.truck_repository import TruckRepository, get_truck_repository
from src.service.bin_packing_service import BinPackingService


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

    def distribute_orders(
        self,
    ) -> dict[str, List[OrderDistributionEntity | NonAllocatedOrderEntity]]:
        orders = (
            self.order_repository.get_all_orders_that_status_is_different_than_allocated()
        )
        trucks = self.truck_repository.get_all()

        distribution_id = self.distribution_repository.create(
            DistributionEntity(date=datetime.now())
        ).distribution_id

        bin_packing_service = BinPackingService(
            orders=orders, trucks=trucks, distribution_id=distribution_id
        )

        order_distribution, non_allocated_orders = (
            bin_packing_service.best_fit_decreasing()
        )

        map(self.order_repository.update, orders)

        return {
            "order_distribution": [
                self.order_distribution_repository.create(order_distribution_entity)
                for order_distribution_entity in order_distribution
            ],
            "non_allocated_orders": [
                self.non_allocated_order_repository.create(non_allocated_orders_entity)
                for non_allocated_orders_entity in non_allocated_orders
            ],
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
