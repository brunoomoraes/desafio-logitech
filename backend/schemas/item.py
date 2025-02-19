from typing import List

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    name: str
    weight: float


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ItemListResponse(BaseModel):
    items: List[ItemResponse]

    model_config = ConfigDict(from_attributes=True)
