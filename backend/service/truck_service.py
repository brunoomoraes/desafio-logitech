from typing import List, Optional
from uuid import UUID

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

    def find_by_id(self, truck_id: UUID) -> Optional[TruckEntity]:
        return self._truck_repository.find_by_id(truck_id)

    def update(self, truck_entity: TruckEntity) -> TruckEntity:
        return self._truck_repository.update(truck_entity)


def get_truck_service(
    truck_repository: TruckRepository = Depends(get_truck_repository),
) -> TruckService:
    return TruckService(truck_repository)
