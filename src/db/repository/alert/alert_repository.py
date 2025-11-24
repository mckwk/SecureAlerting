from db.entities import AlertEntity
from db.repository.base.base_repository import BaseRepository


class AlertRepository(BaseRepository[AlertEntity]):

    entity_class = AlertEntity