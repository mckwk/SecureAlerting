from pydantic import BaseModel, Field, AnyHttpUrl, EmailStr, field_validator
from typing import List
import os


class Settings(BaseModel):
    KAFKA_BROKER_URL: str = Field(
        default=os.getenv("KAFKA_BROKER_URL", "broker:9093"),
        description="URL of the Kafka broker"
    )
    NOTIFICATION_TOPIC: str = Field(
        default=os.getenv("NOTIFICATION_TOPIC", "alert_notifications"),
        description="Kafka topic for notifications"
    )
    KAFKA_CONSUMER_GROUP: str = Field(
        default=os.getenv("KAFKA_CONSUMER_GROUP", "consumer_worker_group"),
        description="Kafka consumer group ID"
    )
    HOST: str = Field(
        default=os.getenv("HOST", "0.0.0.0"),
        description="Host address"
    )
    PORT: int = Field(
        default=int(os.getenv("PORT", 8000)),
        ge=1,
        le=65535,
        description="Port number (1-65535)"
    )
    ALLOW_ORIGINS: List[AnyHttpUrl] = Field(
        default_factory=lambda: os.getenv("ALLOW_ORIGINS", "*").split(","),
        description="List of allowed origins"
    )
    RISK_MODEL: str = Field(
        default=os.getenv("RISK_MODEL", "BaselineRiskModel"),
        description="Active risk model to use"
    )

    # SMTP Configuration
    SMTP_SERVER: str = Field(
        default=os.getenv("SMTP_SERVER", "sandbox.smtp.mailtrap.io"),
        description="SMTP server address"
    )
    SMTP_PORT: int = Field(
        default=int(os.getenv("SMTP_PORT", 2525)),
        ge=1,
        le=65535,
        description="SMTP server port"
    )
    SMTP_USER: EmailStr = Field(
        default=os.getenv("SMTP_USER"),
        description="SMTP username (must be a valid email)"
    )
    SMTP_PASSWORD: str = Field(
        default=os.getenv("SMTP_PASSWORD"),
        description="SMTP password"
    )
    EMAIL_SENDER: str = Field(
        default=os.getenv("EMAIL_SENDER", "Secure Alerting <from@example.com>"),
        description="Email sender address"
    )
    DEFAULT_NOTIFICATION_RECIPIENT: EmailStr = Field(
        default=os.getenv("DEFAULT_NOTIFICATION_RECIPIENT", "test_user@example.com"),
        description="Default recipient for notifications"
    )


    @field_validator("ALLOW_ORIGINS", mode="before")
    def validate_allow_origins(cls, value):
        if value == "*":
            return ["*"]
        return value


settings = Settings()
