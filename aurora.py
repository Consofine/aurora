import requests
import pytesseract
from PIL import Image, ImageOps
from io import BytesIO
from constants import BASE_URL, IMAGES_URL
from helpers import try_parse_strength
from max_keeper import MaxKeeper
from messenger import send_aurora_text


def fetch_latest_image():
    """
    Returns the binary for the most recent Aurora image
    """
    images = requests.get(IMAGES_URL).json()
    latest_image_url = "{}{}".format(BASE_URL, images[-1]["url"])
    resp = requests.get(latest_image_url)
    return Image.open(BytesIO(resp.content))


def try_read_aurora(image: Image):
    """
    Args:
        - image: Image -- the PIL image to process
    Returns:
        strength: float -- the strength extracted from the image
    Throws:
        ValueError -- allows ValueError to bubble up if strength
        extracted from image is not cast-able to a float.
    """
    cropped_image = image.crop((565, 20, 633, 46))
    grayscaled = ImageOps.grayscale(cropped_image)
    strength = pytesseract.image_to_string(grayscaled)
    return try_parse_strength(strength)


def check_aurora(max_keeper: MaxKeeper):
    print("Checking aurora!")
    try:
        image = fetch_latest_image()
        strength = try_read_aurora(image)
        max_keeper.maybe_clear_max_strength()
        if max_keeper.should_update_strength(strength):
            max_keeper.update_strength(strength)
            send_aurora_text(strength)
    except:
        pass
