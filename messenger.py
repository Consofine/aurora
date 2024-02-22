import os
from twilio.rest import Client
from envelope import Envelope
from pathlib import Path


def check_env_vars(env_vars: list):
    for item in env_vars:
        value = (
            os.environ.get(item[0], item[1])
            if type(item) is tuple
            else os.environ.get(item)
        )
        if not value:
            raise Exception(
                "missing env var: {}".format(item[0] if type(item) is tuple else item)
            )


def send_email(body: str, subject: str | None = None, to_email: str | None = None):
    check_env_vars(["FROM_EMAIL", "FROM_EMAIL_PASSWORD", ("TO_EMAIL", to_email)])

    gpg_key_path = os.environ.get("GPG_PUB_KEY_PATH")
    if not gpg_key_path:
        print(
            "Warning: you are sending unencrypted email. Consider adding a GPG_PUB_KEY_PATH env var to encrypt."
        )

    res = Envelope(
        subject=subject,
        subject_encrypted="nunya" if gpg_key_path else None,
        message=body,
        encrypt=Path(gpg_key_path) if gpg_key_path else None,
        from_=os.environ.get("FROM_EMAIL"),
        smtp={
            "host": "smtp.gmail.com",
            "port": 587,
            "user": os.environ.get("FROM_EMAIL"),
            "password": os.environ.get("FROM_EMAIL_PASSWORD"),
        },
        to=to_email or os.environ.get("TO_EMAIL"),
        send=True,
    )


def send_aurora_email(strength: float):
    message = "Aurora is active! Predicted strength is {} GW".format(strength)
    send_email(message, subject="Aurora Active!")


def send_uptime_email():
    send_email("Aurora still running :)")


def send_text(body, to_number=None):
    check_env_vars(
        [
            "TWILIO_ACCOUNT_SID",
            "TWILIO_AUTH_TOKEN",
            "TWILIO_FROM_NUMBER",
            ("TWILIO_TO_NUMBER", to_number),
        ]
    )

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
