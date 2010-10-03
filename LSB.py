#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

import tools

from PIL import Image

def hide(img, message):
    """
    Hide a message (string) in an image with the
    LSB (Least Significant Bit) technique.
    """
    encoded = img.copy()
    width, height = img.size
    index = 0

    message = message + '~~~'
    message_bits = tools.a2bits(message)

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
    # Point of entry in execution mode
    original_image_file = "./pictures/2010-08-04T15:42:06.png"
    encoded_image_file = "./pictures/2010-08-04T15:42:06_enc.png"
    secret_message = "Avec la technique LSB (Least Significant Bit) l'oeil humain (un normal ;-))  ne voit plus la difference"
    Lorem_ipsum = """\
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.    
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
"""

    img1 = Image.open(original_image_file)
    img_encoded = hide(img1, Lorem_ipsum)

    if img_encoded:
        # Save it
        img_encoded.save(encoded_image_file)
        # Test it
        img2 = Image.open(encoded_image_file)
        print reveal(img2)