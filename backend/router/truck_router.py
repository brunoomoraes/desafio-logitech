from uuid import UUID

from fastapi import APIRouter, Depends

from controller.truck_controller import TruckController, get_truck_controller
from dto.create_truck_dto import CreateTruckDto
from dto.update_truck_weight_dto import UpdateTruckWeightDto

truck_router = APIRouter(prefix="/truck", tags=["truck"])

@truck_router.get("")
def get_all_trucks(truck_controller: TruckController = Depends(get_truck_controller)):
    return truck_controller.get_all_trucks()

@truck_router.post("")
def create_truck(dto: CreateTruckDto, controller: TruckController = Depends(get_truck_controller)):
    return controller.create_truck(dto)

@truck_router.put("/{truck_id}")
def update_truck_weight(truck_id: UUID, dto: UpdateTruckWeightDto, controller: TruckController = Depends(get_truck_controller)):
    return controller.update_truck(truck_id, dto)
