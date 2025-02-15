from enum import Enum


class OrderStatus(Enum):
    CREATED = "CREATED"
    ALLOCATED = "ALLOCATED"
    NON_ALLOCATED = "NON_ALLOCATED"
