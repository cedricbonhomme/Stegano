#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

import sys

from PIL import Image

import tools

def hide(img, message):
    """
    Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    encoded = img.copy()
    width, height = img.size
    index = 0

    message = message + '~~~'
    #message_bits = tools.a2bits(message)
    message_bits = "".join(tools.a2bits_list(message))

    npixels = width * height
    if len(message_bits) > npixels * 3:
        return """Too long message (%s > %s).""" % (len(message_bits), npixels * 3)

    for row in range(height):
        for col in range(width):

            if index + 3 <= len(message_bits) :

                # Get the colour component.
                (r, g, b) = img.getpixel((col, row))

                # Change the Least Significant Bit of each colour component.
                r = tools.setlsb(r, message_bits[index])
                g = tools.setlsb(g, message_bits[index+1])
                b = tools.setlsb(b, message_bits[index+2])

                # Save the new pixel
                encoded.putpixel((col, row), (r, g , b))

            index += 3

    return encoded

def reveal(img):
    """
    Find a message in an image
    (with the LSB technique).
    """
    width, height = img.size
    buff, count = 0, 0
    bitab = []
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))

            buff += (r&1)<<(7-count)
            count += 1
            if count == 8:
                bitab.append(chr(buff))
                buff, count = 0, 0

            buff += (g&1)<<(7-count)
            count += 1
            if count == 8:
                bitab.append(chr(buff))
                buff, count = 0, 0

            buff += (b&1)<<(7-count)
            count += 1
            if count == 8:
                bitab.append(chr(buff))
                buff, count = 0, 0

            if len(bitab) > 0 and bitab[-1] == chr(126):
                return "".join(bitab)[:-1]
    return ""

def reveal_slow(img):
    """
    Find a message in an image
    (with the LSB technique).
    """
    width, height = img.size
    bits = ""
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))

            bits += tools.bs(r)[-1] + tools.bs(g)[-1] + tools.bs(b)[-1]

            if int(bits[-8:], 2) == 126:
                # chr(126) = '~ '
                list_of_string_bits = ["".join(list(bits[i:(i+8)])) for i in range(0, len(bits)-8, 8)]

                list_of_character = [chr(int(elem, 2)) for elem in list_of_string_bits]
                return "".join(list_of_character)
    return ""


if __name__ == '__main__':
    # Point of entry in execution mode.
    from optparse import OptionParser
    usage = "usage: %prog hide|reveal [options]"
    parser = OptionParser(usage)
    parser.add_option("-i", "--input", dest="input_image_file",
                    help="Image file")
    parser.add_option("-o", "--output", dest="output_image_file",
                    help="Image file")
    parser.add_option("-s", "--secret", dest="secret",
                    help="Your secret (Message, Image, Music or any binary file.)")
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
        print reveal(img)