from io import BytesIO

from PIL import Image
from flask import Response, request, send_file
import requests

IMAGE_ASSET_PATH = "resources/images/"
FONT_ASSET_PATH = "resources/fonts/"


class Handler:

    def __init__(self):
        self.request = request

    def __call__(self, *args):
        return Response(status=200)

    def get_image(self, url) -> Image:
        return Image.open(BytesIO(requests.get(url, stream=True).content))

    def get_image_asset(self, path) -> Image:
        return Image.open(IMAGE_ASSET_PATH + path)

    def get_image_response(self, frames) -> Response:
        f = "png" if len(frames) == 1 else "gif"

        b = BytesIO()
        frames[0].save(b, format=f, save_all=True, append_images=frames[1:], loop=0, optimize=True, disposal=2,
                       transparency=0)
        b.seek(0)

        return send_file(b, mimetype=f"image/{f}")
