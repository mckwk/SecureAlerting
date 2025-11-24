from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.entities.alert.alert_sending_status_entity import AlertSendingStatusEntity
from src.db.entities.alert.alert_severity_entity import AlertSeverityEntity
from src.db.entities.alert.alert_type_entity import AlertTypeEntity
from src.db.entities.base.base_entity import BaseEntity
from src.db.entities.risk.risk_estimation_model_entity import RiskEstimationModelEntity


class AlertEntity(BaseEntity):
    __tablename__ = "alerts"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    subject: Mapped[Optional[str]] = mapped_column(String(255))
    message: Mapped[Optional[str]] = mapped_column(Text)
    sender: Mapped[Optional[str]] = mapped_column(String(512))
    recipient: Mapped[Optional[str]] = mapped_column(String(512))
    severity_id: Mapped[UUID] = mapped_column(ForeignKey("alert_severities.id"))
    severity: Mapped[AlertSeverityEntity] = relationship(
        back_populates="alerts"
    )
    type_id: Mapped[UUID] = mapped_column(ForeignKey("alert_types.id"))
    type: Mapped[AlertTypeEntity] = relationship(
        back_populates="alerts"
    )
    sending_status_id: Mapped[UUID] = mapped_column(
        ForeignKey("alert_sending_statuses.id")
    )
    sending_status: Mapped[AlertSendingStatusEntity] = relationship(
        back_populates="alerts"
    )
    risk_estimation_model_id: Mapped[UUID] = mapped_column(
        ForeignKey("risk_estimation_models.id")
    )
    risk_estimation_model: Mapped[RiskEstimationModelEntity] = relationship(
        back_populates="alerts"
    )
    first_sent_attempt_at: Mapped[Optional[datetime]] = mapped_column(
        default=None
    )
    sent_at: Mapped[Optional[datetime]] = mapped_column(
        default=None
    )
    retries: Mapped[Optional[int]] = mapped_column(
        default=0
    )
    is_batch: Mapped[Optional[bool]] = mapped_column(
        default=None
    )

    __table_args__ = (
        Index(
            'idx0_alerts_sent_at',
            'sent_at'
        ),
        Index(
            'idx1_alerts_first_sent_attempt_at',
            'first_sent_attempt_at'
        ),
        Index(
            'idx2_alerts_subject',
            'subject'
        ),
    )