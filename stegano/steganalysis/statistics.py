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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2010/10/01 $"
__revision__ = "$Date: 2021/11/01 $"
__license__ = "GPLv3"

import typing
from collections import Counter, OrderedDict


def steganalyse(img):
    """
    Steganlysis of the LSB technique.
    """
    width, height = img.size
    colours_counter: typing.Counter[int] = Counter()
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            colours_counter[r] += 1

    most_common = colours_counter.most_common(10)
    dict_colours = OrderedDict(
        sorted(list(colours_counter.items()), key=lambda t: t[1])
    )

    colours: float = 0
    for colour in list(dict_colours.keys()):
        colours += colour
    colours = colours / len(dict_colours)

    # return colours.most_common(10)
    return list(dict_colours.keys())[:30], most_common
