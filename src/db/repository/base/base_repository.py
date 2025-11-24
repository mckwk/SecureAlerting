from datetime import datetime
from typing import Optional, List, Type
from uuid import UUID

from sqlalchemy.orm import Session

from db.repository.base.abstract_repository import AbstractRepository, Entity
from utils.validation.validation_utils import ValidationUtils


class BaseRepository(AbstractRepository[Entity, UUID]):

    entity_class = Type[Entity]

    def __init__(self, db: Session):
        self.db = db

    def upsert(self, entity: Optional[Entity]) -> Optional[Entity]:
        ValidationUtils.has_value_or_raise(entity)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def find_by_pk(self, pk: UUID) -> Optional[Entity]:
        return self.db.get(Type[Entity], pk)

    def find_all(self) -> List[Entity]:
        return self.db.query(self.entity_class).filter(
            self.entity_class.deleted_at.is_(None),
        ).all()

    def delete(self, entity: Optional[Entity]) -> None:
        ValidationUtils.has_value_or_raise(entity)
        entity.deleted_at = datetime.now()
        self.upsert(entity)
