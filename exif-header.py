#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Stéganô - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2011  Cédric Bonhomme - http://cedricbonhomme.org/
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

def hide(img, img_enc, copyright="http://bitbucket.org/cedricbonhomme/stegano"):
    """
    """
    import shutil
    import datetime
    from zlib import compress
    from zlib import decompress
    from base64 import b64encode
    from exif.minimal_exif_writer import MinimalExifWriter

    file = open("lorem_ipsum.txt", "r")
    text = "\nImage annotation date: "
    text = text + str(datetime.date.today())
    text = text  + "\nImage description:\n"
    text = compress(b64encode(text + file.read()))
    file.close()

    try:
        shutil.copy(img, img_enc)
    except Exception as e:
        print("Impossible to copy image:", e)
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
    from exif.minimal_exif_reader import MinimalExifReader
    try:
        g = MinimalExifReader(img)
    except:
        print("Impossible to read description.")
        return
    print(b64decode(decompress(g.imageDescription())))
    print(("\nCopyright " + g.copyright()))
    #print g.dateTimeOriginal()s


if __name__ == "__main__":
    hide(img='./pictures/Elisha-Cuthbert.jpg', img_enc='./pictures/Elisha-Cuthbert_enc.jpg')
    reveal(img='./pictures/Elisha-Cuthbert_enc.jpg')