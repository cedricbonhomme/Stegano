#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Stéganô - Stéganô is a basic Python Steganography module.
# Copyright (C) 2010-2019  Cédric Bonhomme - https://www.cedricbonhomme.org
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
__version__ = "$Revision: 0.3 $"
__date__ = "$Date: 2011/12/28 $"
__revision__ = "$Date: 2017/03/10 $"
__license__ = "GPLv3"

import math
import itertools
from typing import Iterator, List, Dict

def identity() -> Iterator[int]:
    """f(x) = x
    """
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
        yield (n*(n+1))//2
        n += 1

def fermat() -> Iterator[int]:
    """Generate the n-th Fermat Number.
    https://oeis.org/A000215
    """
    y = 3
    while True:
        yield y
        y = pow(y-1,2)+1

def mersenne() -> Iterator[int]:
    """Generate 2^p - 1, where p is prime.
    https://oeis.org/A001348
    """
    prime_numbers = eratosthenes()
    while True:
        yield 2**next(prime_numbers) - 1

def eratosthenes() -> Iterator[int]:
    """Generate the prime numbers with the sieve of Eratosthenes.
    https://oeis.org/A000040
    """
    d = {} # type: Dict[int, List[int]]
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
        for n in range(p1 + 1, p2):
            yield n
        p1 = p2

def carmichael() -> Iterator[int]:
    """Composite numbers n such that a^(n-1) == 1 (mod n) for every a coprime
    to n.
    https://oeis.org/A002997
    """
    for m in composite():
        for a in range(2, m):
            if pow(a,m,m) != a:
                break
        else:
            yield m

def ackermann_naive(m: int, n: int) -> int:
    """Ackermann number.
    """
    if m == 0:
        return n + 1
    elif n == 0:
        return ackermann(m - 1, 1)
    else:
        return ackermann(m - 1, ackermann(m, n - 1))

def ackermann(m: int, n: int) -> int:
    """Ackermann number.
    """
    while m >= 4:
        if n == 0:
            n = 1
        else:
            n = ackermann(m, n - 1)
        m -= 1
    if m == 3:
        return (1 << n + 3) - 3
    elif m == 2:
        return (n << 1) + 3
    elif m == 1:
        return n + 2
    else:
        return n + 1

def fibonacci() -> Iterator[int]:
    """Generate the sequence of Fibonacci.
    https://oeis.org/A000045
    """
    a, b = 1, 2
    while True:
        yield a
        a, b = b, a + b

def log_gen() -> Iterator[int]:
    """Logarithmic generator.
    """
    y = 1
    while True:
        adder = max(1, math.pow(10, int(math.log10(y))))
        yield int(y)
        y = y + int(adder)
