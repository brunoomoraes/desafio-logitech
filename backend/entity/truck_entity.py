from datetime import datetime

from sqlalchemy import Column, UUID, Float, DateTime
import uuid

from entity.base_entity import Base


class TruckEntity(Base):
    __tablename__ = "truck"

    truck_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    weight = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
