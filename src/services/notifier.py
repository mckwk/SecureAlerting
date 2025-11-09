import json
import logging

from kafka import KafkaProducer

from src.config.settings import settings
from src.services.notification_service import (EmailNotificationService,
                                               INotificationService)
from src.services.risk_evaluator import RiskEvaluator


class Notifier:
    def __init__(self, notification_service: INotificationService = None):
        self.topic = settings.NOTIFICATION_TOPIC
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.risk_evaluator = RiskEvaluator()
        self.notification_service = notification_service or EmailNotificationService()
        self.logger = logging.getLogger(__name__)

    def send_notification(self, alert):
        try:
            # Calculate risk
            risk_data = self.risk_evaluator.evaluate_risk(alert)
            alert.update(risk_data)

            self.logger.info(f"Sending notification with risk data: {alert}")
            self.producer.send(self.topic, value=alert)
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")

    def send_email_notification(self, recipient, subject, message):
        try:
            self.notification_service.send_notification(
                recipient, subject, message)
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
