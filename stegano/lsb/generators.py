#!/usr/bin/env python
# Stegano - Stegano is a pure Python steganography module.
# Copyright (C) 2010-2024 Cédric Bonhomme - https://www.cedricbonhomme.org
#
# For more information : https://git.sr.ht/~cedric/stegano
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
__date__ = "$Date: 2011/12/28 $"
__revision__ = "$Date: 2021/11/29 $"
__license__ = "GPLv3"

import itertools
import math
from typing import Any, Dict, Iterator, List

import cv2
import numpy as np


def identity() -> Iterator[int]:
    """f(x) = x"""
    n = 0
    while True:
        yield n
        n += 1


def triangular_numbers() -> Iterator[int]:
    """Triangular numbers: a(n) = C(n+1,2) = n(n+1)/2 = 0+1+2+...+n.
    http://oeis.org/A000217
    """
    n = 0
    while True:
        yield (n * (n + 1)) // 2
        n += 1


def fermat() -> Iterator[int]:
    """Generate the n-th Fermat Number.
    https://oeis.org/A000215
    """
    y = 3
    while True:
        yield y
        y = pow(y - 1, 2) + 1


def mersenne() -> Iterator[int]:
    """Generate 2^p - 1, where p is prime.
    https://oeis.org/A001348
    """
    prime_numbers = eratosthenes()
    while True:
        yield 2 ** next(prime_numbers) - 1


def eratosthenes() -> Iterator[int]:
    """Generate the prime numbers with the sieve of Eratosthenes.
    https://oeis.org/A000040
    """
    d: Dict[int, List[int]] = {}
    for i in itertools.count(2):
        if i in d:
            for j in d[i]:
                d[i + j] = d.get(i + j, []) + [j]
            del d[i]
        else:
            d[i * i] = [i]
            yield i


def composite() -> Iterator[int]:
    """Generate the composite numbers using the sieve of Eratosthenes.
    https://oeis.org/A002808
    """
    p1 = 3
    for p2 in eratosthenes():
        yield from range(p1 + 1, p2)
        p1 = p2


def carmichael() -> Iterator[int]:
    """Composite numbers n such that a^(n-1) == 1 (mod n) for every a coprime
    to n.
    https://oeis.org/A002997
    """
    for m in composite():
        for a in range(2, m):
            if pow(a, m, m) != a:
                break
        else:
            yield m


def ackermann_slow(m: int, n: int) -> int:
    """Ackermann number."""
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann_slow(m - 1, 1)
    else:
        return ackermann_slow(m - 1, ackermann_slow(m, n - 1))


def ackermann_naive(m: int) -> Iterator[int]:
    """Naive Ackermann encapsulated in a generator."""
    n = 0
    while True:
        yield ackermann_slow(m, n)
        n += 1


def ackermann_fast(m: int, n: int) -> int:
    """Ackermann number."""
    while m >= 4:
        if n == 0:
            n = 1
        else:
            n = ackermann_fast(m, n - 1)
        m -= 1
    if m == 3:
        return (1 << n + 3) - 3
    elif m == 2:
        return (n << 1) + 3
    elif m == 1:
        return n + 2
    else:
        return n + 1


def ackermann(m: int) -> Iterator[int]:
    """Ackermann encapsulated in a generator."""
    n = 0
    while True:
        yield ackermann_fast(m, n)
        n += 1


def fibonacci() -> Iterator[int]:
    """Generate the sequence of Fibonacci.
    https://oeis.org/A000045
    """
    a, b = 1, 2
    while True:
        yield a
        a, b = b, a + b


def log_gen() -> Iterator[int]:
    """Logarithmic generator."""
    y = 1
    while True:
        adder = max(1, math.pow(10, int(math.log10(y))))
        yield int(y)
        y = y + int(adder)


polys = {
    2: [2, 1],
    3: [3, 1],
    4: [4, 1],
    5: [5, 2],
    6: [6, 1],
    7: [7, 1],
    8: [8, 4, 3, 2],
    9: [9, 4],
    10: [10, 3],
    11: [11, 2],
    12: [12, 6, 4, 1],
    13: [13, 4, 3, 1],
    14: [14, 8, 6, 1],
    15: [15, 1],
    16: [16, 12, 3, 1],
    17: [17, 3],
    18: [18, 7],
    19: [19, 5, 2, 1],
    20: [20, 3],
    21: [21, 2],
    22: [22, 1],
    23: [23, 5],
    24: [24, 7, 2, 1],
    25: [25, 3],
    26: [26, 6, 2, 1],
    27: [27, 5, 2, 1],
    28: [28, 3],
    29: [29, 2],
    30: [30, 23, 2, 1],
    31: [31, 3],
}


def LFSR(m: int) -> Iterator[int]:
    """LFSR generator of the given size
    https://en.wikipedia.org/wiki/Linear-feedback_shift_register
    """
    n: int = m.bit_length() - 1
    # Set initial state to {1 0 0 ... 0}
    state: List[int] = [0] * n
    state[0] = 1
    feedback: int = 0
    poly: List[int] = polys[n]
    while True:
        # Compute the feedback bit
        feedback = 0
        for i in range(len(poly)):
            feedback = feedback ^ state[poly[i] - 1]
        # Roll the registers
        state.pop()
        # Add the feedback bit
        state.insert(0, feedback)
        # Convert the registers to an int
        out = sum(e * (2**i) for i, e in enumerate(state))
        yield out


def shi_tomashi(
    image_path: str,
    max_corners: int = 100,
    quality: float = 0.01,
    min_distance: float = 10.0,
) -> Iterator[int]:
    """Shi-Tomachi corner generator of the given points
    https://docs.opencv.org/4.x/d4/d8c/tutorial_py_shi_tomasi.html
    """
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners: np.ndarray = cv2.goodFeaturesToTrack(
        gray, max_corners, quality, min_distance
    )
    corners_int: np.ndarray[Any, np.dtype[np.signedinteger[Any]]] = np.array(
        np.intp(corners)
    )
    i = 0
    while True:
        x, y = corners_int[i].ravel()
        # Compute the pixel number with top left of image as origin
        # using coordinates of the corner.
        # (y * number of pixels a row) + pixels left in last row
        yield (y * image.shape[1]) + x
        i += 1
