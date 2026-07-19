#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2026 Cédric Bonhomme - https://www.cedricbonhomme.org
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

import array
import os
import unittest
import wave

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
            wav.hide(
                "./tests/sample-files/free-software-song.wav", message, "./audio.wav"
            )
            clear_message = wav.reveal("./audio.wav")

            self.assertEqual(message, clear_message)

    def test_hide_and_reveal_UTF8_unicode(self):
        messages_to_hide = ["héllo wörld 🔥", "🍕🍕🍕", "café crème"]

        for message in messages_to_hide:
            wav.hide(
                "./tests/sample-files/free-software-song.wav", message, "./audio.wav"
            )
            clear_message = wav.reveal("./audio.wav")

            self.assertEqual(message, clear_message)

    def test_hide_and_reveal_UTF32LE(self):
        message = "I love 🍕 and 🍫!"
        wav.hide(
            "./tests/sample-files/free-software-song.wav",
            message,
            "./audio.wav",
            encoding="UTF-32LE",
        )
        clear_message = wav.reveal("./audio.wav", encoding="UTF-32LE")

        self.assertEqual(message, clear_message)

    def test_sample_distortion(self):
        """
        Hiding a message must only change the least significant bit of the
        samples: on a 16-bit carrier every sample may change by at most 1.
        """
        wav.hide(
            "./tests/sample-files/free-software-song.wav",
            "Hello World!",
            "./audio.wav",
        )

        with wave.open("./tests/sample-files/free-software-song.wav", "rb") as f:
            original = array.array("h", f.readframes(f.getnframes()))
        with wave.open("./audio.wav", "rb") as f:
            encoded = array.array("h", f.readframes(f.getnframes()))

        max_delta = max(abs(a - b) for a, b in zip(original, encoded))
        self.assertLessEqual(max_delta, 1)

    def test_with_unsupported_encoding(self):
        with self.assertRaises(ValueError):
            wav.hide(
                "./tests/sample-files/free-software-song.wav",
                "Hello",
                "./audio.wav",
                encoding="latin-1",
            )
        with self.assertRaises(ValueError):
            wav.reveal(
                "./tests/sample-files/free-software-song.wav", encoding="latin-1"
            )

    def test_with_too_long_message(self):
        with open("./tests/sample-files/lorem_ipsum.txt") as f:
            message = f.read()
        with self.assertRaises(AssertionError):
            wav.hide(
                "./tests/sample-files/free-software-song.wav", message, "./audio.wav"
            )

    def test_with_message_over_byte_limit(self):
        # 64 four-byte characters exceed the 255-byte capacity of the
        # 8-bit length prefix even though the character count is small.
        message = "🔥" * 64
        with self.assertRaises(AssertionError):
            wav.hide(
                "./tests/sample-files/free-software-song.wav", message, "./audio.wav"
            )

    def tearDown(self):
        try:
            os.unlink("./audio.wav")
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
