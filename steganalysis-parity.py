#! /usr/local/bin/python
#-*- coding: utf-8 -*-

__author__ = "Cedric Bonhomme"
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2010/10/01 $"
__license__ = "GPLv3"

from PIL import Image

def steganalyse(img):
    """
    Steganlysis of the LSB technique.
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
    output_image.save(options.output_image_file)