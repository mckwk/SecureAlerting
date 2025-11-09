import json

from kafka import KafkaConsumer

from config.settings import settings
from src.workers.notification_worker import NotificationWorker


class ConsumerWorker:
    def __init__(self):
        self.consumer = KafkaConsumer(
            settings.NOTIFICATION_TOPIC,
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.notification_worker = NotificationWorker()

    def run(self):
        for message in self.consumer:
            alert = message.value
            self.notification_worker.process_alert(alert)


if __name__ == "__main__":
    worker = ConsumerWorker()
    worker.run()
