import uuid

from sqlalchemy import UUID, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from entity.base_entity import Base


class NonAllocatedOrderEntity(Base):
    __tablename__ = "non_allocated_order"

    non_allocated_order_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    reason: Mapped[str] = mapped_column(String, nullable=False)

    order_id: Mapped[UUID] = mapped_column(ForeignKey("order.order_id"), nullable=False)
    distribution_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("distribution.distribution_id"), nullable=False
    )
