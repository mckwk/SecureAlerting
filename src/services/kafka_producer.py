import json

from kafka import KafkaProducer

from src.config.settings import settings
from src.models.alert import Alert


class AlertProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_alert(self, topic, alert: Alert):
        self.producer.send(topic, alert.to_dict())
        self.producer.flush()
