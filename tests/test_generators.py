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
        """Test the identity generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.identity(), 15)),
                        (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))

    def test_fibonacci(self):
        """Test the Fibonacci generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.fibonacci(), 20)),
                        (1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
                        987, 1597, 2584, 4181, 6765, 10946))

    def test_eratosthenes(self):
        """Test the Eratosthenes sieve.
        """
        self.assertEqual(tuple(itertools.islice(generators.eratosthenes(), 168)),
                        (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                        53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
                        109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167,
                        173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
                        233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283,
                        293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359,
                        367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431,
                        433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491,
                        499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571,
                        577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641,
                        643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
                        719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787,
                        797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859,
                        863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
                        947, 953, 967, 971, 977, 983, 991, 997))

    def test_composite(self):
        """Test the composite sieve.
        """
        self.assertEqual(tuple(itertools.islice(generators.composite(), 114)),
                        (4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25,
                        26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44,
                        45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62,
                        63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80,
                        81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96,
                        98, 99, 100, 102, 104, 105, 106, 108, 110, 111, 112,
                        114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
                        125, 126, 128, 129, 130, 132, 133, 134, 135, 136, 138,
                        140, 141, 142, 143, 144, 145, 146, 147, 148, 150))

    def test_fermat(self):
        """Test the Fermat generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.fermat(), 9)),
                        (3, 5, 17, 257, 65537, 4294967297, 18446744073709551617,
                        340282366920938463463374607431768211457,
                        115792089237316195423570985008687907853269984665640564039457584007913129639937))

    def test_triangular_numbers(self):
        """Test the Triangular numbers generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.triangular_numbers(), 54)),
                        (0, 1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91,
                        105, 120, 136, 153, 171, 190, 210, 231, 253, 276, 300,
                        325, 351, 378, 406, 435, 465, 496, 528, 561, 595, 630,
                        666, 703, 741, 780, 820, 861, 903, 946, 990, 1035, 1081,
                        1128, 1176, 1225, 1275, 1326, 1378, 1431))

    def test_mersenne(self):
        """Test the Mersenne generator.
        """
        with open('./tests/expected-results/mersenne', 'r') as f: 
            self.assertEqual(tuple(itertools.islice(generators.mersenne(), 20)),
                             tuple(int(line) for line in f))

    def test_carmichael(self):
        """Test the Carmichael generator.
        """
        self.assertEqual(tuple(itertools.islice(generators.carmichael(), 33)),
                        (561, 1105, 1729, 2465, 2821, 6601, 8911, 10585, 15841,
                        29341, 41041, 46657, 52633, 62745, 63973, 75361, 101101,
                         115921, 126217, 162401, 172081, 188461, 252601, 278545,
                          294409, 314821, 334153, 340561, 399001, 410041,
                          449065, 488881, 512461))

    def test_ackermann_naive(self):
        """Test the Ackermann set.
        """

        self.assertEqual(generators.ackermann(3, 1), 13)
        self.assertEqual(generators.ackermann(3, 2), 29)

    def test_ackermann(self):
        """Test the Ackermann set.
        """
        self.assertEqual(generators.ackermann(3, 1), 13)
        self.assertEqual(generators.ackermann(3, 2), 29)
        self.assertEqual(generators.ackermann(4, 1), 65533)
        with open('./tests/expected-results/ackermann', 'r') as f:
            self.assertEqual(generators.ackermann(4, 2), int(f.readline())) 

if __name__ == '__main__':
    unittest.main()
