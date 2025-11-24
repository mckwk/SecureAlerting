from typing import List, Optional, TYPE_CHECKING
from uuid import uuid4, UUID

from sqlalchemy import String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.entities.base.base_entity import BaseEntity

if TYPE_CHECKING:
    from src.db.entities.alert.alert_entity import AlertEntity


class AlertSeverityEntity(BaseEntity):
    __tablename__ = "alert_severities"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    reference: Mapped[str] = mapped_column(String(80), unique=True)
    max_risk_score: Mapped[Optional[int]] = mapped_column(
        default=None
    )

    alerts: Mapped[List["AlertEntity"]] = relationship(back_populates="severity")

    __table_args__ = (
        Index(
            'idx0_alert_severities_max_risk_score',
            'max_risk_score'
        ),
    )