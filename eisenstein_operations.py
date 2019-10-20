#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions and Time Series Algebra mix - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
   https://planetmath.org/StreamInterlaceAndDeinterlace
"""

import sys
import math

if sys.version_info[0] < 3:
    print("You need to run this with Python 3")
    sys.exit(1)

from eisenstein_fractions import EisensteinFraction
from eisenstein import get_dot_product

# TODO: Implement all functions from operations.py based on EisensteinFarction type and cover UT
# DONE: add_Eisenstein_Fraction
# DONE: diff_Eisenstein_Fraction
# DONE: hash_Eisenstein_Fraction
# TODO: dehasheven_Eisenstein_Fraction
# TODO: dehashodd_Eisenstein_Fraction

PROBE_LEN = 40

# Code under test
def hash_Eisenstein_Fraction(
    A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction
):
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
        ii = EisensteinFraction(four=(i, 1, 0, 1))
        di = ii * delta
        if int(abs(di)) == int(abs(di + delta)):
            result.append(B[i - int(abs(di))])
        else:
            result.append(A[int(abs(di))])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC


# Code under test
def add_Eisenstein_Fraction(
    A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction
):
    result = []
    if abs(deltaA) < abs(deltaB):
        deltaC = deltaA
    else:
        deltaC = deltaB

    for i in range(PROBE_LEN):
        ii = EisensteinFraction(four=(i, 1, 0, 1))
        if deltaC == deltaA:
            first = A[i]
            second = B[int(abs((ii * deltaA / deltaB)))]
        else:
            first = A[int(abs((ii * deltaB / deltaA)))]
            second = B[i]
        result.append((first, second))
    return result, deltaC


# Code under development
def diff_Eisenstein_Fraction(
    C: list, deltaA: EisensteinFraction, deltaB: EisensteinFraction
):

    result = []
    # deltaC = min(deltaA, deltaB)
    if abs(deltaA) < abs(deltaB):
        deltaC = deltaA
    else:
        deltaC = deltaB

    for i in range(PROBE_LEN):
        ii = EisensteinFraction(four=(i, 1, 0, 1))
        if abs(deltaA) > abs(deltaB):
            idx = int(math.ceil(abs(ii * deltaA / deltaB)))
        else:
            idx = i
        if idx >= len(C):
            return result, deltaC
        result.append(C[idx])
    return result, deltaC
