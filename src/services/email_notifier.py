import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config.settings import settings


class EmailNotifier:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.logger = logging.getLogger(__name__)

    def send_email(self, recipient, subject, message, severity, timestamp):
        try:
            sender = "Secure Alerting <from@example.com>"

            with open("src/templates/alert_email_template.html", "r") as template_file:
                html_template = template_file.read()
            html_content = html_template.replace("{{ alert_message }}", message)\
                .replace("{{ alert_severity }}", severity)\
                .replace("{{ alert_timestamp }}", timestamp)

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
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
