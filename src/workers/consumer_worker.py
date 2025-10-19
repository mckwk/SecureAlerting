import json

from kafka import KafkaConsumer

from config.settings import settings
from services.notifier import Notifier


class ConsumerWorker:
    def __init__(self):
        self.consumer = KafkaConsumer(
            settings.NOTIFICATION_TOPIC,
            bootstrap_servers=settings.KAFKA_BROKER_URL,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        self.notifier = Notifier()

    def run(self):
        for message in self.consumer:
            alert = message.value
            self.process_alert(alert)

    def process_alert(self, alert):
        self.notifier.send_notification(alert)


if __name__ == "__main__":
    worker = ConsumerWorker()
    worker.run()
