# Secure Alerting

Secure Alerting is a microservice designed to collect, process, and deliver alert notifications. It integrates with Kafka for publish-subscribe messaging and provides an API for managing alerts. Notifications can now be sent via multiple channels, including email (all alert levels - single and batched notifications) and SMS (high and critial notifications).


## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed
- Kafka and Zookeeper services (configured in `docker-compose.yml`)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mckwk/SecureAlerting
   ```

2. **Set up environment variables:**
   Copy `.env.example` to `.env` and update the values as needed:
   ```bash
   cp .env.example .env
   ```

   Key environment variables for notifications:
   - `NOTIFICATION_CHANNELS`: Comma-separated list of notification channels (e.g., `email,sms`).
   - `DEFAULT_NOTIFICATION_RECIPIENT`: Default email recipient for notifications.
   - `SMS_RECIPIENT`: Default phone number for SMS notifications.
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`: Twilio credentials for SMS notifications.

3. **Set up Docker Compose configuration:**
   Copy `docker-compose.example.yml` to `docker-compose.yml`:
   ```bash
   cp docker-compose.example.yml docker-compose.yml
   ```
   Replace placeholders (e.g., `<your-smtp-server>`, `<your-smtp-user>`) with your actual values.


4. **Build and run the application using Docker Compose:**
   ```bash
   docker-compose up --build
   ```

5. **Access the API:**
   The API will be available at `http://localhost:8000`.

## API Endpoints

### Create an Alert
**POST** `/alerts/`

Request Body:
```json
{
  "message": "Test alert",
  "severity": "high"
}
```

Response:
```json
{
  "status": "Alert published to Kafka"
}
```

### Get All Alerts
**GET** `/alerts/`

Response:
```json
[
  {
    "id": 1,
    "message": "Test alert",
    "severity": "high"
  }
]
```

### Get Alert by ID
**GET** `/alerts/{alert_id}`

Response:
```json
{
  "id": 1,
  "message": "Test alert",
  "severity": "high"
}
```

## Configuration

The application uses environment variables for configuration. Key variables include:

- `KAFKA_BROKER_URL`: Kafka broker URL (default: `broker:9093`)
- `KAFKA_CONSUMER_GROUP`: Kafka consumer group name (default: `consumer_worker_group`)
- `NOTIFICATION_TOPIC`: Kafka topic for notifications (default: `alert_notifications`)
- `HOST`: Host for the FastAPI app (default: `0.0.0.0`)
- `PORT`: Port for the FastAPI app (default: `8000`)
- `ALLOW_ORIGINS`: Allowed origins for CORS (default: `*`)
- `PYTHONPATH`: Python path for the application (default: `.`)
- `RISK_MODEL`: Risk evaluation model to use (default: `BaselineRiskModel`)
- `SMTP_SERVER`: SMTP server for sending emails
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password
- `EMAIL_SENDER`: Email sender address (e.g., `"SecureAlerting <secure@alerting.com>")
- `DEFAULT_NOTIFICATION_RECIPIENT`: Default email recipient for notifications
- `BATCH_NOTIFICATION_INTERVAL`: Interval in seconds for sending batched notifications (default: `120`)
- `TWILIO_ACCOUNT_SID`: Twilio Account SID for SMS notifications
- `TWILIO_AUTH_TOKEN`: Twilio Auth Token for SMS notifications
- `TWILIO_PHONE_NUMBER`: Twilio phone number for sending SMS
- `SMS_RECIPIENT`: Default phone number for SMS notifications
- `NOTIFICATION_CHANNELS`: Comma-separated list of notification channels (e.g., `email,sms`)

## Dependencies

Refer to `requirements.txt` for the full list.

