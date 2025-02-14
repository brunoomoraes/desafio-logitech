from fastapi import Depends
from sqlalchemy.orm import Session

from database.postgres import get_db
from entity.distribution_entity import DistributionEntity
from repository.generic_repository import GenericRepository


class DistributionRepository(GenericRepository[DistributionEntity]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, DistributionEntity)


def get_distribution_repository(
    db: Session = Depends(get_db),
) -> DistributionRepository:
    return DistributionRepository(db)
