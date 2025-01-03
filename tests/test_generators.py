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
__date__ = "$Date: 2017/03/01 $"
__revision__ = "$Date: 2017/03/01 $"
__license__ = "GPLv3"

import itertools
import unittest

import cv2
import numpy as np

from stegano.lsb import generators


class TestGenerators(unittest.TestCase):
    def test_identity(self):
        """Test the identity generator."""
        self.assertEqual(
            tuple(itertools.islice(generators.identity(), 15)),
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
        )

    def test_fibonacci(self):
        """Test the Fibonacci generator."""
        self.assertEqual(
            tuple(itertools.islice(generators.fibonacci(), 20)),
            (
                1,
                2,
                3,
                5,
                8,
                13,
                21,
                34,
                55,
                89,
                144,
                233,
                377,
                610,
                987,
                1597,
                2584,
                4181,
                6765,
                10946,
            ),
        )

    def test_eratosthenes(self):
        """Test the Eratosthenes sieve."""
        with open("./tests/expected-results/eratosthenes") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.eratosthenes(), 168)),
                tuple(int(line) for line in f),
            )

    def test_composite(self):
        """Test the composite sieve."""
        with open("./tests/expected-results/composite") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.composite(), 114)),
                tuple(int(line) for line in f),
            )

    def test_fermat(self):
        """Test the Fermat generator."""
        with open("./tests/expected-results/fermat") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.fermat(), 9)),
                tuple(int(line) for line in f),
            )

    def test_triangular_numbers(self):
        """Test the Triangular numbers generator."""
        with open("./tests/expected-results/triangular_numbers") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.triangular_numbers(), 54)),
                tuple(int(line) for line in f),
            )

    def test_mersenne(self):
        """Test the Mersenne generator."""
        with open("./tests/expected-results/mersenne") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.mersenne(), 20)),
                tuple(int(line) for line in f),
            )

    def test_carmichael(self):
        """Test the Carmichael generator."""
        with open("./tests/expected-results/carmichael") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.carmichael(), 33)),
                tuple(int(line) for line in f),
            )

    def test_ackermann_slow(self):
        """Test the Ackermann set."""
        with open("./tests/expected-results/ackermann") as f:
            self.assertEqual(generators.ackermann_slow(3, 1), int(f.readline()))
            self.assertEqual(generators.ackermann_slow(3, 2), int(f.readline()))

    def test_ackermann_naive(self):
        """Test the Naive Ackermann generator"""
        gen = generators.ackermann_naive(3)
        next(gen)
        with open("./tests/expected-results/ackermann") as f:
            self.assertEqual(next(gen), int(f.readline()))
            self.assertEqual(next(gen), int(f.readline()))

    def test_ackermann_fast(self):
        """Test the Ackermann set."""
        with open("./tests/expected-results/ackermann") as f:
            self.assertEqual(generators.ackermann_fast(3, 1), int(f.readline()))
            self.assertEqual(generators.ackermann_fast(3, 2), int(f.readline()))
            self.assertEqual(generators.ackermann_fast(4, 1), int(f.readline()))

    def test_ackermann(self):
        """Test the Ackermann generator"""
        gen = generators.ackermann(3)
        next(gen)
        with open("./tests/expected-results/ackermann") as f:
            self.assertEqual(next(gen), int(f.readline()))
            self.assertEqual(next(gen), int(f.readline()))

    def test_LFSR(self):
        """Test the LFSR generator"""
        with open("./tests/expected-results/LFSR") as f:
            self.assertEqual(
                tuple(itertools.islice(generators.LFSR(2**8), 256)),
                tuple(int(line) for line in f),
            )

    def test_shi_tomashi(self):
        """Test the Shi Tomashi generator"""

        # The expected results are only for tests/sample-files/Montenach.png file and
        # the below mentioned shi-tomashi configuration.
        # If the values below are changed,
        # please ensure the tests/expected-results/shi_tomashi.txt
        # is also appropriately modified
        # Using the shi_tomashi_reconfigure static method

        image = cv2.imread("tests/sample-files/Montenach.png")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, 1000, 0.001, 10)
        # Commented because min_distance argument of generators.shi_tomashi is now set
        # to 10.0:
        # corners = np.int0(corners)
        corners = corners.reshape(corners.shape[0], -1)
        test_file = np.loadtxt("tests/expected-results/shi_tomashi.txt")
        test_file_reshaped = test_file.reshape(
            int(test_file.shape[0]), int(test_file.shape[1])
        )
        res = np.testing.assert_allclose(corners, test_file_reshaped, rtol=1e-0, atol=0)  # type: ignore
        self.assertIsNone(res)

    @staticmethod
    def shi_tomashi_reconfigure(
        file_name: str,
        max_corners: int = 1000,
        quality: float = 0.001,
        min_distance: int = 10,
    ):
        """
        Method to update/reconfigure Shi-Tomashi for various images and configuration
        """
        image = cv2.imread(file_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        corners = cv2.goodFeaturesToTrack(gray, max_corners, quality, min_distance)
        # Commented because min_distance argument of generators.shi_tomashi is now set
        # to 10.0:
        # corners = np.int0(corners)
        corners = corners.reshape(corners.shape[0], -1)
        np.savetxt("tests/expected-results/shi_tomashi.txt", corners)


if __name__ == "__main__":
    unittest.main()
