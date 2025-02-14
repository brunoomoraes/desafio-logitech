from pydantic import BaseModel


class CreateTruckDto(BaseModel):
    max_weight: float
