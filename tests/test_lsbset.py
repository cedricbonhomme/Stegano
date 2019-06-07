#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2017  Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.4 $"
__date__ = "$Date: 2016/04/13 $"
__revision__ = "$Date: 2017/05/04 $"
__license__ = "GPLv3"

import io
import os
import unittest
from unittest.mock import patch

from stegano import lsbset
from stegano.lsbset import generators

class TestLSBSet(unittest.TestCase):

    def test_hide_empty_message(self):
        """
        Test hiding the empty string.
        """
        with self.assertRaises(AssertionError):
            secret = lsbset.hide("./tests/sample-files/Lenna.png", "",
                                    generators.eratosthenes())

    def test_hide_and_reveal(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]
        for message in messages_to_hide:
            secret = lsbset.hide("./tests/sample-files/Lenna.png", message,
                                    generators.eratosthenes())
            secret.save("./image.png")

            clear_message = lsbset.reveal("./image.png",
                                    generators.eratosthenes())

            self.assertEqual(message, clear_message)

    def test_hide_and_reveal_with_ackermann(self):
        messages_to_hide = ["foo"]
        for message in messages_to_hide:
            secret = lsbset.hide("./tests/sample-files/Lenna.png", message,
                                    generators.ackermann(m=3))
            secret.save("./image.png")

            clear_message = lsbset.reveal("./image.png",
                                    generators.ackermann(m=3))

            self.assertEqual(message, clear_message)
            
    def test_hide_and_reveal_with_shift(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]
        for message in messages_to_hide:
            secret = lsbset.hide("./tests/sample-files/Lenna.png", message,
                                    generators.eratosthenes(), 4)
            secret.save("./image.png")

            clear_message = lsbset.reveal("./image.png",
                                    generators.eratosthenes(), 4)

            self.assertEqual(message, clear_message)

    def test_hide_and_reveal_UTF32LE(self):
        messages_to_hide = 'I love 🍕 and 🍫!'
        secret = lsbset.hide("./tests/sample-files/Lenna.png",
                            messages_to_hide,
                            generators.eratosthenes(),
                            encoding='UTF-32LE')
        secret.save("./image.png")

        clear_message = lsbset.reveal("./image.png", generators.eratosthenes(),
                                        encoding='UTF-32LE')
        self.assertEqual(messages_to_hide, clear_message)

    def test_with_transparent_png(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]
        for message in messages_to_hide:
            secret = lsbset.hide("./tests/sample-files/transparent.png",
                                    message, generators.eratosthenes())
            secret.save("./image.png")

            clear_message = lsbset.reveal("./image.png",
                                    generators.eratosthenes())

            self.assertEqual(message, clear_message)

    @patch('builtins.input', return_value='y')
    def test_manual_convert_rgb(self, input):
        message_to_hide = "Hello World!"
        secret = lsbset.hide("./tests/sample-files/Lenna-grayscale.png",
                                    message_to_hide, generators.eratosthenes())

    @patch('builtins.input', return_value='n')
    def test_refuse_convert_rgb(self, input):
        message_to_hide = "Hello World!"
        with self.assertRaises(Exception):
            secret = lsbset.hide("./tests/sample-files/Lenna-grayscale.png",
                                    message_to_hide, generators.eratosthenes())

    def test_with_location_of_image_as_argument(self):
        messages_to_hide = ["Hello World!"]

        for message in messages_to_hide:
            outputBytes = io.BytesIO()
            bytes_image = lsbset.hide("./tests/sample-files/20160505T130442.jpg", message,
                                      generators.identity())
            bytes_image.save(outputBytes, "PNG")
            outputBytes.seek(0)

            clear_message = lsbset.reveal(outputBytes, generators.identity())

            self.assertEqual(message, clear_message)

    def test_auto_convert_rgb(self):
        message_to_hide = "Hello World!"
        secret = lsbset.hide("./tests/sample-files/Lenna-grayscale.png",
                            message_to_hide, generators.eratosthenes(),
                            auto_convert_rgb=True)

    def test_with_too_long_message(self):
        with open("./tests/sample-files/lorem_ipsum.txt") as f:
            message = f.read()
        message += message*2
        with self.assertRaises(Exception):
            lsbset.hide("./tests/sample-files/Lenna.png", message,
                                    generators.identity())

    def test_hide_and_reveal_with_bad_generator(self):
        message_to_hide = "Hello World!"
        secret = lsbset.hide("./tests/sample-files/Lenna.png", message_to_hide,
                                    generators.eratosthenes())
        secret.save("./image.png")

        with self.assertRaises(IndexError):
            clear_message = lsbset.reveal("./image.png", generators.identity())

    def test_with_unknown_generator(self):
        message_to_hide = "Hello World!"
        with self.assertRaises(AttributeError):
            secret = lsbset.hide("./tests/sample-files/Lenna.png",
                                    message_to_hide, generators.eratosthene())

    def tearDown(self):
        try:
            os.unlink("./image.png")
        except:
            pass


if __name__ == '__main__':
    unittest.main()
