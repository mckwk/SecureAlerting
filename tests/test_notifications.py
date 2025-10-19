import json
import time

import pytest
import requests
from kafka import KafkaConsumer

# Constants
API_URL = "http://localhost:8000/alerts/"
# Adjust to 'broker:9093' if running inside Docker
KAFKA_BROKER_URL = "localhost:9092"
NOTIFICATION_TOPIC = "alert_notifications"
PAYLOAD = {
    "severity": "high",
    "message": "Test alert notification"
}
HEADERS = {
    "Content-Type": "application/json"
}


@pytest.fixture
def api_response():
    response = requests.post(API_URL, json=PAYLOAD, headers=HEADERS)
    return response


def test_api(api_response):
    assert api_response.status_code == 201, f"API test failed! Status code: {
        api_response.status_code}"
    assert "status" in api_response.json(), "API response missing 'status' key"
    assert api_response.json(
    )["status"] == "Notification sent", "Unexpected API response content"


def test_kafka_consumer():
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
        if alert["message"] == PAYLOAD["message"] and alert["severity"] == PAYLOAD["severity"]:
            assert True, "Producer and Consumer test passed!"
            break
        if time.time() > timeout:
            pytest.fail(
                "Producer and Consumer test failed: No matching message received.")
