from typing import List

from sqlalchemy import UUID, Float
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from entity.base_entity import Base


class TruckEntity(Base):
    __tablename__ = "truck"

    truck_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    max_weight: Mapped[float] = mapped_column(Float, nullable=False)

    distributions: Mapped[List["OrderDistributionEntity"]] = relationship(
        back_populates="truck"
    )
