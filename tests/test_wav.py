#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2025 Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2016/05/19 $"
__license__ = "GPLv3"

import os
import unittest

from stegano import wav


class TestWav(unittest.TestCase):
    def test_hide_empty_message(self):
        """
        Test hiding the empty string.
        """
        with self.assertRaises(AssertionError):
            wav.hide("./tests/sample-files/free-software-song.wav", "", "./audio.wav")

    def test_hide_and_reveal(self):
        messages_to_hide = ["a", "foo", "Hello World!", ":Python:"]

        for message in messages_to_hide:
            wav.hide("./tests/sample-files/free-software-song.wav", message, "./audio.wav")
            clear_message = wav.reveal("./audio.wav")

            self.assertEqual(message, clear_message)

    def test_with_too_long_message(self):
        with open("./tests/sample-files/lorem_ipsum.txt") as f:
            message = f.read()
        with self.assertRaises(AssertionError):
            wav.hide("./tests/sample-files/free-software-song.wav", message, "./audio.wav")

    def tearDown(self):
        try:
            os.unlink("./audio.wav")
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
