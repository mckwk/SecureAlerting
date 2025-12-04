from datetime import datetime
import html


class Alert:
    def __init__(self, id: str, message: str, severity: str, timestamp: str):
        self.id = html.escape(str(id))
        self.message = html.escape(message)
        self.severity = html.escape(severity)
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() if isinstance(self.timestamp, datetime) else self.timestamp,
        }
