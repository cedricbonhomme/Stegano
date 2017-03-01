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
__version__ = "$Revision: 0.1 $"
__date__ = "$Date: 2017/03/01 $"
__revision__ = "$Date: 2017/03/01 $"
__license__ = "GPLv3"

import unittest
import itertools

from stegano.lsbset import generators

class TestGenerators(unittest.TestCase):

    def test_identity(self):
        """
        Test the identity generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.identity(), 15)),
                        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))

    def test_fibonacci(self):
        """
        Test the Fibonacci generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.fibonacci(), 20)),
                        (1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
                        987, 1597, 2584, 4181, 6765, 10946))

    def test_fermat(self):
        """
        Test the Fermat generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.fermat(), 9)),
                        (3, 5, 17, 257, 65537, 4294967297, 18446744073709551617,
                        340282366920938463463374607431768211457,
                        115792089237316195423570985008687907853269984665640564039457584007913129639937))

    def test_triangular_numbers(self):
        """
        Test the Triangular numbers generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.triangular_numbers(), 54)),
                        (0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91,
                        105, 120, 136, 153, 171, 190, 210, 231, 253, 276, 300,
                        325, 351, 378, 406, 435, 465, 496, 528, 561, 595, 630,
                        666, 703, 741, 780, 820, 861, 903, 946, 990, 1035, 1081,
                        1128, 1176, 1225, 1275, 1326, 1378, 1431))

    # def test_mersenne(self):
    #     """
    #     Test the Mersenne generator.
    #     """
    #     self.assertEqual(tuple(itertools.islice(generators.mersenne(), 20)),
    #                     (3, 7, 31, 127, 2047, 8191, 131071, 524287, 8388607,
    #                     536870911, 2147483647, 137438953471, 2199023255551,
    #                     8796093022207, 140737488355327, 9007199254740991,
    #                     576460752303423487, 2305843009213693951,
    #                     147573952589676412927, 2361183241434822606847))



if __name__ == '__main__':
    unittest.main()
