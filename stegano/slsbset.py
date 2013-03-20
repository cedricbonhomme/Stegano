#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Stéganô - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2013  Cédric Bonhomme - http://cedricbonhomme.org/
#
# For more information : http://bitbucket.org/cedricbonhomme/stegano/
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
__date__ = "$Date: 2011/12/28 $"
__license__ = "GPLv3"

import sys

from PIL import Image

import tools
import generators

def hide(input_image_file, message, generator_function):
    """
    Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    img = Image.open(input_image_file)
    img_list = list(img.getdata())
    width, height = img.size
    index = 0

    message = str(len(message)) + ":" + message
    #message_bits = tools.a2bits(message)
    message_bits = "".join(tools.a2bits_list(message))

    npixels = width * height
    if len(message_bits) > npixels * 3:
        raise Exception("""The message you want to hide is too long (%s > %s).""" % (len(message_bits), npixels * 3))

    generator = getattr(generators, generator_function)()
    
    while index + 3 <= len(message_bits) :
        generated_number = next(generator)
        (r, g, b) = img_list[generated_number]

        # Change the Least Significant Bit of each colour component.
        r = tools.setlsb(r, message_bits[index])
        g = tools.setlsb(g, message_bits[index+1])
        b = tools.setlsb(b, message_bits[index+2])

        # Save the new pixel
        img_list[generated_number] = (r, g , b)
        
        index += 3

    # create empty new image of appropriate format
    encoded = Image.new('RGB', (img.size))
        
    # insert saved data into the image
    encoded.putdata(img_list)
    
    return encoded
    


def reveal(input_image_file, generator_function):
    """
    Find a message in an image
    (with the LSB technique).
    """
    img = Image.open(input_image_file)
    img_list = list(img.getdata())
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    limit = None

    generator = getattr(generators, generator_function)()

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

    return ""

def write(image, output_image_file):
    """
    """
    try:
        image.save(output_image_file)
    except Exception as e:
        # If hide() returns an error (Too long message).
        print(e)

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

    # Generator
    parser.add_option("-g", "--generator", dest="generator_function",
                    help="Generator")
                    
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
                        generator_function = 'fermat',
                        output_image_file = './pictures/Lenna_enc.png',
                        secret_message = '', secret_file = '', secret_binary = "")

    (options, args) = parser.parse_args()


    if options.hide:
        if options.secret_message != "" and options.secret_file == "":
            secret = options.secret_message
        elif options.secret_message == "" and options.secret_file != "":
            secret = tools.binary2base64(options.secret_file)

        img_encoded = hide(options.input_image_file, secret, options.generator_function)
        try:
            img_encoded.save(options.output_image_file)
        except Exception as e:
            # If hide() returns an error (Too long message).
            print(e)

    elif options.reveal:
        try:
            secret = reveal(options.input_image_file, options.generator_function)
        except IndexError:
            print("Impossible to detect message.")
            exit(0)
        if options.secret_binary != "":
            data = tools.base642binary(secret)
            with open(options.secret_binary, "w") as f:
                f.write(data)
        else:
            print(secret)
