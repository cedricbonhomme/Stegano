#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2019 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://github.com/cedricbonhomme/Stegano
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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2016/05/17 $"
__revision__ = "$Date: 2017/01/18 $"
__license__ = "GPLv3"

import os
import unittest
import io

from stegano import exifHeader

class TestEXIFHeader(unittest.TestCase):

    def test_hide_empty_message(self):
        """Test hiding the empty string.
        """
        secret = exifHeader.hide("./tests/sample-files/20160505T130442.jpg",
                                "./image.jpg", secret_message="")
        #secret.save(""./image.png"")

        clear_message = exifHeader.reveal("./image.jpg")

        self.assertEqual(b"", clear_message)

    def test_hide_and_reveal(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]

        for message in messages_to_hide:
            secret = exifHeader.hide("./tests/sample-files/20160505T130442.jpg",
                                    "./image.jpg", secret_message=message)

            clear_message = exifHeader.reveal("./image.jpg")

            self.assertEqual(message, message)

    def test_with_image_without_exif_data(self):
        secret = exifHeader.hide("./tests/sample-files/Lenna.jpg",
                                "./image.jpg", secret_message="")
        #secret.save(""./image.png"")

        clear_message = exifHeader.reveal("./image.jpg")

        self.assertEqual(b"", clear_message)

    def test_with_text_file(self):
        text_file_to_hide = "./tests/sample-files/lorem_ipsum.txt"
        with open(text_file_to_hide, "rb") as f:
            message = f.read()
        secret = exifHeader.hide("./tests/sample-files/20160505T130442.jpg",
                            img_enc="./image.jpg",
                            secret_file=text_file_to_hide)

        clear_message = exifHeader.reveal("./image.jpg")
        self.assertEqual(message, clear_message)

    def test_with_png_image(self):
        secret = exifHeader.hide("./tests/sample-files/Lenna.png",
                                "./image.png", secret_message="Secret")
        #secret.save(""./image.png"")

        with self.assertRaises(ValueError):
            clear_message = exifHeader.reveal("./image.png")

    def test_with_bytes(self):
        outputBytes = io.BytesIO()
        message = b"Secret"
        with open("./tests/sample-files/20160505T130442.jpg", 'rb') as f:
            exifHeader.hide(f, outputBytes, secret_message=message)

            clear_message = exifHeader.reveal(outputBytes)
            self.assertEqual(message, clear_message)

    def tearDown(self):
        try:
            os.unlink("./image.jpg")
        except:
            pass
        try:
            os.unlink("./image.png")
        except:
            pass

if __name__ == '__main__':
    unittest.main()
