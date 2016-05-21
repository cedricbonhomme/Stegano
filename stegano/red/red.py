#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stéganô - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2016  Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"
__license__ = "GPLv3"

import sys

from PIL import Image

def hide(input_image_file, message):
    """
    Hide a message (string) in an image.

    Use the red portion of a pixel (r, g, b) tuple to
    hide the message string characters as ASCII values.
    The red value of the first pixel is used for message_length of the string.
    """
    message_length = len(message)
    assert message_length != 0, "message message_length is zero"
    assert message_length < 255, "message is too long"
    img = Image.open(input_image_file)
    # Use a copy of image to hide the text in
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            (r, g, b) = img.getpixel((col, row))
            # first value is message_length of message
            if row == 0 and col == 0 and index < message_length:
                asc = message_length
            elif index <= message_length:
                c = message[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    img.close()
    return encoded

def reveal(input_image_file):
    """
    Find a message in an image.

    Check the red portion of an pixel (r, g, b) tuple for
    hidden message characters (ASCII values).
    The red value of the first pixel is used for message_length of string.
    """
    img = Image.open(input_image_file)
    width, height = img.size
    message = ""
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            # First pixel r value is length of message
            if row == 0 and col == 0:
                message_length = r
            elif index <= message_length:
                message += chr(r)
            index += 1
    img.close()
    return message

def write(image, output_image_file):
    """
    """
    try:
        image.save(output_image_file)
    except Exception as e:
        # If hide() returns an error (Too long message).
        print(e)
    finally:
        image.close()

if __name__ == '__main__':
    # Point of entry in execution mode.
    from optparse import OptionParser
    usage = "usage: %prog hide|reveal [options]"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="input_image_file",
                    help="Image file.")
    parser.add_option("-o", "--output", dest="output_image_file",
                    help="Image file.")
    parser.add_option("-s", "--secret", dest="secret",
                    help="Your secret (Message, Image, Music or any binary file).")
    parser.set_defaults(input_image_file = './pictures/Lenna.png',
                        output_image_file = './pictures/Lenna_enc.png',
                        secret = 'Hello World!')

    (options, args) = parser.parse_args()

    if sys.argv[1] == "hide":
        img = Image.open(options.input_image_file)
        img_encoded = hide(img, options.secret)
        img_encoded.save(options.output_image_file)

    elif sys.argv[1] == "reveal":
        img = Image.open(options.input_image_file)
        print(reveal(img))
