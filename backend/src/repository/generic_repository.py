from typing import TypeVar, Generic, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from src.entity.base_entity import Base

T = TypeVar("T", bound=Base)


class GenericRepository(Generic[T]):
    def __init__(self, db: Session, model: Base) -> None:
        self.db = db
        self.model = model

    def create(self, entity: T) -> T:
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return entity
        except Exception as e:
            self.db.rollback()
            raise e

    def find_by_id(self, entity_id: UUID) -> Optional[T]:
        return self.db.query(self.model).get(entity_id)

    def get_all(self) -> list[T]:
        return self.db.query(self.model).all()

    def update(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, entity: T) -> None:
        self.db.delete(T)
        self.db.commit()
