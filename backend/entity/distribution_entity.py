import uuid
from datetime import datetime
from typing import List

from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from entity.base_entity import Base


class DistributionEntity(Base):
    __tablename__ = "distribution"

    distribution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    orders: Mapped[List["OrderDistributionEntity"]] = relationship(
        back_populates="distribution"
    )
