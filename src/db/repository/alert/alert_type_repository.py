from db.entities import AlertTypeEntity
from db.repository.base.base_repository import BaseRepository


class AlertTypeRepository(BaseRepository[AlertTypeEntity]):

    entity_class = AlertTypeEntity