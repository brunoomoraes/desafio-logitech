from pydantic import BaseModel
from uuid import UUID


class GetUserByIdDTO(BaseModel):
    order_id: UUID
