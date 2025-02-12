from datetime import datetime

from sqlalchemy import Column, UUID, Float, String, Enum, DateTime
import uuid

from entity.base_entity import Base
from status.order_status import OrderStatus


class OrderEntity(Base):
    __tablename__ = "order"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    weight = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.CREATED)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
