from pydantic import BaseModel


class CreateOrderDto(BaseModel):
    weight: float
