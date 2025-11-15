from src.services.email_notifier import EmailNotifier
from src.services.sms_notifier import SMSNotifier


class NotifierFactory:
    @staticmethod
    def get_notifier(notifier_type: str):
        if notifier_type == "email":
            return EmailNotifier()
        elif notifier_type == "sms":
            return SMSNotifier()
        else:
            raise ValueError(f"Unknown notifier type: {notifier_type}")
