import smtplib
import ssl
from collections import namedtuple

Credentials = namedtuple('Credentials', 'username password')


class EmailSender:
    def __init__(self, port, smtp_address, credentials, ssl_enabled=False):
        self.port = port
        self.smtp_address = smtp_address
        self.ssl_enabled = ssl_enabled
        self.connection = None
        self.credentials = credentials

    def __enter__(self):
        if not self.ssl_enabled:
            self.connection = smtplib.SMTP(self.smtp_address, self.port)
        else:
            context = ssl.create_default_context()
            self.connection = smtplib.SMTP_SSL(self.smtp_address, self.port, context)
        self.connection.login(self.credentials.username, self.credentials.password)

        return self

    def sendmail(self, sender, receiver, message):
        try:
            self.connection.sendmail(sender, receiver, message.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connection:
            self.connection.quit()


