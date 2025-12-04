from twilio.rest import Client

from src.config.settings import settings
from src.services.notifier import INotifier


class SMSNotifier(INotifier):
    def __init__(self):
        self.twilio_client = Client(
            settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.twilio_phone_number = settings.TWILIO_PHONE_NUMBER

    def send(self, recipient, subject, message, severity, timestamp):
        try:
            body = f"Alert: [{severity.upper()}] {message} (Timestamp: {timestamp})"
            message = self.twilio_client.messages.create(
                body=body,
                from_=self.twilio_phone_number,
                to=recipient
            )
            print(f"SMS sent successfully. SID: {message.sid}")
        except Exception as e:
            raise Exception(f"Failed to send SMS: {e}")

    def get_recipient(self):
        return settings.SMS_RECIPIENT
