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
__version__ = "$Revision: 0.3 $"
__date__ = "$Date: 2016/04/12 $"
__revision__ = "$Date: 2017/05/04 $"
__license__ = "GPLv3"

import io
import os
import base64
import unittest
from unittest.mock import patch

from stegano import lsb

class TestLSB(unittest.TestCase):

    def test_hide_empty_message(self):
        """
        Test hiding the empty string.
        """
        with self.assertRaises(AssertionError):
            secret = lsb.hide("./tests/sample-files/Lenna.png", "")

    def test_hide_and_reveal(self):
        messages_to_hide = ['a', 'foo', 'Hello World!', ':Python:']
        for message in messages_to_hide:
            secret = lsb.hide("./tests/sample-files/Lenna.png", message)
            secret.save("./image.png")

            clear_message = lsb.reveal("./image.png")
            self.assertEqual(message, clear_message)

    def test_hide_and_reveal_UTF32LE(self):
        messages_to_hide = 'I love 🍕 and 🍫!'
        secret = lsb.hide("./tests/sample-files/Lenna.png",
                            messages_to_hide, encoding='UTF-32LE')
        secret.save("./image.png")

        clear_message = lsb.reveal("./image.png", encoding='UTF-32LE')
        self.assertEqual(messages_to_hide, clear_message)

    def test_with_transparent_png(self):
        messages_to_hide = ['🍕', 'a', 'foo', 'Hello World!', ':Python:']
        for message in messages_to_hide:
            secret = lsb.hide("./tests/sample-files/transparent.png",
                                message, encoding='UTF-32LE')
            secret.save("./image.png")

            clear_message = lsb.reveal("./image.png", encoding='UTF-32LE')

            self.assertEqual(message, clear_message)

    @patch('builtins.input', return_value='y')
    def test_manual_convert_rgb(self, input):
        message_to_hide = 'I love 🍕 and 🍫!'
        secret = lsb.hide("./tests/sample-files/Lenna-grayscale.png",
                            message_to_hide, encoding='UTF-32LE')

    @patch('builtins.input', return_value='n')
    def test_refuse_convert_rgb(self, input):
        message_to_hide = 'I love 🍕 and 🍫!'
        with self.assertRaises(Exception):
            secret = lsb.hide("./tests/sample-files/Lenna-grayscale.png",
                                    message_to_hide, encoding='UTF-32LE')

    def test_auto_convert_rgb(self):
        message_to_hide = 'I love 🍕 and 🍫!'
        secret = lsb.hide("./tests/sample-files/Lenna-grayscale.png",
                            message_to_hide, encoding='UTF-32LE', auto_convert_rgb=True)

    def test_with_text_file(self):
        text_file_to_hide = './tests/sample-files/lorem_ipsum.txt'
        with open(text_file_to_hide) as f:
            message = f.read()
        secret = lsb.hide("./tests/sample-files/Lenna.png", message)
        secret.save("./image.png")

        clear_message = lsb.reveal("./image.png")
        self.assertEqual(message, clear_message)

    def test_with_binary_file(self):
        binary_file_to_hide = "./tests/sample-files/free-software-song.ogg"
        with open(binary_file_to_hide, "rb") as bin_file:
            encoded_string = base64.b64encode(bin_file.read())
            message = encoded_string.decode()
        secret = lsb.hide("./tests/sample-files/Montenach.png", message)
        secret.save("./image.png")

        clear_message = lsb.reveal("./image.png")
        clear_message += '==='
        clear_message = base64.b64decode(clear_message)
        with open('file1', 'wb') as f:
            f.write(clear_message)
        with open('file1', 'rb') as bin_file:
            encoded_string = base64.b64encode(bin_file.read())
            message1 = encoded_string.decode()
        self.assertEqual(message, message1)
        try:
            os.unlink('./file1')
        except:
            pass

    def test_with_too_long_message(self):
        with open("./tests/sample-files/lorem_ipsum.txt") as f:
            message = f.read()
        message += message*2
        with self.assertRaises(Exception):
            lsb.hide("./tests/sample-files/Lenna.png", message)

    def test_with_bytes(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]

        for message in messages_to_hide:
            outputBytes = io.BytesIO()
            with open("./tests/sample-files/20160505T130442.jpg", 'rb') as f:
                bytes_image = lsb.hide(f, message)
                bytes_image.save(outputBytes, "PNG")
                outputBytes.seek(0)

                clear_message = lsb.reveal(outputBytes)

                self.assertEqual(message, clear_message)

    def test_with_location_of_image_as_argument(self):
        messages_to_hide = ["Hello World!"]

        for message in messages_to_hide:
            outputBytes = io.BytesIO()
            bytes_image = lsb.hide("./tests/sample-files/20160505T130442.jpg", message)
            bytes_image.save(outputBytes, "PNG")
            outputBytes.seek(0)

            clear_message = lsb.reveal(outputBytes)

            self.assertEqual(message, clear_message)

    def tearDown(self):
        try:
            os.unlink("./image.png")
        except:
            pass


if __name__ == '__main__':
    unittest.main()
