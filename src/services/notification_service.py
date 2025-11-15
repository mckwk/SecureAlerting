from abc import ABC, abstractmethod

from src.services.notifier import INotifier


class INotificationService(ABC):
    @abstractmethod
    def send_notification(self, recipient, subject, message, severity, timestamp):
        pass


class NotificationService(INotificationService):
    def __init__(self, notifier: INotifier):
        self.notifier = notifier

    def send_notification(self, recipient, subject, message, severity, timestamp):
        self.notifier.send(recipient, subject, message, severity, timestamp)
