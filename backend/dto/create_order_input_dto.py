from pydantic import BaseModel


class CreateOrderInputDto(BaseModel):
    weight: float
