#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Stéganô - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2017  Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.3 $"
__date__ = "$Date: 2016/08/04 $"
__revision__ = "$Date: 2017/05/04 $"
__license__ = "GPLv3"

import sys

from PIL import Image
from typing import Union, IO

from stegano import tools

def hide(input_image: Union[str, IO[bytes]],
        message: str,
        encoding: str = 'UTF-8',
        auto_convert_rgb: bool = False):
    """Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    message_length = len(message)
    assert message_length != 0, "message length is zero"

    img = Image.open(input_image)

    if img.mode not in ['RGB', 'RGBA']:
        if not auto_convert_rgb:
            print('The mode of the image is not RGB. Mode is {}'.\
                                                            format(img.mode))
            answer = input('Convert the image to RGB ? [Y / n]\n') or 'Y'
            if answer.lower() == 'n':
                raise Exception('Not a RGB image.')
        img = img.convert('RGB')

    encoded = img.copy()
    width, height = img.size
    index = 0

    message = str(message_length) + ":" + str(message)
    message_bits = "".join(tools.a2bits_list(message, encoding))
    message_bits += '0' * ((3 - (len(message_bits) % 3)) % 3)

    npixels = width * height
    len_message_bits = len(message_bits)
    if len_message_bits > npixels * 3:
        raise Exception("The message you want to hide is too long: {}". \
                                                        format(message_length))
    for row in range(height):
        for col in range(width):
            if index + 3 <= len_message_bits :

                # Get the colour component.
                pixel = img.getpixel((col, row))
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]

                # Change the Least Significant Bit of each colour component.
                r = tools.setlsb(r, message_bits[index])
                g = tools.setlsb(g, message_bits[index+1])
                b = tools.setlsb(b, message_bits[index+2])

                # Save the new pixel
                if img.mode == 'RGBA':
                    encoded.putpixel((col, row), (r, g, b, pixel[3]))
                else:
                    encoded.putpixel((col, row), (r, g, b))

                index += 3
            else:
                img.close()
                return encoded


def reveal(input_image: Union[str, IO[bytes]], encoding='UTF-8'):
    """Find a message in an image (with the LSB technique).
    """
    img = Image.open(input_image)
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None
    for row in range(height):
        for col in range(width):

            # pixel = [r, g, b] or [r,g,b,a]
            pixel = img.getpixel((col, row))
            if img.mode == 'RGBA':
                pixel = pixel[:3] # ignore the alpha
            for color in pixel:
                buff += (color&1)<<(tools.ENCODINGS[encoding]-1 - count)
                count += 1
                if count == tools.ENCODINGS[encoding]:
                    bitab.append(chr(buff))
                    buff, count = 0, 0
                    if bitab[-1] == ":" and limit == None:
                        try:
                            limit = int("".join(bitab[:-1]))
                        except:
                            pass

            if len(bitab)-len(str(limit))-1 == limit :
                img.close()
                return "".join(bitab)[len(str(limit))+1:]
