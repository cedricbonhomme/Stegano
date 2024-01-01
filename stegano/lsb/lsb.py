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
__version__ = "$Revision: 0.7 $"
__date__ = "$Date: 2016/03/13 $"
__revision__ = "$Date: 2019/05/31 $"
__license__ = "GPLv3"

from typing import IO, Iterator, Union

from stegano import tools

from .generators import identity


def hide(
    image: Union[str, IO[bytes]],
    message: str,
    generator: Union[None, Iterator[int]] = None,
    shift: int = 0,
    encoding: str = "UTF-8",
    auto_convert_rgb: bool = False,
):
    """Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    hider = tools.Hider(image, message, encoding, auto_convert_rgb)
    width = hider.encoded_image.width

    if not generator:
        generator = identity()

    while shift != 0:
        next(generator)
        shift -= 1

    while hider.encode_another_pixel():
        generated_number = next(generator)

        col = generated_number % width
        row = int(generated_number / width)

        hider.encode_pixel((col, row))

    return hider.encoded_image


def reveal(
    encoded_image: Union[str, IO[bytes]],
    generator: Union[None, Iterator[int]] = None,
    shift: int = 0,
    encoding: str = "UTF-8",
):
    """Find a message in an image (with the LSB technique)."""
    revealer = tools.Revealer(encoded_image, encoding)
    width = revealer.encoded_image.width

    if not generator:
        generator = identity()

    while shift != 0:
        next(generator)
        shift -= 1

    while True:
        generated_number = next(generator)

        col = generated_number % width
        row = int(generated_number / width)

        if revealer.decode_pixel((col, row)):
            return revealer.secret_message
