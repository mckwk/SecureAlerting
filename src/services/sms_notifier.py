from src.services.notifier import INotifier


class SMSNotifier(INotifier):
    def send(self, recipient, subject, message, severity, timestamp):
        # Logic to send SMS
        print(f"Sending SMS to {recipient}: {message}")
