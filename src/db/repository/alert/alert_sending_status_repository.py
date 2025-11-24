from db.entities import AlertSendingStatusEntity
from db.repository.base.base_repository import BaseRepository


class AlertSendingStatusRepository(BaseRepository[AlertSendingStatusEntity]):

    entity_class = AlertSendingStatusEntity