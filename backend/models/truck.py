from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base
from backend.models.item import Item


class Truck(Base):
    __tablename__ = "trucks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight_max = Column(Float, nullable=False)
    weight_current = Column(Float, default=0.0)

    items = relationship("Item", back_populates="truck")

    @property
    def total_sum_items(self) -> float:
        return sum([item.weight for item in self.items])

    def can_add_item(self, item: Item) -> bool:
        return self.total_sum_items + item.weight <= self.weight_max

    def can_receive_more_items(self) -> bool:
        return self.weight_max >= self.weight_current
