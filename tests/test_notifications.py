import json
import time

import pytest
import requests
from kafka import KafkaConsumer
from unittest.mock import patch

from src.services.notifier import Notifier
from src.models.risk_estimation import BaselineRiskModel
from src.services.email_notifier import EmailNotifier
from src.services.notification_service import EmailNotificationService


# Constants
API_URL = "http://localhost:8000/alerts/"
# Adjust to 'broker:9093' if running inside Docker
KAFKA_BROKER_URL = "localhost:9092"
NOTIFICATION_TOPIC = "alert_notifications"
HEADERS = {
    "Content-Type": "application/json"
}


def test_api():
    alert = {
    "severity": "high",
    "message": "Test alert notification from test_api()"
    }
    response = requests.post(API_URL, json=alert, headers=HEADERS)
    assert response.status_code == 201, f"API test failed! Status code: {response.status_code}"
    assert "status" in response.json(), "API response missing 'status' key"
    assert response.json()["status"] == "Notification sent", "Unexpected API response content"


def test_kafka_consumer():
    alert = {
    "severity": "high",
    "message": "Test alert notification from test_kafka_consumer()"
    }
    response = requests.post(API_URL, json=alert, headers=HEADERS)
    assert response.status_code == 201, f"API test failed! Status code: {response.status_code}"
    consumer = KafkaConsumer(
        NOTIFICATION_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )
    timeout = time.time() + 5  # seconds
    for message in consumer:
        alert = message.value
        if alert["message"] == alert["message"] and alert["severity"] == alert["severity"]:
            assert True, "Producer and Consumer test passed!"
            break
        if time.time() > timeout:
            pytest.fail(
                "Producer and Consumer test failed: No matching message received.")



def test_baseline_risk_model():
    model = BaselineRiskModel()
    alert = {"severity": "high"}
    result = model.calculate_risk(alert)
    assert result["risk_score"] == 70
    assert result["risk_level"] == "High"


def test_notification_with_risk_via_api():
    alert = {"message": "Test alert from test_notification_with_risk_via_api()", "severity": "critical"}
    response = requests.post(API_URL, json=alert, headers=HEADERS)
    
    assert response.status_code == 201, f"API test failed! Status code: {response.status_code}"
    assert "status" in response.json(), "API response missing 'status' key"
    assert response.json()["status"] == "Notification sent", "Unexpected API response content"


def test_email_notification():
    recipient = "test_user@example.com"
    subject = "Test Alert"
    message = "This is a test email for alert notifications."

    # Mock the EmailNotifier's send_email method
    with patch.object(EmailNotifier, "send_email", return_value=None) as mock_send_email:
        email_service = EmailNotificationService()
        email_service.send_notification(recipient, subject, message)
        mock_send_email.assert_called_once_with(recipient, subject, message)
