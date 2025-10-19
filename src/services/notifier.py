import json
import logging

from kafka import KafkaProducer

from src.config.settings import settings


class Notifier:
    def __init__(self):
        self.topic = settings.NOTIFICATION_TOPIC
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.logger = logging.getLogger(__name__)

    def send_notification(self, alert):
        try:
            self.logger.info(f"Attempting to send notification: {alert}")
            self.producer.send(self.topic, value=alert)
            self.producer.flush()
            self.logger.info(
                f"Notification sent to topic '{self.topic}': {alert}"
            )
        except Exception as e:
            self.logger.error(f"Failed to send notification: {e}")
