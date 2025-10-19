from typing import Optional

from pydantic import BaseModel


class AlertSchema(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    timestamp: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "id": "12345",
                "title": "Example notification",
                "description": "Blablabla",
                "severity": "high",
                "timestamp": "2025-12-17T12:00:00Z"
            }
        }
