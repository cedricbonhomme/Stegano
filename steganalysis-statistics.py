#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"

import operator

from PIL import Image
from collections import Counter
from collections import OrderedDict

def steganalyse(img):
    """
    Steganlysis of the LSB technique.
    """
    encoded = img.copy()
    width, height = img.size
    colours = Counter()
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            colours[r] += 1

    most_common = colours.most_common(10)
    dict_colours = OrderedDict(sorted(colours.items(), key=lambda t: t[1]))

    colours = 0
    for colour in dict_colours.keys():
        colours += colour
    colours = colours / len(dict_colours)

    #return colours.most_common(10)
    return dict_colours.keys()[:30], most_common

if __name__ == '__main__':
    # Point of entry in execution mode.    
    original_image_file = "./pictures/montenach.png"
    encoded_image_file = "./pictures/montenach_enc.png"
    original_image_file_steganalysed = "./pictures/montenach_steganalysed.png"
    encoded_image_file_steganalysed = "./pictures/montenach_enc_steganalysed.png"

    img_original_image_file = Image.open(original_image_file)
    img_encoded_image_file = Image.open(encoded_image_file)
    img_original_image_file_steganalysed = Image.open(original_image_file_steganalysed)
    img_encoded_image_file_steganalysed = Image.open(encoded_image_file_steganalysed)

    print steganalyse(img_original_image_file)
    print
    print steganalyse(img_encoded_image_file)
    print
    print
    print steganalyse(img_original_image_file_steganalysed)
    print
    print steganalyse(img_encoded_image_file_steganalysed)