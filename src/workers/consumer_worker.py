import json
import logging
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from src.config.settings import settings
from src.services.notification_service import NotificationService
from src.services.notifier_factory import NotifierFactory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsumerWorker:
    def __init__(self, max_retries=5, retry_delay=5):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.consumer = None
        notifier = NotifierFactory.get_notifier("email")
        self.notification_service = NotificationService(notifier)

        self.connect_to_broker()

    def connect_to_broker(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.consumer = KafkaConsumer(
                    settings.NOTIFICATION_TOPIC,
                    bootstrap_servers=settings.KAFKA_BROKER_URL,
                    group_id="consumer_worker_group",
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='earliest',
                    enable_auto_commit=True
                )
                logger.info("Connected to Kafka broker.")
                return
            except NoBrokersAvailable as e:
                retries += 1
                logger.warning(
                    f"Failed to connect to Kafka broker (attempt {retries}/{self.max_retries}): {e}")
                if retries < self.max_retries:
                    time.sleep(self.retry_delay)
                else:
                    logger.error(
                        "Exceeded maximum retries to connect to Kafka broker.")
                    raise RuntimeError(
                        "Exceeded maximum retries to connect to Kafka broker.")

    def run(self):
        logger.info("Running ConsumerWorker...")
        for message in self.consumer:
            alert = message.value
            logger.info(f"Processing alert: {alert}")
            try:
                self.notification_service.send_notification(
                    recipient="test_user@example.com",
                    subject=f"[SEVERITY: {alert['severity'].upper()}] New Alert Notification",
                    message=alert["message"],
                    severity=alert["severity"],
                    timestamp=alert.get("timestamp", "N/A")
                )
                logger.info("Notification sent successfully.")
            except Exception as e:
                logger.error(f"Failed to send notification: {e}")


if __name__ == "__main__":
    logger.info("Starting ConsumerWorker...")
    worker = ConsumerWorker()
    logger.info("ConsumerWorker initialized.")
    worker.run()
