from io import BytesIO
from typing import Optional

import requests
from PIL import Image
from flask import Response, send_file

IMAGE_ASSET_PATH = "resources/images/"
FONT_ASSET_PATH = "resources/fonts/"


def get_image(url: str) -> Image:
    return Image.open(BytesIO(requests.get(url, stream=True).content))


def get_image_asset(path: str) -> Image:
    return Image.open(IMAGE_ASSET_PATH + path)


def get_image_response(frames: [Image], transparency: int=0) -> Response:
    png = len(frames) == 1
    f = "png" if png else "gif"

    b = BytesIO()
    if png:
        frames[0].save(b, format=f)
    else:
        frames[0].save(b, format=f, save_all=True, append_images=frames[1:], loop=0, optimize=True, disposal=2, transparency=transparency)

    b.seek(0)

    return send_file(b, mimetype=f"image/{f}")
