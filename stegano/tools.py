#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2024 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://git.sr.ht/~cedric/stegano
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
__version__ = "$Revision: 0.3 $"
__date__ = "$Date: 2010/10/01 $"
__revision__ = "$Date: 2017/05/04 $"
__license__ = "GPLv3"

import base64
import itertools
from functools import reduce
from typing import IO, List, Union

from PIL import Image

ENCODINGS = {"UTF-8": 8, "UTF-32LE": 32}


def a2bits(chars: str) -> str:
    """Converts a string to its bits representation as a string of 0's and 1's.

    >>> a2bits("Hello World!")
    '010010000110010101101100011011000110111100100000010101110110111101110010011011000110010000100001'
    """
    return bin(reduce(lambda x, y: (x << 8) + y, (ord(c) for c in chars), 1))[3:]


def a2bits_list(chars: str, encoding: str = "UTF-8") -> List[str]:
    """Convert a string to its bits representation as a list of 0's and 1's.

    >>>  a2bits_list("Hello World!")
    ['01001000',
    '01100101',
    '01101100',
    '01101100',
    '01101111',
    '00100000',
    '01010111',
    '01101111',
    '01110010',
    '01101100',
    '01100100',
    '00100001']
    >>> "".join(a2bits_list("Hello World!"))
    '010010000110010101101100011011000110111100100000010101110110111101110010011011000110010000100001'
    """
    return [bin(ord(x))[2:].rjust(ENCODINGS[encoding], "0") for x in chars]


def bs(s: int) -> str:
    """Converts an int to its bits representation as a string of 0's and 1's."""
    return str(s) if s <= 1 else bs(s >> 1) + str(s & 1)


def setlsb(component: int, bit: str) -> int:
    """Set Least Significant Bit of a colour component."""
    return component & ~1 | int(bit)


def n_at_a_time(items: List[int], n: int, fillvalue: str):
    """Returns an iterator which groups n items at a time.
    Any final partial tuple will be padded with the fillvalue

    >>> list(n_at_a_time([1, 2, 3, 4, 5], 2, 'X'))
    [(1, 2), (3, 4), (5, 'X')]
    """
    it = iter(items)
    return itertools.zip_longest(*[it] * n, fillvalue=fillvalue)


def binary2base64(binary_file: str) -> str:
    """Convert a binary file (OGG, executable, etc.) to a
    printable string.
    """
    # Use mode = "rb" to read binary file
    with open(binary_file, "rb") as bin_file:
        encoded_string = base64.b64encode(bin_file.read())
    return encoded_string.decode()


def base642binary(b64_fname: str) -> bytes:
    """Convert a printable string to a binary file."""
    b64_fname += "==="
    return base64.b64decode(b64_fname)


def open_image(fname_or_instance: Union[str, IO[bytes]]):
    """Opens a Image and returns it.

    :param fname_or_instance: Can either be the location of the image as a
                              string or the Image.Image instance itself.
    """
    if isinstance(fname_or_instance, Image.Image):
        return fname_or_instance

    return Image.open(fname_or_instance)


class Hider:
    def __init__(
        self,
        input_image: Union[str, IO[bytes]],
        message: str,
        encoding: str = "UTF-8",
        auto_convert_rgb: bool = False,
    ):
        self._index = 0

        message_length = len(message)
        assert message_length != 0, "message length is zero"

        image = open_image(input_image)

        if image.mode not in ["RGB", "RGBA"]:
            if not auto_convert_rgb:
                print(f"The mode of the image is not RGB. Mode is {image.mode}")
                answer = input("Convert the image to RGB ? [Y / n]\n") or "Y"
                if answer.lower() == "n":
                    raise Exception("Not a RGB image.")

            image = image.convert("RGB")

        self.encoded_image = image.copy()
        image.close()

        message = str(message_length) + ":" + str(message)
        self._message_bits = "".join(a2bits_list(message, encoding))
        self._message_bits += "0" * ((3 - (len(self._message_bits) % 3)) % 3)

        width, height = self.encoded_image.size
        npixels = width * height
        self._len_message_bits = len(self._message_bits)

        if self._len_message_bits > npixels * 3:
            raise Exception(
                f"The message you want to hide is too long: {message_length}"
            )

    def encode_another_pixel(self):
        return True if self._index + 3 <= self._len_message_bits else False

    def encode_pixel(self, coordinate: tuple):
        # Get the colour component.
        r, g, b, *a = self.encoded_image.getpixel(coordinate)

        # Change the Least Significant Bit of each colour component.
        r = setlsb(r, self._message_bits[self._index])
        g = setlsb(g, self._message_bits[self._index + 1])
        b = setlsb(b, self._message_bits[self._index + 2])

        # Save the new pixel
        if self.encoded_image.mode == "RGBA":
            self.encoded_image.putpixel(coordinate, (r, g, b, *a))
        else:
            self.encoded_image.putpixel(coordinate, (r, g, b))

        self._index += 3


class Revealer:
    def __init__(self, encoded_image: Union[str, IO[bytes]], encoding: str = "UTF-8"):
        self.encoded_image = open_image(encoded_image)
        self._encoding_length = ENCODINGS[encoding]
        self._buff, self._count = 0, 0
        self._bitab: List[str] = []
        self._limit: Union[None, int] = None
        self.secret_message = ""

    def decode_pixel(self, coordinate: tuple):
        # pixel = [r, g, b] or [r,g,b,a]
        pixel = self.encoded_image.getpixel(coordinate)

        if self.encoded_image.mode == "RGBA":
            pixel = pixel[:3]  # ignore the alpha

        for color in pixel:
            self._buff += (color & 1) << (self._encoding_length - 1 - self._count)
            self._count += 1

            if self._count == self._encoding_length:
                self._bitab.append(chr(self._buff))
                self._buff, self._count = 0, 0

                if self._bitab[-1] == ":" and self._limit is None:
                    if "".join(self._bitab[:-1]).isdigit():
                        self._limit = int("".join(self._bitab[:-1]))
                    else:
                        raise IndexError("Impossible to detect message.")

        if len(self._bitab) - len(str(self._limit)) - 1 == self._limit:
            self.secret_message = "".join(self._bitab)[
                len(str(self._limit)) + 1 :  # noqa: E203
            ]
            self.encoded_image.close()

            return True

        else:
            return False
