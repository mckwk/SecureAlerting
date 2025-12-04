import json
import logging
import threading
import time
from datetime import datetime
from queue import Queue

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from src.config.settings import settings
from src.models.alert import Alert
from src.services.notification_service import NotificationService
from src.services.notifier_factory import NotifierFactory
from src.services.risk_evaluator import RiskEvaluator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConsumerWorker:
    def __init__(self, max_retries=5, retry_delay=5, batch_interval=60):
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.consumer = None
        self.risk_evaluator = RiskEvaluator()
        self.batch_queue = Queue()
        self.batch_interval = settings.BATCH_NOTIFICATION_INTERVAL  # Time in seconds
        self.last_batch_time = datetime.now()

        self.connect_to_broker()

        # Start the batch processing thread
        self.batch_thread = threading.Thread(
            target=self.process_batch_queue, daemon=True)
        self.batch_thread.start()

    def connect_to_broker(self):
        retries = 0
        while retries < self.max_retries:
            try:
                self.consumer = KafkaConsumer(
                    settings.NOTIFICATION_TOPIC,
                    bootstrap_servers=settings.KAFKA_BROKER_URL,
                    group_id=settings.KAFKA_CONSUMER_GROUP,
                    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                    auto_offset_reset='earliest',
                    enable_auto_commit=False
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

    def process_batch_queue(self):
        while True:
            now = datetime.now()
            if not self.batch_queue.empty() and (now - self.last_batch_time).total_seconds() >= self.batch_interval:
                self.last_batch_time = now
                batch = []
                while not self.batch_queue.empty():
                    batch.append(self.batch_queue.get())
                self.send_batch_notifications(batch)

    def send_batch_notifications(self, batch):
        try:
            # Use email for batched notifications
            notifier = NotifierFactory.get_notifier("email")
            notification_service = NotificationService(notifier)
            notification_service.notifier.send_batch(
                recipient=settings.DEFAULT_NOTIFICATION_RECIPIENT,
                subject="Batched Alert Notifications",
                alerts=batch
            )
            logger.info("Batched email sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send batched email: {e}")

    def run(self):
        logger.info("Running ConsumerWorker...")
        for message in self.consumer:
            alert_data = message.value
            alert = Alert(
                id=alert_data["id"],
                message=alert_data["message"],
                severity=alert_data["severity"],
                timestamp=alert_data.get("timestamp", "N/A")
            )
            logger.info(f"Processing alert: {alert.to_dict()}")

            # Evaluate risk score
            risk = self.risk_evaluator.evaluate_risk(alert)
            risk_score = risk["risk_score"]

            if risk_score > 50:
                # Send notifications to all specified channels
                for channel in settings.NOTIFICATION_CHANNELS:
                    try:
                        notifier = NotifierFactory.get_notifier(channel)
                        recipient = notifier.get_recipient()
                        notification_service = NotificationService(notifier)

                        notification_service.send_notification(
                            recipient=recipient,
                            subject=f"[SEVERITY: {alert.severity.upper()}] Immediate Alert Notification",
                            message=alert.message,
                            severity=alert.severity,
                            timestamp=alert.timestamp
                        )
                        logger.info(
                            f"Immediate {channel.upper()} notification sent successfully.")
                    except Exception as e:
                        logger.error(
                            f"Failed to send {channel.upper()} notification: {e}")

                self.consumer.commit()
            else:
                # Add to batch queue
                self.batch_queue.put(alert.to_dict())
                logger.info(f"Alert added to batch queue: {alert.id}")


if __name__ == "__main__":
    logger.info("Starting ConsumerWorker...")
    worker = ConsumerWorker()
    logger.info("ConsumerWorker initialized.")
    worker.run()
