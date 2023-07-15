import asyncio
from io import BytesIO
import requests
import pytesseract
from PIL import Image, ImageOps
from constants import BASE_URL, IMAGES_URL
from helpers import try_parse_strength


async def _fetch_latest_images(limit: int):
    """
    Returns the binary for the most recent Aurora image
    """

    async def fetch_image_iteration(iteration: int):
        latest_image_url = "{}{}".format(BASE_URL, image_list[-1 - iteration]["url"])
        resp = requests.get(latest_image_url)
        return Image.open(BytesIO(resp.content))

    image_list = requests.get(IMAGES_URL).json()
    num_iterations = min(limit, len(image_list))
    images = await asyncio.gather(
        *[fetch_image_iteration(iteration) for iteration in range(num_iterations)]
    )
    return images


async def _try_read_auroras(images: list[Image.Image], optimize: bool):
    async def get_strength(image: Image):
        strength = pytesseract.image_to_string(image)
        return try_parse_strength(strength)

    async def process_and_read_image(image: Image.Image, iteration: int):
        try:
            cropped_image = image.crop((565, 20, 633, 46))
            strength = None
            if optimize:
                grayscaled = ImageOps.grayscale(cropped_image)
                strength = await get_strength(grayscaled)
            else:
                strength = await get_strength(cropped_image)
            print("{}) Strength: {}".format(iteration, strength))
        except:
            print("{}) Error!".format(iteration))

    async with asyncio.TaskGroup() as tg:
        for iteration, image in enumerate(images):
            tg.create_task(process_and_read_image(image, iteration))


async def test_accuracy(limit: int):
    images = await _fetch_latest_images(limit)
    # non-optimized pass
    print("##### NON-OPTIMIZED #####")
    await _try_read_auroras(images, False)
    # optimized pass
    print("##### OPTIMIZED #####")
    await _try_read_auroras(images, True)
