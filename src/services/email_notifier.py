import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.config.settings import settings
from src.services.notifier import INotifier


class EmailNotifier(INotifier):
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.logger = logging.getLogger(__name__)

    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(smtplib.SMTPException),
    )
    def send(self, recipient, subject, message, severity, timestamp):
        try:
            sender = settings.EMAIL_SENDER

            env = Environment(loader=FileSystemLoader('src/templates'))
            template = env.get_template('alert_email_template.html')
            html_content = template.render(
                alert_message=message,
                alert_severity=severity,
                alert_timestamp=timestamp
            )

            msg = MIMEMultipart("alternative")
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = recipient
            msg.attach(MIMEText(html_content, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(sender, recipient, msg.as_string())

            self.logger.info(f"Email sent to {recipient}")
        except smtplib.SMTPException as e:
            self.logger.error(f"SMTP error occurred: {e}")
            raise  # Reraise the exception to trigger retry logic
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            raise  # Reraise the exception to ensure proper handling
