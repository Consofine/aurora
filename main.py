import re
import os
import time
import requests
import schedule
from PIL import Image
import pytesseract
from twilio.rest import Client


IMAGES_URL = "https://services.swpc.noaa.gov/products/animations/ovation_north_24h.json"
BASE_URL = "https://services.swpc.noaa.gov"


def try_parse_strength(strength):
    """
    Attempts to parse the given string into a float. Will let
    error bubble up if `strength` is not convertible into float.
    """
    cleaned_strength = re.sub(r"[^0-9.]", r"", strength)
    return float(cleaned_strength)


def fetch_latest_image():
    """
    Returns the binary for the most recent Aurora image
    """
    images = requests.get(IMAGES_URL).json()
    latest_image_url = "{}{}".format(BASE_URL, images[-1]["url"])
    latest_image = requests.get(latest_image_url).content
    with open("aurora.jpg", "wb+") as f:
        f.write(latest_image)


def try_read_aurora():
    """
    Loads an image at a predetermined path './aurora.jpg'
    into Tesseract and returns the aurora strength in GW
    """
    image = Image.open("aurora.jpg")
    cropped_image = image.crop((565, 20, 633, 46))
    strength = pytesseract.image_to_string(cropped_image)
    return try_parse_strength(strength)


def send_text(body, to_number):
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


def maybe_send_aurora_text(strength: float):
    if strength > 70.0:
        message = "Aurora is active! Predicted strength is {} GW".format(strength)
        send_text(message)
    return


def check_aurora():
    try:
        fetch_latest_image()
        strength = try_read_aurora()
        maybe_send_aurora_text(strength)
    except:
        pass


def send_uptime_text():
    send_text("Aurora still running :)")


if __name__ == "__main__":
    schedule.every(5).minutes.do(check_aurora)
    schedule.every(1).day.do(send_uptime_text)

    while True:
        schedule.run_pending()
        time.sleep(1)
