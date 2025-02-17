from uuid import UUID

from pydantic import BaseModel

from src.entity.truck_entity import TruckEntity


class TruckResponseDTO(BaseModel):
    truck_id: UUID
    max_weight: float

    @classmethod
    def from_truck_entity(cls, truck_entity: TruckEntity) -> "TruckResponseDTO":
        return cls(
            truck_id=truck_entity.truck_id,
            max_weight=truck_entity.max_weight,
        )
