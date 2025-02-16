from collections import defaultdict
from typing import List
from uuid import UUID, uuid4

import pytest

from src.entity import OrderEntity, TruckEntity
from src.service.bin_packing_service import BinPackingService
from src.status.order_status import OrderStatus


@pytest.fixture
def distribution_id():
    return UUID("f6485ae8-f15e-46c7-a0c0-d49cc57d78a6")


@pytest.fixture
def sample_orders() -> List[OrderEntity]:
    return [
        OrderEntity(
            order_id=UUID("a591d7b9-495f-4921-9b73-f634173d48d7"),
            weight=50,
            status=OrderStatus.CREATED,
        ),
        OrderEntity(
            order_id=UUID("53412567-911f-43ea-bd74-2ab75f22c16f"),
            weight=75,
            status=OrderStatus.CREATED,
        ),
        OrderEntity(
            order_id=UUID("1b089cfd-50e1-45d1-83c4-48d861fa04ab"),
            weight=25,
            status=OrderStatus.CREATED,
        ),
    ]


@pytest.fixture
def sample_trucks() -> List[TruckEntity]:
    return [
        TruckEntity(
            truck_id=UUID("01ad9072-8f6c-40fa-96c3-a0c2b94670a5"), max_weight=100
        ),
        TruckEntity(
            truck_id=UUID("8a17fd04-4b21-42c0-8f73-a4e7cae1a8c8"), max_weight=150
        ),
        TruckEntity(
            truck_id=UUID("c29660f1-b699-44c2-9d79-c19d092bdf2e"), max_weight=200
        ),
    ]


def test_simple_allocation(sample_orders, sample_trucks, distribution_id):
    service = BinPackingService(sample_orders, sample_trucks, distribution_id)
    order_distribution, non_allocated = service.best_fit_decreasing()

    assert len(order_distribution) == 3
    assert len(non_allocated) == 0
    assert all(order.status == OrderStatus.ALLOCATED for order in sample_orders)
    assert any(
        order_distribution_entity.truck_id
        == UUID("01ad9072-8f6c-40fa-96c3-a0c2b94670a5")
        and order_distribution_entity.order_id
        == UUID("1b089cfd-50e1-45d1-83c4-48d861fa04ab")
        for order_distribution_entity in order_distribution
    )
    assert any(
        order_distribution_entity.truck_id
        == UUID("01ad9072-8f6c-40fa-96c3-a0c2b94670a5")
        and order_distribution_entity.order_id
        == UUID("53412567-911f-43ea-bd74-2ab75f22c16f")
        for order_distribution_entity in order_distribution
    )
    assert any(
        order_distribution_entity.truck_id
        == UUID("8a17fd04-4b21-42c0-8f73-a4e7cae1a8c8")
        and order_distribution_entity.order_id
        == UUID("a591d7b9-495f-4921-9b73-f634173d48d7")
        for order_distribution_entity in order_distribution
    )


def test_empty_input(distribution_id):
    service = BinPackingService([], [], distribution_id)
    order_distribution, non_allocated = service.best_fit_decreasing()

    assert len(order_distribution) == 0
    assert len(non_allocated) == 0


def test_empty_trucks(sample_orders, distribution_id):
    service = BinPackingService(sample_orders, [], distribution_id)
    order_distribution, non_allocated = service.best_fit_decreasing()

    assert len(order_distribution) == 0
    assert len(non_allocated) == len(sample_orders)
    assert all(order.status == OrderStatus.NON_ALLOCATED for order in sample_orders)
    assert all(
        non_allocated_entity.reason == "No truck available"
        for non_allocated_entity in non_allocated
    )


# No truck can fit this order
def test_order_larger_than_truck_limit(distribution_id, sample_trucks):
    heavy_order = OrderEntity(order_id=uuid4(), weight=250, status=OrderStatus.CREATED)

    service = BinPackingService([heavy_order], sample_trucks, distribution_id)
    order_distribution, non_allocated = service.best_fit_decreasing()

    assert len(order_distribution) == 0
    assert len(non_allocated) == 1
    assert non_allocated[0].reason == "Order weight exceeds maximum truck capacity"
    assert heavy_order.status == OrderStatus.NON_ALLOCATED


