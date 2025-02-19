from pydantic import BaseModel
from backend.schemas.item import ItemResponse
from typing import List


class TruckBase(BaseModel):
    name: str
    weight_max: float


class TruckCreate(TruckBase):
    pass


class TruckResponse(TruckBase):
    id: int

    class Config:
        from_attributes = True


class _TruckResponse(TruckResponse):
    weight_current: float
    items: List[ItemResponse]

    class Config:
        from_attributes = True


class TruckListResponse(BaseModel):
    trucks: List[_TruckResponse]

    class Config:
        from_attributes = True
