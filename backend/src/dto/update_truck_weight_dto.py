from pydantic import BaseModel


class UpdateTruckWeightDto(BaseModel):
    max_weight: float
