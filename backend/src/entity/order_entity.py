from sqlalchemy import UUID, Float, Enum
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.entity.base_entity import Base
from src.status.order_status import OrderStatus


class OrderEntity(Base):
    __tablename__ = "order"

    order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus), nullable=False, default=OrderStatus.CREATED
    )

    distribution: Mapped["OrderDistributionEntity"] = relationship(
        back_populates="order", uselist=False
    )
