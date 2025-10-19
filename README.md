# Secure Alerting

Secure Alerting is a microservice designed to collect, process, and deliver alert notifications in real-time. It integrates with Kafka for publish-subscribe messaging and provides a FastAPI-based REST API for managing alerts.

## Project Structure

```
secure-alerting
├── src
│   ├── app.py                  # Entry point of the application
│   ├── api
│   │   └── routes.py           # API routes for alert notifications
│   ├── services
│   │   ├── kafka_consumer.py   # Kafka consumer for incoming alerts
│   │   ├── kafka_producer.py   # Kafka producer for sending notifications
│   │   └── notifier.py         # Logic for processing and sending notifications
│   ├── models
│   │   └── alert.py            # Alert model definition
│   ├── schemas
│   │   └── alert_schema.py     # Pydantic schema for alert validation
│   ├── config
│   │   └── settings.py         # Configuration settings
│   ├── workers
│   │   └── consumer_worker.py  # Background worker for consuming Kafka messages
├── tests
│   └── test_notifications.py   # Unit tests for notifications and Kafka integration
├── Dockerfile                  # Instructions for building the Docker image
├── docker-compose.yml          # Defines services and dependencies for Docker
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
└── README.md                   # Project documentation
```


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

3. **Build the Docker image:**
   ```bash
   docker build -t secure-alerting .
   ```

4. **Run the application using Docker Compose:**
   ```bash
   docker-compose up
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
  "status": "Notification sent"
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

## Testing

Run the tests using `pytest`:
```bash
pytest
```

## Configuration

The application uses environment variables for configuration. Key variables include:

- `KAFKA_BROKER_URL`: Kafka broker URL (default: `broker:9093`)
- `NOTIFICATION_TOPIC`: Kafka topic for notifications (default: `alert_notifications`)
- `HOST`: Host for the FastAPI app (default: `0.0.0.0`)
- `PORT`: Port for the FastAPI app (default: `8000`)

## Dependencies

The project uses the following Python libraries:

- `fastapi`
- `uvicorn`
- `kafka-python`
- `pydantic`
- `pytest`
- `requests`

Refer to `requirements.txt` for the full list.

