import os
import smtplib
import logging


class Sender:
    def __init__(self) -> None:
        self.logger = logging.getLogger()
        self.login = os.getenv('SMTP_LOGIN')
        self.password = os.getenv('SMTP_PASSWORD')
        self.host = os.getenv('SMTP_HOST')
        self.port = os.getenv('SMTP_PORT')
        self.subj = 'Sender Notifications'

    def send_email(self, key, dest):
        text = f'Hello! You have Notification with message: {key}'
        body = "\r\n".join((f"From: {self.login}", f"To: {dest}", f"Subject: {self.subj}", 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=utf-8', "", text))
        try:
            smtp = smtplib.SMTP(self.host, self.port)
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.login, self.password)
            smtp.sendmail(self.login, dest, body.encode('utf-8'))
            self.logger.info('Send Succusefuly')
        except smtplib.SMTPException as e:
            self.logger.warning(f'current mistake is {e}')
        finally:
            smtp.quit()
