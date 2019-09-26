#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions and Time Series Algebra mix - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
   https://planetmath.org/StreamInterlaceAndDeinterlace
"""

from eisenstein import *

# TODO I'm not sure how to interpret delta as EisnensteinFraction maybe there should appear norm function and delta
#  became variable like in vhash?
A = range(1, 24)
deltaA = EisensteinFraction(1, 2)
B = list(map(chr, range(ord("a"), ord("z") + 1)))
deltaB = EisensteinFraction(1, 1)


def hash(A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction):
    # TODO check if we need here hash of vhash from operations.py or something completly different
    result = []
    delta = deltaB / (deltaA + deltaB)

    for i in range(20):
        if floor(i * delta) == floor((i + 1) * delta):
            result.append(B[i - floor((i + 1) * delta)])
        else:
            result.append(A[floor(i * delta)])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC


def main():
    hash_result, delta_hash = hash(A, deltaA, B, deltaB)
    print("Hash:", hash(A, deltaA, B, deltaB))


if __name__ == "__main__":
    main()
