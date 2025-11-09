from abc import ABC, abstractmethod

from src.services.email_notifier import EmailNotifier


class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient, subject, message):
        pass


class EmailNotificationService(INotificationService):
    def __init__(self):
        self.email_notifier = EmailNotifier()

    def send_notification(self, recipient, subject, message):
        self.email_notifier.send_email(recipient, subject, message)
