from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from entity.base_entity import Base


class OrderDistributionEntity(Base):
    __tablename__ = "order_distribution"

    distribution_id: Mapped[UUID] = mapped_column(
        ForeignKey("distribution.distribution_id"), primary_key=True
    )
    order_id: Mapped[UUID] = mapped_column(
        ForeignKey("order.order_id"), primary_key=True
    )
    truck_id: Mapped[UUID] = mapped_column(
        ForeignKey("truck.truck_id"), primary_key=True
    )

    distribution: Mapped["DistributionEntity"] = relationship(back_populates="orders")
    order: Mapped["OrderEntity"] = relationship(back_populates="distribution")
    truck: Mapped["TruckEntity"] = relationship(back_populates="distributions")
