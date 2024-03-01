#!/usr/bin/env python

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
__version__ = "$Revision: 0.9.4 $"
__date__ = "$Date: 2019/06/06 $"
__revision__ = "$Date: 2019/06/06 $"
__license__ = "GPLv3"

import unittest

from PIL import Image, ImageChops

from stegano import lsb
from stegano.steganalysis import parity, statistics


class TestSteganalysis(unittest.TestCase):
    def test_parity(self):
        """Test stegano.steganalysis.parity"""
        text_file_to_hide = "./tests/sample-files/lorem_ipsum.txt"
        with open(text_file_to_hide) as f:
            message = f.read()
        secret = lsb.hide("./tests/sample-files/Lenna.png", message)
        analysis = parity.steganalyse(secret)
        target = Image.open("./tests/expected-results/parity.png")
        diff = ImageChops.difference(target, analysis).getbbox()
        self.assertTrue(diff is None)

    def test_parity_rgba(self):
        """Test that stegano.steganalysis.parity works with RGBA images"""
        img = Image.open("./tests/sample-files/transparent.png")
        analysis = parity.steganalyse(img)
        target = Image.open("./tests/expected-results/parity_rgba.png")
        diff = ImageChops.difference(target, analysis).getbbox()
        self.assertTrue(diff is None)

    def test_statistics(self):
        """Test stegano.steganalysis.statistics"""
        image = Image.open("./tests/sample-files/Lenna.png")
        stats = str(statistics.steganalyse(image)) + "\n"
        file = open("./tests/expected-results/statistics")
        target = file.read()
        file.close()
        self.assertEqual(stats, target)


if __name__ == "__main__":
    unittest.main()
