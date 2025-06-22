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
__version__ = "$Revision: 0.9.4 $"
__date__ = "$Date: 2010/10/01 $"
__revision__ = "$Date: 2019/06/06 $"
__license__ = "GPLv3"

from typing import cast

from PIL import Image


def steganalyse(img: Image.Image) -> Image.Image:
    """
    Steganlysis of the LSB technique.
    """
    encoded = Image.new(img.mode, (img.size))
    width, height = img.size
    for row in range(height):
        for col in range(width):
            if pixel := cast(tuple[int, int, int], img.getpixel((col, row))):
                r, g, b = pixel[0:3]
            else:
                raise Exception("Error during steganlysis.")
            if r % 2 == 0:
                r = 0
            else:
                r = 255
            if g % 2 == 0:
                g = 0
            else:
                g = 255
            if b % 2 == 0:
                b = 0
            else:
                b = 255
            encoded.putpixel((col, row), (r, g, b))
    return encoded
