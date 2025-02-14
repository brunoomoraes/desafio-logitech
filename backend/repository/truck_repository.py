from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.orm import Session

from database.postgres import get_db
from entity.truck_entity import TruckEntity
from repository.generic_repository import GenericRepository


class TruckRepository(GenericRepository[TruckEntity]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, TruckEntity)


def get_truck_repository(db: Session = Depends(get_db)) -> TruckRepository:
    return TruckRepository(db)
