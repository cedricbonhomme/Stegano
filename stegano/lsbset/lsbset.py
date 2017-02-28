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
__version__ = "$Revision: 0.4.2 $"
__date__ = "$Date: 2016/03/13 $"
__revision__ = "$Date: 2016/05/22 $"
__license__ = "GPLv3"

import sys

from PIL import Image

from stegano import tools
from . import generators

def hide(input_image_file, message, generator, auto_convert_rgb=False):
    """Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    message_length = len(message)
    assert message_length != 0, "message length is zero"

    img = Image.open(input_image_file)

    if img.mode not in ['RGB', 'RGBA']:
        if not auto_convert_rgb:
            print('The mode of the image is not RGB. Mode is {}'.\
                                                            format(img.mode))
            answer = input('Convert the image to RGB ? [Y / n]\n') or 'Y'
            if answer.lower() == 'n':
                raise Exception('Not a RGB image.')
        img = img.convert('RGB')

    img_list = list(img.getdata())
    width, height = img.size
    index = 0

    message = str(message_length) + ":" + str(message)
    message_bits = "".join(tools.a2bits_list(message))
    message_bits += '0' * ((3 - (len(message_bits) % 3)) % 3)

    npixels = width * height
    len_message_bits = len(message_bits)
    if len_message_bits > npixels * 3:
        raise Exception("The message you want to hide is too long: {}". \
                                                        format(message_length))

    while index + 3 <= len_message_bits :
        generated_number = next(generator)
        r, g, b, *a = img_list[generated_number]

        # Change the Least Significant Bit of each colour component.
        r = tools.setlsb(r, message_bits[index])
        g = tools.setlsb(g, message_bits[index+1])
        b = tools.setlsb(b, message_bits[index+2])

        # Save the new pixel
        if img.mode == 'RGBA':
            img_list[generated_number] = (r, g , b, a[0])
        else:
            img_list[generated_number] = (r, g , b)

        index += 3

    # create empty new image of appropriate format
    encoded = Image.new('RGB', (img.size))

    # insert saved data into the image
    encoded.putdata(img_list)

    return encoded


def reveal(input_image_file, generator):
    """Find a message in an image (with the LSB technique).
    """
    img = Image.open(input_image_file)
    img_list = list(img.getdata())
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None

    while True:
        generated_number = next(generator)
        # color = [r, g, b]
        for color in img_list[generated_number]:
            buff += (color&1)<<(7-count)
            count += 1
            if count == 8:
                bitab.append(chr(buff))
                buff, count = 0, 0
                if bitab[-1] == ":" and limit == None:
                    try:
                        limit = int("".join(bitab[:-1]))
                    except:
                        pass
        if len(bitab)-len(str(limit))-1 == limit :
            return "".join(bitab)[len(str(limit))+1:]
