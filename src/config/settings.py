import os


class Settings:
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL", "broker:9093")
    NOTIFICATION_TOPIC: str = os.getenv(
        "NOTIFICATION_TOPIC", "alert_notifications")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    ALLOW_ORIGINS: list = os.getenv("ALLOW_ORIGINS", "*").split(",")


settings = Settings()
