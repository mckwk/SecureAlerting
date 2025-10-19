class Alert:
    def __init__(self, id: str, message: str, severity: str, timestamp: str):
        self.id = id
        self.message = message
        self.severity = severity
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "id": self.id,
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }
