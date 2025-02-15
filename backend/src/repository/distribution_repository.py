from fastapi import Depends
from sqlalchemy.orm import Session

from src.database.postgres import get_db
from src.entity.distribution_entity import DistributionEntity
from src.repository.generic_repository import GenericRepository


class DistributionRepository(GenericRepository[DistributionEntity]):
    def __init__(self, db: Session) -> None:
        super().__init__(db, DistributionEntity)


def get_distribution_repository(
    db: Session = Depends(get_db),
) -> DistributionRepository:
    return DistributionRepository(db)
