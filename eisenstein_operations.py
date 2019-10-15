#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions and Time Series Algebra mix - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
   https://planetmath.org/StreamInterlaceAndDeinterlace
"""

import sys

if sys.version_info[0] < 3:
    print("You need to run this with Python 3")
    sys.exit(1)

import data_sets
from eisenstein_fractions import EisensteinFraction
from eisenstein import get_dot_product

# TODO I'm not sure how to interpret delta as EisnensteinFraction
#  maybe there should appear norm function and delta
#  became variable like in vhash?

PROBE_LEN = 40

# code under test
def hash_a(A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction):
    """
    This is hash function for Time series that interwave two Time Series that
    time steps are computed by a+bw number that a,b are EisensteinFractions

    This is hash_a because Python have hash method in standard lib i.e. __hash__()
    hash_b is declared in operations.py (for rational coefficients)
    """
    # get_dot_product works for Eisenstein and EisensteinFraction
    # this requirement was invented during experimental work with equations
    assert get_dot_product(deltaA, deltaB) > 0

    result = []
    delta = deltaB / (deltaA + deltaB)

    for i in range(PROBE_LEN):
        di = i * delta
        if int(abs(di)) == int(abs(di + delta)):
            result.append(B[i - int(abs(di))])
        else:
            result.append(A[int(abs(di))])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC


def add(A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction):
    result = []
    if abs(deltaA) < abs(deltaB):
        deltaC = deltaA
    else:
        deltaC = deltaB

    for i in range(PROBE_LEN):
        if deltaC == deltaA:
            first = A[i]
            second = B[int(abs(i * deltaA / deltaB))]
        else:
            first = A[int(abs((i * deltaB / deltaA)))]
            second = B[i]
        result.append((first, second))
    return result, deltaC


if __name__ == "__main__":
    pass
