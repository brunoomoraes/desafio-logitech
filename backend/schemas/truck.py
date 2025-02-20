from typing import List

from pydantic import BaseModel, ConfigDict

from backend.schemas.item import ItemResponse


class TruckBase(BaseModel):
    name: str
    weight_max: float


class TruckCreate(TruckBase):
    pass


class TruckResponse(TruckBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class _TruckResponse(TruckResponse):
    weight_current: float
    items: List[ItemResponse]

    model_config = ConfigDict(from_attributes=True)


class TruckListResponse(BaseModel):
    trucks: List[_TruckResponse]

    model_config = ConfigDict(from_attributes=True)
