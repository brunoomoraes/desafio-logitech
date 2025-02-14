from typing import List

from fastapi import Depends

from entity.truck_entity import TruckEntity
from repository.truck_repository import get_truck_repository, TruckRepository


class TruckService:
    def __init__(self, truck_repository: TruckRepository):
        self._truck_repository = truck_repository

    def create(self, truck_entity: TruckEntity) -> TruckEntity:
        return self._truck_repository.create(truck_entity)

    def get_all(self) -> List[TruckEntity]:
        return self._truck_repository.get_all()

def get_truck_service(
    truck_repository: TruckRepository = Depends(get_truck_repository),
) -> TruckService:
    return TruckService(truck_repository)
