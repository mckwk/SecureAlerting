import json
import logging

from kafka import KafkaConsumer

from config import settings
from services.notifier import Notifier


class KafkaAlertConsumer:
    def __init__(self, bootstrap_servers):
        self.topic = settings.NOTIFICATION_TOPIC
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.notifier = Notifier()

    def consume_alerts(self):
        for message in self.consumer:
            alert = message.value
            logging.info(f"Received alert from topic '{self.topic}': {alert}")
            self.notifier.process_alert(alert)


if __name__ == "__main__":
    consumer = KafkaAlertConsumer(bootstrap_servers=settings.KAFKA_BROKER_URL)
    consumer.consume_alerts()
