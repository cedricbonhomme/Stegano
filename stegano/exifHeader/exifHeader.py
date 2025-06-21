#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2025 Cédric Bonhomme - https://www.cedricbonhomme.org
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


if __name__ == "__main__":
    # Point of entry in execution mode.
    # TODO: improve the management of arguments
    from optparse import OptionParser

    parser = OptionParser(version=__version__)
    parser.add_option(
        "--hide",
        action="store_true",
        default=False,
        help="Hides a message in an image.",
    )
    parser.add_option(
        "--reveal",
        action="store_true",
        default=False,
        help="Reveals the message hided in an image.",
    )
    # Original image
    parser.add_option(
        "-i", "--input", dest="input_image_file", help="Input image file."
    )
    # Image containing the secret
    parser.add_option(
        "-o",
        "--output",
        dest="output_image_file",
        help="Output image containing the secret.",
    )

    # Secret raw message to hide
    parser.add_option(
        "-m",
        "--secret-message",
        dest="secret_message",
        help="Your raw secret message to hide.",
    )

    # Secret text file to hide.
    parser.add_option(
        "-f",
        "--secret-file",
        dest="secret_file",
        help="Your secret text file to hide.",
    )

    parser.set_defaults(
        input_image_file="./pictures/Elisha-Cuthbert.jpg",
        output_image_file="./pictures/Elisha-Cuthbert_enc.jpg",
        secret_message="",
        secret_file="",
    )

    (options, args) = parser.parse_args()

    if options.hide:
        if options.secret_message != "" and options.secret_file == "":
            hide(
                input_image_file=options.input_image_file,
                img_enc=options.output_image_file,
                secret_message=options.secret_message,
            )
        elif options.secret_message == "" and options.secret_file != "":
            hide(
                input_image_file=options.input_image_file,
                img_enc=options.output_image_file,
                secret_file=options.secret_file,
            )

    elif options.reveal:
        reveal(input_image_file=options.input_image_file)
