#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Stéganô - Stéganô is a basic Python Steganography module.
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
__version__ = "$Revision: 0.2 $"
__date__ = "$Date: 2016/04/13 $"
__revision__ = "$Date: 2016/05/22 $"
__license__ = "GPLv3"

import os
import unittest

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

    def test_with_transparent_png(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]

        for message in messages_to_hide:
            secret = lsbset.hide("./tests/sample-files/transparent.png",
                                    message, generators.eratosthenes())
            secret.save("./image.png")

            clear_message = lsbset.reveal("./image.png",
                                    generators.eratosthenes())

            self.assertEqual(message, clear_message)

    def test_with_too_long_message(self):
        with open("./tests/sample-files/lorem_ipsum.txt") as f:
            message = f.read()
        with self.assertRaises(Exception):
            lsbset.hide("./tests/sample-files/Lenna.png", message,
                                    generators.eratosthenes())

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
