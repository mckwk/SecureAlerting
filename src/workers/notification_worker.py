from src.services.notifier import Notifier


class NotificationWorker:
    def __init__(self):
        self.notifier = Notifier()

    def process_alert(self, alert):
        self.notifier.send_notification(alert)
        self.notifier.send_email_notification(
            recipient="test_user@example.com",
            subject=f"Alert: {alert['severity']}",
            message=f"Message: {alert['message']}\nSeverity: {alert['severity']}"
        )
