import os
import imgkit


def image_from_string(string, filename):
    if os.getenv('XVFB_LOCATION'):
        config = imgkit.config(xvfb=os.getenv('XVFB_LOCATION'))
        imgkit.from_string(string, filename, config=config)
    else:
        imgkit.from_string(string, filename)
