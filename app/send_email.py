import os
import smtplib


def send_email(key, to):
    text = f'Hello! You have Notification with message: {key}'
    subj = 'Sender Notifications'
    body = "\r\n".join((f"From: {os.getenv('SMTP_LOGIN')}", f"To: {to}", f"Subject: {subj}", 'MIME-Version: 1.0', 'Content-Type: text/plain; charset=utf-8', "", text))
    try:
        smtp = smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT'))
        smtp.starttls()
        smtp.ehlo()
        smtp.login(os.getenv('SMTP_LOGIN'), os.getenv('SMTP_PASSWORD'))
        smtp.sendmail(os.getenv('SMTP_LOGIN'), to, body.encode('utf-8'))
        print('succesfuly send')
    except smtplib.SMTPException as e:
        print(e)
    finally:
        smtp.quit()
