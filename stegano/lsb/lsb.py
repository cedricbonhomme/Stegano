#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2022 Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.4 $"
__date__ = "$Date: 2016/08/04 $"
__revision__ = "$Date: 2019/06/01 $"
__license__ = "GPLv3"

from typing import IO, Union

from stegano import tools


def hide(
    image: Union[str, IO[bytes]],
    message: str,
    encoding: str = "UTF-8",
    shift: int = 0,
    auto_convert_rgb: bool = False,
):
    """Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    hider = tools.Hider(image, message, encoding, auto_convert_rgb)
    width, height = hider.encoded_image.size

    for row in range(height):
        for col in range(width):
            if shift != 0:
                shift -= 1
                continue

            if hider.encode_another_pixel():
                hider.encode_pixel((col, row))
            else:
                return hider.encoded_image


def reveal(
    encoded_image: Union[str, IO[bytes]],
    encoding: str = "UTF-8",
    shift: int = 0,
):
    """Find a message in an image (with the LSB technique)."""
    revealer = tools.Revealer(encoded_image, encoding)
    width, height = revealer.encoded_image.size

    for row in range(height):
        for col in range(width):
            if shift != 0:
                shift -= 1
                continue

            if revealer.decode_pixel((col, row)):
                return revealer.secret_message
