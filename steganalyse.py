#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

from PIL import Image

def steganalyse(img):
    """
    Find a message in an image
    (with the LSB technique).
    """
    encoded = img.copy()
    width, height = img.size
    bits = ""
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
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
            encoded.putpixel((col, row), (r, g , b))
    return encoded

if __name__ == '__main__':
    # Point of entry in execution mode
    original_image_file = "./pictures/2010-08-04T15:42:06.png"
    encoded_image_file = "./pictures/2010-08-04T15:42:06_enc.png"
    original_image_file_steganalysed = "./pictures/2010-08-04T15:42:06_steganalysed.png"
    encoded_image_file_steganalysed = "./pictures/2010-08-04T15:42:06_enc_steganalysed.png"

    img_original_image_file = Image.open(original_image_file)
    img_encoded_image_file = Image.open(encoded_image_file)

    img_original_image_steganalysde = steganalyse(img_original_image_file)
    img_encoded_image_steganalysed = steganalyse(img_encoded_image_file)

    img_original_image_steganalysde.save(original_image_file_steganalysed)
    img_encoded_image_steganalysed.save(encoded_image_file_steganalysed)