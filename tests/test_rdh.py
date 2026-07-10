#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2026  Cédric Bonhomme - https://www.cedricbonhomme.org
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

import os
import unittest

from PIL import Image

from stegano import rdh

GRAYSCALE = "./tests/sample-files/Lenna-grayscale.png"
COLOR = "./tests/sample-files/Lenna.png"


class TestHistogramShifting(unittest.TestCase):
    def tearDown(self):
        for name in ("./rdh-stego.png",):
            if os.path.isfile(name):
                os.unlink(name)

    def test_hide_and_reveal(self):
        messages = ["a", "foo", "Hello World!", ":Python:", ""]
        for message in messages:
            stego = rdh.hide(GRAYSCALE, message)
            stego.save("./rdh-stego.png")
            self.assertEqual(message, rdh.reveal("./rdh-stego.png"))

    def test_hide_and_reveal_rgb(self):
        message = "Reversible data hiding in an RGB image."
        stego = rdh.hide(COLOR, message)
        stego.save("./rdh-stego.png")
        self.assertEqual(message, rdh.reveal("./rdh-stego.png"))

    def test_hide_and_reveal_utf32le(self):
        message = "héllo €"
        stego = rdh.hide(GRAYSCALE, message, "UTF-32LE")
        stego.save("./rdh-stego.png")
        self.assertEqual(message, rdh.reveal("./rdh-stego.png", "UTF-32LE"))

    def test_wide_characters_rejected_with_utf8(self):
        # Characters above U+00FF do not fit in the 8 bits per character of
        # the UTF-8 encoding and would be silently corrupted.
        with self.assertRaises(ValueError):
            rdh.hide(GRAYSCALE, "héllo €")

    def test_cover_is_recovered_exactly_grayscale(self):
        # The defining property of reversible data hiding: after extraction
        # the original cover is restored pixel-for-pixel.
        original = Image.open(GRAYSCALE).convert("L")
        stego = rdh.hide(original, "some secret payload")
        recovered = rdh.recover(stego)
        self.assertEqual(recovered.mode, original.mode)
        self.assertEqual(recovered.size, original.size)
        self.assertEqual(recovered.tobytes(), original.tobytes())

    def test_cover_is_recovered_exactly_rgb(self):
        original = Image.open(COLOR).convert("RGB")
        stego = rdh.hide(original, "another secret payload for rgb")
        recovered = rdh.recover(stego)
        self.assertEqual(recovered.tobytes(), original.tobytes())

    def test_recovery_survives_lossless_save(self):
        original = Image.open(GRAYSCALE).convert("L")
        rdh.hide(original, "persisted secret").save("./rdh-stego.png")
        self.assertEqual("persisted secret", rdh.reveal("./rdh-stego.png"))
        recovered = rdh.recover("./rdh-stego.png")
        self.assertEqual(recovered.tobytes(), original.tobytes())

    def test_stego_only_differs_by_at_most_one_level(self):
        # Histogram shifting only ever moves a sample by +/-1.
        original = Image.open(GRAYSCALE).convert("L")
        stego = rdh.hide(original, "low distortion check")
        for before, after in zip(original.tobytes(), stego.tobytes()):
            self.assertLessEqual(abs(before - after), 1)

    def test_capacity_matches_hide_limit(self):
        capacity = rdh.capacity(GRAYSCALE)
        self.assertGreater(capacity, 0)
        # A message at the capacity fits; one byte more does not.
        rdh.hide(GRAYSCALE, "a" * capacity)
        with self.assertRaises(ValueError):
            rdh.hide(GRAYSCALE, "a" * (capacity + 1))

    def test_reveal_without_payload_raises(self):
        with self.assertRaises(ValueError):
            rdh.reveal(GRAYSCALE)

    def test_unsupported_mode_raises(self):
        with self.assertRaises(ValueError):
            rdh.hide(Image.new("CMYK", (64, 64)), "hi")
        with self.assertRaises(ValueError):
            rdh.capacity(Image.new("CMYK", (64, 64)))

    def test_saturated_histogram_raises(self):
        # An image whose payload region uses every value in 0-255 has no zero
        # point for the shift.
        saturated = Image.new("L", (256, 256))
        saturated.putdata([i % 256 for i in range(256 * 256)])
        with self.assertRaises(ValueError):
            rdh.hide(saturated, "hi")

    def test_image_too_small_raises(self):
        with self.assertRaises(ValueError):
            rdh.hide(Image.new("L", (4, 4)), "hi")


if __name__ == "__main__":
    unittest.main()
