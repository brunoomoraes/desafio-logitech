from typing import List
from uuid import UUID

import pytest

from src.entity import OrderEntity, TruckEntity
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
            truck_id=UUID("01ad9072-8f6c-40fa-96c3-a0c2b94670a5"),
            max_weight=100
        ),
        TruckEntity(
            truck_id=UUID("8a17fd04-4b21-42c0-8f73-a4e7cae1a8c8"),
            max_weight=150
        ),
        TruckEntity(
            truck_id=UUID("c29660f1-b699-44c2-9d79-c19d092bdf2e"),
            max_weight=200
        ),
    ]