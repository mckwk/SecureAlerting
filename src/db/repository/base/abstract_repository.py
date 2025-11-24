from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

from db.entities.base.base_entity import BaseEntity

Entity = TypeVar("Entity", bound=BaseEntity)
PK = TypeVar("PK")


class AbstractRepository(ABC, Generic[Entity, PK]):

    @abstractmethod
    def upsert(self, entity: Optional[Entity]) -> Optional[Entity]:
        pass

    @abstractmethod
    def find_by_pk(self, pk: PK) -> Optional[Entity]:
        pass

    @abstractmethod
    def find_all(self) -> List[Entity]:
        pass

    @abstractmethod
    def delete(self, entity: Optional[Entity]) -> None:
        pass