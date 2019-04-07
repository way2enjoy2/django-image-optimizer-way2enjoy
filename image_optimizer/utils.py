# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from io import BytesIO
from PIL import Image

import way2E
import requests

from .settings import (OPTIMIZED_IMAGE_METHOD, WAY2ENJOY_KEY)


def image_optimizer(image_data):
    """Optimize an image that has not been saved to a file."""
    if OPTIMIZED_IMAGE_METHOD == 'pillow':
        image = Image.open(image_data)
        bytes_io = BytesIO()
        if image_data.name.split('.')[-1].lower() != 'jpg':
            extension = image_data.name.split('.')[-1].upper()
        else:
            extension = 'JPEG'
        image.save(bytes_io, format=extension, optimize=True)
        image_data.seek(0)
        image_data.file.write(bytes_io.getvalue())
        image_data.file.truncate()
    elif OPTIMIZED_IMAGE_METHOD == 'way2enjoy':
        # disable warning info
        requests.packages.urllib3.disable_warnings()

        way2E.key = WAY2ENJOY_KEY
        optimized_buffer = way2E.from_buffer(image_data.file.read()).to_buffer()
        image_data.seek(0)
        image_data.file.write(optimized_buffer)
        image_data.file.truncate()
    return image_data
