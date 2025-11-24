from db.entities import RiskEstimationModelEntity
from db.repository.base.base_repository import BaseRepository


class RiskEstimationModelRepository(BaseRepository[RiskEstimationModelEntity]):

    entity_class = RiskEstimationModelEntity