import os


class Settings:
    KAFKA_BROKER_URL: str = os.getenv("KAFKA_BROKER_URL", "broker:9093")
    NOTIFICATION_TOPIC: str = os.getenv(
        "NOTIFICATION_TOPIC", "alert_notifications")
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", 8000))
    ALLOW_ORIGINS: list = os.getenv("ALLOW_ORIGINS", "*").split(",")

    # SMTP Configuration
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "sandbox.smtp.mailtrap.io")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 2525))
    SMTP_USER: str = os.getenv("SMTP_USER")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD")


settings = Settings()
