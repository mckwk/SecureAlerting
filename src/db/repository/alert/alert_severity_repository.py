from db.entities import AlertSeverityEntity
from db.repository.base.base_repository import BaseRepository


class AlertSeverityRepository(BaseRepository[AlertSeverityEntity]):

    entity_class = AlertSeverityEntity