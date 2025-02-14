from uuid import UUID

from pydantic import BaseModel


class TruckResponseDTO(BaseModel):
    truck_id: UUID
    max_weight: float
