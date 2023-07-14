import re
import os
import time
import requests
import schedule
from PIL import Image, ImageOps
import pytesseract
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

IMAGES_URL = "https://services.swpc.noaa.gov/products/animations/ovation_north_24h.json"
BASE_URL = "https://services.swpc.noaa.gov"
MIN_STRENGTH_THRESHOLD = 70.0
RESET_TIME_HOURS = 12


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
    grayscaled = ImageOps.grayscale(cropped_image)
    strength = pytesseract.image_to_string(grayscaled)
    return try_parse_strength(strength)


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


class MaxKeeper:
    max_strength = 0.0
    max_set_at = None

    def handle_strength_update(self, strength: float):
        if strength > MIN_STRENGTH_THRESHOLD and strength > self.max_strength + 30:
            self.max_strength = strength
            self.max_set_at = datetime.now()
            send_aurora_text(strength)

    def check_should_clear_max(self):
        if not self.max_set_at:
            return False
        diff = datetime.now() - self.max_set_at
        timespan_in_seconds = 60 * 60 * RESET_TIME_HOURS
        return diff.total_seconds() > timespan_in_seconds

    def maybe_clear_max_strength(self):
        if self.max_set_at and self.check_should_clear_max():
            self.max_set_at = None
            self.max_strength = 0.0


def check_aurora(max_keeper: MaxKeeper):
    print("Checking aurora!")
    try:
        fetch_latest_image()
        strength = try_read_aurora()
        max_keeper.maybe_clear_max_strength()
        max_keeper.handle_strength_update(strength)
    except:
        pass


if __name__ == "__main__":
    max_keeper = MaxKeeper()
    schedule.every(5).minutes.do(check_aurora, max_keeper)
    schedule.every(1).day.do(send_uptime_text)

    while True:
        schedule.run_pending()
        time.sleep(1)