# The first truck has the same capacity as the order, so it should fit preferably in the first truck
def test_best_fit_order(distribution_id, sample_trucks):
    order = OrderEntity(order_id=uuid4(), weight=100, status=OrderStatus.CREATED)

    service = BinPackingService([order], sample_trucks, distribution_id)
    order_distribution, non_allocated = service.best_fit_decreasing()
    assert len(order_distribution) == 1
    assert len(non_allocated) == 0
    assert order.status == OrderStatus.ALLOCATED
    assert order_distribution[0].truck_id == sample_trucks[0].truck_id


def test_if_truck_load_doesnt_exceeds_max_truck_capacity(distribution_id):
    trucks = [
        TruckEntity(truck_id=uuid4(), max_weight=100),
        TruckEntity(truck_id=uuid4(), max_weight=150),
    ]

    orders = [
        OrderEntity(order_id=uuid4(), weight=80, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=60, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=40, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=70, status=OrderStatus.CREATED),
    ]

    service = BinPackingService(orders, trucks, distribution_id)
    order_distribution, non_allocated = service.best_fit_decreasing()

    assert len(order_distribution) + len(non_allocated) == len(orders)

    assert (
        next(
            order.weight
            for order in orders
            if order.order_id == non_allocated[0].order_id
        )
        == 40
    )

    truck_loads = defaultdict(float)
    for order_distribution_entity in order_distribution:
        order_weight = next(
            order.weight
            for order in orders
            if order.order_id == order_distribution_entity.order_id
        )
        truck_max_weight = next(
            truck.max_weight
            for truck in trucks
            if truck.truck_id == order_distribution_entity.truck_id
        )
        truck_loads[order_distribution_entity.truck_id] += order_weight
        assert truck_loads[order_distribution_entity.truck_id] <= truck_max_weight

def test_tabu_search_basic_allocation(distribution_id):
    trucks = [
        TruckEntity(truck_id=uuid4(), max_weight=100),
        TruckEntity(truck_id=uuid4(), max_weight=150),
    ]

    orders = [
        OrderEntity(order_id=uuid4(), weight=80, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=90, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=40, status=OrderStatus.CREATED),
    ]

    service = BinPackingService(orders, trucks, distribution_id)
    order_distribution, non_allocated = service.tabu_search(max_iterations=50)

    # All orders should be allocated
    assert len(order_distribution) == 3
    assert len(non_allocated) == 0

    # Check truck loads don't exceed capacity
    truck_loads = service._get_truck_loads(order_distribution)
    for truck in trucks:
        assert truck_loads[truck.truck_id] <= truck.max_weight


def test_tabu_search_overweight_order():
    distribution_id = UUID('12345678-1234-5678-1234-567812345678')

    trucks = [
        TruckEntity(truck_id=uuid4(), max_weight=100)
    ]

    orders = [
        OrderEntity(order_id=uuid4(), weight=150, status=OrderStatus.CREATED),
    ]

    service = BinPackingService(orders, trucks, distribution_id)
    order_distribution, non_allocated = service.tabu_search()

    assert len(order_distribution) == 0
    assert len(non_allocated) == 1


def test_tabu_search_overweight_order():
    distribution_id = UUID('12345678-1234-5678-1234-567812345678')

    trucks = [
        TruckEntity(UUID('truck-1'), 100.0)
    ]

    orders = [
        OrderEntity(UUID('order-1'), 150.0)  # Order too heavy for any truck
    ]

    service = BinPackingService(orders, trucks, distribution_id)
    order_distribution, non_allocated = service.tabu_search()

    assert len(order_distribution) == 0
    assert len(non_allocated) == 1
    assert non_allocated[0].reason == "Order weight exceeds maximum truck capacity"


def test_tabu_search_improvement_over_best_fit(distribution_id):
    trucks = [
        TruckEntity(truck_id=uuid4(), max_weight=100),
        TruckEntity(truck_id=uuid4(), max_weight=150),
    ]

    orders = [
        OrderEntity(order_id=uuid4(), weight=80, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=60, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=40, status=OrderStatus.CREATED),
        OrderEntity(order_id=uuid4(), weight=70, status=OrderStatus.CREATED),
    ]

    service = BinPackingService(orders, trucks, distribution_id)

    _, bfd_non_allocated_orders = service.best_fit_decreasing()
    bfd_non_allocated_orders_size = len(bfd_non_allocated_orders)

    _, tabu_non_allocated_orders = service.tabu_search(max_iterations=100)
    tabu_non_allocated_orders_size = len(tabu_non_allocated_orders)

    assert tabu_non_allocated_orders_size < bfd_non_allocated_orders_size