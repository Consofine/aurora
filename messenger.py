import os
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText


def send_email(body, subject=None, to_email=None):
    sender = os.environ.get("FROM_EMAIL")
    receiver = to_email or os.environ.get("TO_EMAIL")
    message = MIMEText(body)
    message["Subject"] = subject or "Aurora Update"
    message["From"] = sender
    message["To"] = receiver
    smtp = smtplib.SMTP_SSL("127.0.0.1", 1025)
    # this is the pseudo-password (hashed?) from protonmail-bridge,
    # NOT your actual email password
    smtp.login(sender, os.environ.get("FROM_EMAIL_PASSWORD"))
    smtp.sendmail(sender, [receiver], message.as_string())


def send_aurora_email(strength: float):
    message = "Aurora is active! Predicted strength is {} GW".format(strength)
    send_email(message, subject="Aurora Active!")


def send_uptime_email():
    send_email("Aurora still running :)")


def send_text(body, to_number=None):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM_NUMBER")
    to_number = to_number or os.environ.get("TWILIO_TO_NUMBER")

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to_number,
        from_=from_number,
        body=body,
    )


def send_aurora_text(strength: float):
    message = "Aurora is active! Predicted strength is {} GW".format(strength)
    send_text(message)


def send_uptime_text():
    send_text("Aurora still running :)")
