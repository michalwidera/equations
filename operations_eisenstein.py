#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions and Time Series Algebra mix - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
   https://planetmath.org/StreamInterlaceAndDeinterlace
"""

from eisenstein_fractions import *

# TODO I'm not sure how to interpret delta as EisnensteinFraction
#  maybe there should appear norm function and delta
#  became variable like in vhash?
A = range(1, 50)
deltaA = EisensteinFraction(1, 2)
B = list(map(chr, range(ord("a"), ord("z") + 1)))
B = B + B + B + B
deltaB = EisensteinFraction(1, 1)

PROBE_LEN = 20

def hash(A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction):
    # TODO check if we need here hash of vhash from operations.py or something completly different
    result = []
    delta = deltaB / (deltaA + deltaB)

    for i in range(PROBE_LEN):
        if floor(i * abs(delta)) == floor((i + 1) * abs(delta)):
            result.append(B[i - floor((i + 1) * abs(delta))])
        else:
            result.append(A[floor(i * abs(delta))])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC

def check_result( Var: list):

    alpha = []
    digit = []

    for item in Var:

        try:
            if item.isalpha():
                alpha.append( item )
        except:
            digit.append( item )

    print(alpha)
    print(digit)

    if digit:
        for index,item in enumerate(digit):
            if item != A[index]:
                print("Fail:" , item , A[index])
                raise SystemExit('This algorithm fails A')

        for index,item in enumerate(alpha):
            if item != B[index]:
                rint("Fail:", item, B[index])
                raise SystemExit('This algorithm fails B')
def main():
    for j in range(20):
        for i in range(20):
            deltaA = EisensteinFraction(1, i)
            deltaB = EisensteinFraction(1, j)
            hash_result, delta_hash = hash(A, deltaA, B, deltaB)
            print("DeltaA, DeltaB:", deltaA , deltaB )
            print("Hash:", hash_result , delta_hash)

            check_result( hash_result )

if __name__ == "__main__":
    main()
