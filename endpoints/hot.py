from PIL import ImageSequence, Image
from requests.exceptions import MissingSchema, ConnectionError

from handler import Handler

from utility.response import BadRequest


class HotHandler(Handler):

    def __call__(self):
        image_url = self.query("image")
        if not image_url:
            return BadRequest("Image query not given")

        try:
            image = self.get_image(image_url)
        except MissingSchema:
            return BadRequest("Url could not be formed to an image")
        except ConnectionError:
            return BadRequest("Site took too long to respond")

        background = self.get_image_asset("thats-hot-meme.png")
        blank = Image.new("RGBA", background.size, (255, 255, 255, 0))

        frames = []
        for frame in ImageSequence.Iterator(image):
            frame = frame.convert("RGBA").resize((400, 300))

            blank = blank.copy()
            blank.paste(frame, (8, 213), frame)
            blank.paste(background, (0, 0), background)

            frames.append(blank)

        return self.get_image_response(frames)