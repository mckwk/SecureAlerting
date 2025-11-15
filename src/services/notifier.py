from abc import ABC, abstractmethod


class INotifier(ABC):
    @abstractmethod
    def send(self, recipient, subject, message, severity, timestamp):
        pass
