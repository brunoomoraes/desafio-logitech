from http.client import HTTPException
from typing import List
from uuid import UUID

from fastapi import Depends, HTTPException

from src.dto.create_truck_dto import CreateTruckDto
from src.dto.truck_response_dto import TruckResponseDTO
from src.dto.update_truck_weight_dto import UpdateTruckWeightDto
from src.entity.truck_entity import TruckEntity
from src.service.truck_service import TruckService, get_truck_service


class TruckController:
    def __init__(self, truck_service: TruckService) -> None:
        self.truck_service = truck_service

    def create_truck(self, truck_dto: CreateTruckDto) -> TruckResponseDTO:
        entity = TruckEntity(
            max_weight=truck_dto.max_weight,
        )
        return TruckResponseDTO.from_truck_entity(self.truck_service.create(entity))

    def get_all_trucks(self) -> List[TruckResponseDTO]:
        truck_entities = self.truck_service.get_all()
        return [TruckResponseDTO.from_truck_entity(entity) for entity in truck_entities]

    def update_truck(self, truck_id: UUID, truck_dto: UpdateTruckWeightDto):
        truck_entity = self.truck_service.find_by_id(truck_id)

        if truck_entity is None:
            raise HTTPException(status_code=404, detail="Truck not found")

        truck_entity.max_weight = truck_dto.max_weight
        return self.truck_service.update(truck_entity)


def get_truck_controller(
    truck_service: TruckService = Depends(get_truck_service),
) -> TruckController:
    return TruckController(truck_service)
