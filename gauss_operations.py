#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Gaussian Rational Fractions and Time Series Algebra mix - Python 3.x

   Same equations as eisenstein_operations.py, time steps are a+bi numbers
   with rational a, b.

   Moduly nie sa liczone przez abs(), float ani complex. |z| = sqrt(N(z)), gdzie
   norma N(z) jest dokladnym ulamkiem, wiec porownania modulow sa porownaniami
   norm, a floor/ceil z modulu licza sie na liczbach calkowitych (math.isqrt).
"""

import sys

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

from fractions import Fraction
from math import ceil, floor, isqrt

from gauss_fractions import GaussFraction, get_dot_product

# Length of tested probe. Based on this value following functions will create
# loops that will return combined series of data.
PROBE_LEN = 40


def floor_sqrt(x: Fraction) -> int:
    """floor(sqrt(x)) dla wymiernego x >= 0, bez liczb zmiennoprzecinkowych."""
    assert x >= 0
    return isqrt(floor(x))


def ceil_sqrt(x: Fraction) -> int:
    """ceil(sqrt(x)) dla wymiernego x >= 0, bez liczb zmiennoprzecinkowych."""
    assert x >= 0
    if x == 0:
        return 0
    return isqrt(ceil(x) - 1) + 1


def floor_abs_multiple(n: int, z: GaussFraction) -> int:
    """floor(n * |z|) = floor(sqrt(n^2 * N(z)))."""
    return floor_sqrt(n * n * z.get_norm)


def abs_less(x: GaussFraction, y: GaussFraction) -> bool:
    """|x| < |y| <=> N(x) < N(y)."""
    return x.get_norm < y.get_norm


def hash_Gauss_Fraction(A: list, deltaA: GaussFraction, B: list, deltaB: GaussFraction):
    """
    Interleave of two time series, time steps are Gaussian rationals.
    """

    assert get_dot_product(deltaA, deltaB) > 0

    result = []
    delta = deltaB / (deltaA + deltaB)

    for i in range(PROBE_LEN):
        k = floor_abs_multiple(i, delta)
        if k == floor_abs_multiple(i + 1, delta):
            result.append(B[i - k])
        else:
            result.append(A[k])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC


def add_Gauss_Fraction(A: list, deltaA: GaussFraction, B: list, deltaB: GaussFraction):
    """
    Function combine two series. If values of first comming slower
    Data will be duplicated to faster series.
    """

    result = []
    if abs_less(deltaA, deltaB):
        deltaC = deltaA
    else:
        deltaC = deltaB

    for i in range(PROBE_LEN):
        if deltaC == deltaA:
            first = A[i]
            second = B[floor_sqrt(i * i * deltaA.get_norm / deltaB.get_norm)]
        else:
            first = A[floor_sqrt(i * i * deltaB.get_norm / deltaA.get_norm)]
            second = B[i]
        result.append((first, second))
    return result, deltaC


def diff_Gauss_Fraction(C: list, deltaA: GaussFraction, deltaB: GaussFraction):
    """
    Function gets primary form argument based on given deltas.
    If we gathering data from slower series, faster
    data will be truncated. If we quering same speed - no probes
    will be dropped.
    """

    result = []
    if abs_less(deltaA, deltaB):
        deltaC = deltaA
    else:
        deltaC = deltaB

    for i in range(PROBE_LEN):
        if abs_less(deltaB, deltaA):
            idx = ceil_sqrt(i * i * deltaA.get_norm / deltaB.get_norm)
        else:
            idx = i
        if idx >= len(C):
            return result, deltaC
        result.append(C[idx])
    return result, deltaC


def dehasheven_Gauss_Fraction(C: list, deltaC: GaussFraction, deltaA: GaussFraction):

    result = []

    # This condition should be true because Hashed TS should be faster than argument
    assert abs_less(deltaC, deltaA)

    deltaB = (deltaA * deltaC) / (deltaA - deltaC)

    assert abs_less(deltaC, deltaB)

    delta = deltaB / (deltaA + deltaB)

    for i in range(PROBE_LEN):
        if floor_abs_multiple(i, delta) == floor_abs_multiple(i + 1, delta):
            continue
        if i >= len(C):
            return result, deltaB
        result.append(C[i])
    return result, deltaB


def dehashodd_Gauss_Fraction(C: list, deltaC: GaussFraction, deltaB: GaussFraction):

    result = []

    # This condition should be true because Hashed TS should be faster than argument
    assert abs_less(deltaC, deltaB)

    deltaA = deltaB * deltaC / (deltaB - deltaC)

    assert abs_less(deltaC, deltaA)

    delta = deltaB / (deltaA + deltaB)

    for i in range(PROBE_LEN):
        if floor_abs_multiple(i, delta) != floor_abs_multiple(i + 1, delta):
            continue
        if i >= len(C):
            return result, deltaA
        result.append(C[i])
    return result, deltaA
