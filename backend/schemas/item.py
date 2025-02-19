from typing import List

from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    weight: float


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int

    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    items: List[ItemResponse]

    class Config:
        from_attributes = True
