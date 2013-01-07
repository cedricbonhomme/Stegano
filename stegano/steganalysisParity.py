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
    output_image.save(options.output_image_file)