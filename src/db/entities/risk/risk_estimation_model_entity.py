from typing import Optional, List, TYPE_CHECKING
from uuid import uuid4, UUID

from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.entities.base.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.db.entities.alert.alert_entity import AlertEntity


class RiskEstimationModelEntity(BaseEntity):
    __tablename__ = "risk_estimation_models"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text)
    reference: Mapped[str] = mapped_column(String(255), unique=True)

    alerts: Mapped[List["AlertEntity"]] = relationship(
        back_populates="risk_estimation_model"
    )