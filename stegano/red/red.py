#!/usr/bin/env python
# Stegano - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2024  Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2010/10/01 $"
__revision__ = "$Date: 2017/02/06 $"
__license__ = "GPLv3"

from typing import IO, Union, cast

from stegano import tools


def hide(input_image: Union[str, IO[bytes]], message: str):
    """
    Hide a message (string) in an image.

    Use the red portion of a pixel (r, g, b) tuple to
    hide the message string characters as ASCII values.
    The red value of the first pixel is used for message_length of the string.
    """
    message_length = len(message)
    assert message_length != 0, "message message_length is zero"
    assert message_length < 255, "message is too long"
    img = tools.open_image(input_image)
    # Ensure image mode is RGB
    if img.mode != "RGB":
        img = img.convert("RGB")
    # Use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            pixel = cast(tuple[int, int, int], img.getpixel((col, row)))
            r, g, b = pixel
            # first value is message_length of message
            if row == 0 and col == 0 and index < message_length:
                asc = message_length
            elif index <= message_length:
                c = message[index - 1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g, b))
            index += 1
    img.close()
    return encoded


def reveal(input_image: Union[str, IO[bytes]]):
    """
    Find a message in an image.

    Check the red portion of an pixel (r, g, b) tuple for
    hidden message characters (ASCII values).
    The red value of the first pixel is used for message_length of string.
    """
    img = tools.open_image(input_image)
    # Ensure image mode is RGB
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    message = ""
    index = 0
    for row in range(height):
        for col in range(width):
            pixel = cast(tuple[int, int, int], img.getpixel((col, row)))
            r, g, b = pixel
            # First pixel r value is length of message
            if row == 0 and col == 0:
                message_length = r
            elif index <= message_length:
                message += chr(r)
            index += 1
    img.close()
    return message
