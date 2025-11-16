# Secure Alerting

Secure Alerting is a microservice designed to collect, process, and deliver alert notifications. It integrates with Kafka for publish-subscribe messaging and provides an API for managing alerts.


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

3. **Set up Docker Compose configuration:**
   Copy `docker-compose.example.yml` to `docker-compose.yml`:
   ```bash
   cp docker-compose.example.yml docker-compose.yml
   ```
   Replace placeholders (e.g., `<your-smtp-server>`, `<your-smtp-user>`) with your actual values.


4. ** Build and run the application using Docker Compose:**
   ```bash
   docker-compose up --build
   ```

6. **Access the API:**
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
- `NOTIFICATION_TOPIC`: Kafka topic for notifications (default: `alert_notifications`)
- `HOST`: Host for the FastAPI app (default: `0.0.0.0`)
- `PORT`: Port for the FastAPI app (default: `8000`)
- `SMTP_SERVER`: SMTP server for sending emails
- `SMTP_PORT`: SMTP server port
- `SMTP_USER`: SMTP username
- `SMTP_PASSWORD`: SMTP password

## Dependencies

The project uses the following Python libraries:

- `fastapi`
- `uvicorn`
- `kafka-python`
- `pydantic`
- `pytest`
- `requests`

Refer to `requirements.txt` for the full list.

