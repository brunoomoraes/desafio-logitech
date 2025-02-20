from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)
    truck_id = Column(Integer, ForeignKey("trucks.id"), nullable=True)

    truck = relationship("Truck", back_populates="items", foreign_keys=[truck_id])
