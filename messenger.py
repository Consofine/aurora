import os
from twilio.rest import Client


def send_text(body, to_number=None):
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM_NUMBER")
    to_number = to_number if to_number else os.environ.get("TWILIO_TO_NUMBER")

    client = Client(account_sid, auth_token)

    client.messages.create(
        to=to_number,
        from_=from_number,
        body=body,
    )


def send_aurora_text(strength: float):
    print("Sending aurora text for strength {}".format(strength))
    message = "Aurora is active! Predicted strength is {} GW".format(strength)
    send_text(message)


def send_uptime_text():
    print("Sending uptime text")
    send_text("Aurora still running :)")
