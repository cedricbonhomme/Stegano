#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"
__license__ = "GPLv3"

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
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input_image_file",
                    help="Image file")
    parser.add_option("-o", "--output", dest="output_image_file",
                    help="Image file")
    parser.set_defaults(input_image_file = './pictures/Lenna.png',
                        output_image_file = './pictures/Lenna_steganalysed.png')
    (options, args) = parser.parse_args()

    input_image_file = Image.open(options.input_image_file)
    output_image = steganalyse(input_image_file)
    soutput_image.save(options.output_image_file)