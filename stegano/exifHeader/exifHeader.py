#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2026 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://github.com/cedricbonhomme/Stegano
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.2.2 $"
__date__ = "$Date: 2016/05/26 $"
__revision__ = "$Date: 2017/01/18 $"
__license__ = "GPLv3"

import piexif

from stegano import tools


def hide(
    input_image_file,
    img_enc,
    secret_message=None,
    secret_file=None,
    img_format=None,
):
    """Hide a message (string) in an image."""
    from base64 import b64encode
    from zlib import compress

    if secret_file is not None:
        with open(secret_file, "rb") as f:
            secret_message = f.read()

    try:
        text = compress(b64encode(bytes(secret_message, "utf-8")))
    except Exception:
        text = compress(b64encode(secret_message))

    img = tools.open_image(input_image_file)

    if img_format is None:
        img_format = img.format

    if "exif" in img.info:
        exif_dict = piexif.load(img.info["exif"])
    else:
        exif_dict = {}
        exif_dict["0th"] = {}
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = text
    exif_bytes = piexif.dump(exif_dict)
    img.save(img_enc, format=img_format, exif=exif_bytes)
    img.close()
    return img


def reveal(input_image_file):
    """Find a message in an image."""
    from base64 import b64decode
    from zlib import decompress

    img = tools.open_image(input_image_file)

    try:
        if img.format in ["JPEG", "TIFF"]:
            if "exif" in img.info:
                exif_dict = piexif.load(img.info.get("exif", b""))
                description_key = piexif.ImageIFD.ImageDescription
                encoded_message = exif_dict["0th"][description_key]
            else:
                encoded_message = b""
        else:
            raise ValueError("Given file is neither JPEG nor TIFF.")
    finally:
        img.close()

    return b64decode(decompress(encoded_message))
