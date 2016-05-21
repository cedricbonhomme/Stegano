#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
__version__ = "$Revision: 0.2.1 $"
__date__ = "$Date: 2016/03/13 $"
__license__ = "GPLv3"

import sys

from PIL import Image

from stegano import tools

try:
   input = raw_input
except NameError:
   pass

def hide(input_image_file, message, auto_convert_rgb=False):
    """
    Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    message_length = len(message)
    assert message_length != 0, "message length is zero"

    img = Image.open(input_image_file)
    if img.mode != 'RGB':
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
    message_bits = "".join(tools.a2bits_list(message))
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
                (r, g, b) = img.getpixel((col, row))

                # Change the Least Significant Bit of each colour component.
                r = tools.setlsb(r, message_bits[index])
                g = tools.setlsb(g, message_bits[index+1])
                b = tools.setlsb(b, message_bits[index+2])

                # Save the new pixel
                encoded.putpixel((col, row), (r, g , b))

                index += 3
            else:
                img.close()
                return encoded

    img.close()
    return encoded

def reveal(input_image_file):
    """
    Find a message in an image
    (with the LSB technique).
    """
    img = Image.open(input_image_file)
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None
    for row in range(height):
        for col in range(width):

            # color = [r, g, b]
            for color in img.getpixel((col, row)):
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
                img.close()
                return "".join(bitab)[len(str(limit))+1:]
    img.close()
    return ""

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
    parser = OptionParser(version=__version__)
    parser.add_option('--hide', action='store_true', default=False,
                      help="Hides a message in an image.")
    parser.add_option('--reveal', action='store_true', default=False,
                      help="Reveals the message hided in an image.")
    # Original image
    parser.add_option("-i", "--input", dest="input_image_file",
                    help="Input image file.")
    # Image containing the secret
    parser.add_option("-o", "--output", dest="output_image_file",
                    help="Output image containing the secret.")

    # Non binary secret message to hide
    parser.add_option("-m", "--secret-message", dest="secret_message",
                    help="Your secret message to hide (non binary).")

    # Binary secret to hide (OGG, executable, etc.)
    parser.add_option("-f", "--secret-file", dest="secret_file",
                    help="Your secret to hide (Text or any binary file).")
    # Output for the binary binary secret.
    parser.add_option("-b", "--binary", dest="secret_binary",
                    help="Output for the binary secret (Text or any binary file).")

    parser.set_defaults(input_image_file = './pictures/Lenna.png',
                        output_image_file = './pictures/Lenna_enc.png',
                        secret_message = '', secret_file = '', secret_binary = "")

    (options, args) = parser.parse_args()


    if options.hide:
        if options.secret_message != "" and options.secret_file == "":
            secret = options.secret_message
        elif options.secret_message == "" and options.secret_file != "":
            secret = tools.binary2base64(options.secret_file)

        img_encoded = hide(options.input_image_file, secret)
        try:
            img_encoded.save(options.output_image_file)
        except Exception as e:
            # If hide() returns an error (Too long message).
            print(e)

    elif options.reveal:
        secret = reveal(options.input_image_file)
        if options.secret_binary != "":
            data = tools.base642binary(secret)
            with open(options.secret_binary, "w") as f:
                f.write(data)
        else:
            print(secret)
