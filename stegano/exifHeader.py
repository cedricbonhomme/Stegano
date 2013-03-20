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
__date__ = "$Date: 2010/03/24 $"
__license__ = "GPLv3"

# Thanks to: http://www.julesberman.info/spec2img.htm

def hide(img, img_enc, copyright="http://bitbucket.org/cedricbonhomme/stegano", \
            secret_message = None, secret_file = None):
    """
    """
    import shutil
    import datetime
    from zlib import compress
    from zlib import decompress
    from base64 import b64encode
    from .exif.minimal_exif_writer import MinimalExifWriter

    if secret_file != None:
        with open(secret_file, "r") as f:
            secret_file_content = f.read()
    text = "\nImage annotation date: "
    text = text + str(datetime.date.today())
    text = text  + "\nImage description:\n"
    if secret_file != None:
        text = compress(b64encode(text + secret_file_content))
    else:
        text = compress(b64encode(text + secret_message))

    try:
        shutil.copy(img, img_enc)
    except Exception as e:
        print(("Impossible to copy image:", e))
        return

    f = MinimalExifWriter(img_enc)
    f.removeExif()
    f.newImageDescription(text)
    f.newCopyright(copyright, addYear = 1)
    f.process()


def reveal(img):
    """
    """
    from base64 import b64decode
    from zlib import decompress
    from .exif.minimal_exif_reader import MinimalExifReader
    try:
        g = MinimalExifReader(img)
    except:
        print("Impossible to read description.")
        return
    print((b64decode(decompress(g.imageDescription()))))
    print(("\nCopyright " + g.copyright()))
    #print g.dateTimeOriginal()s


if __name__ == "__main__":
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

    # Secret raw message to hide
    parser.add_option("-m", "--secret-message", dest="secret_message",
                    help="Your raw secret message to hide.")

    # Secret text file to hide.
    parser.add_option("-f", "--secret-file", dest="secret_file",
                    help="Your secret textt file to hide.")

    parser.set_defaults(input_image_file = './pictures/Elisha-Cuthbert.jpg',
                        output_image_file = './pictures/Elisha-Cuthbert_enc.jpg',
                        secret_message = '', secret_file = '')

    (options, args) = parser.parse_args()

    if options.hide:
        if options.secret_message != "" and options.secret_file == "":
            hide(img=options.input_image_file, img_enc=options.output_image_file, \
                    secret_message=options.secret_message)
        elif options.secret_message == "" and options.secret_file != "":
            hide(img=options.input_image_file, img_enc=options.output_image_file, \
                    secret_file=options.secret_file)

    elif options.reveal:
        reveal(img=options.input_image_file)