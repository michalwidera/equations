#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Time Series Algebra Equations Implementation - Python 3.x
   Copyright (c) 2019 Michal Widera

   https://planetmath.org/StreamInterlaceAndDeinterlace
"""

import sys

if sys.version_info[0] < 3:
    print("You need to run this with Python 3")
    sys.exit(1)

from fractions import Fraction
from math import floor, ceil

A = range(1, 24)
deltaA = Fraction(1)
B = list(map(chr, range(ord("a"), ord("z") + 1)))
deltaB = Fraction(1, 2)


def sum(A: list, deltaA: Fraction, B: list, deltaB: Fraction):

    result = []
    deltaC = min(deltaA, deltaB)

    for i in range(20):
        if deltaC == deltaA:
            result.append(str(A[i]) + B[int(i * deltaA / deltaB)])
        else:
            result.append(str(A[int(i * deltaB / deltaA)]) + B[i])
    return result, deltaC


def diff(C: list, deltaA: Fraction, deltaB: Fraction):

    result = []
    deltaC = min(deltaA, deltaB)

    for i in range(10):
        if deltaA > deltaB:
            result.append(C[int(ceil(i * deltaA / deltaB))])
        else:
            result.append(C[i])
    return result, deltaC


def fractionhash(A: list, deltaA: Fraction, B: list, deltaB: Fraction):

    result = []
    delta = deltaB / (deltaA + deltaB)

    for i in range(20):
        if floor(i * delta) == floor((i + 1) * delta):
            result.append(B[i - int(floor((i + 1) * delta))])
        else:
            result.append(A[int(floor(i * delta))])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC


def dehasheven(C: list, deltaC: Fraction, deltaA: Fraction):

    result = []
    deltaB = deltaA * deltaC / (deltaA - deltaC)

    for i in range(6):
        result.append(C[i + int(ceil((i + 1) * deltaA / deltaB))])
    return result, deltaB


def dehashodd(C: list, deltaC: Fraction, deltaB: Fraction):

    result = []
    deltaA = deltaB * deltaC / (deltaB - deltaC)

    for i in range(6):
        result.append(C[i + int(i * deltaB / deltaA)])
    return result, deltaA


def vdeltaA(n: int):
    return Fraction(1, 1) + Fraction(n, 20)


def vdeltaB(n: int):
    return Fraction(1, 1) + Fraction(n, 10)


def z(i: int):
    return vdeltaB(i) / (vdeltaA(i) + vdeltaB(i))


def vhash():

    result = []
    for i in range(20):
        if int(i * z(i)) == int((i + 1) * z(i + 1)):
            result.append(B[i - int((i) * z(i))])
        else:
            result.append(A[int(i * z(i))])
    return result


def main():
    hash_result, delta_hash = fractionhash(A, deltaA, B, deltaB)
    sum_result, delta_sum = sum(A, deltaA, B, deltaB)

    print("Sum:", sum(A, deltaA, B, deltaB))
    print("Diff:", diff(sum_result, deltaA, deltaB))

    print("Hash:", fractionhash(A, deltaA, B, deltaB))
    print("dehasheven:", dehasheven(hash_result, delta_hash, deltaA))
    print("dehashodd:", dehashodd(hash_result, delta_hash, deltaB))

    print("vhash", vhash())


if __name__ == "__main__":
    main()
