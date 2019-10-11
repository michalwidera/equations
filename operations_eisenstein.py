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

PROBE_LEN = 40

verbose_result = 0

def hash(A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction):
    # TODO check if we need here hash of vhash from operations.py or something completly different
    result = []
    delta = deltaB / (deltaA + deltaB)
    abs_delta = delta.get_norm
    print(abs_delta)

    for i in range(PROBE_LEN):
        if abs((i * delta).floor) == abs(((i + 1) * delta).floor):
            result.append(B[i - int(abs((i * delta).floor))])
        else:
            result.append(A[int(abs((i * delta).floor))])

    deltaC = (deltaA * deltaB) / (deltaA + deltaB)
    return result, deltaC


def check_result(Var: list):

    alpha = []
    digit = []

    for item in Var:

        if type(item) is str:
            alpha.append(item)
        else:
            digit.append(item)

    if verbose_result:
        tmp_format = "alpha"
        print("Eval: %s %s" % (tmp_format, eval(tmp_format)))
        tmp_format = "digit"
        print("Eval: %s %s" % (tmp_format, eval(tmp_format)))

    if digit:
        for index, item in enumerate(digit):
            if item != A[index]:
                print("Fail A:", item, A[index])
                print("len A:", len(alpha), "len B:", len(digit))
                raise SystemExit("This algorithm fails A")

        for index, item in enumerate(alpha):
            if item != B[index]:
                print("Fail B:", item, B[index])
                print("len A:", len(alpha), "len B:", len(digit))
                raise SystemExit("This algorithm fails B")


def main():
    if 0:
        ##############################################################################
        j = 4
        i = 0
        tmp_format = "j, i"
        print("Eval: %s %s" % (tmp_format, eval(tmp_format)))
        deltaA = EisensteinFraction(1, i)
        deltaB = EisensteinFraction(1, j)
        tmp_format = "deltaA"
        print("Eval: %s %s" % (tmp_format, eval(tmp_format)))
        tmp_format = "deltaB"
        print("Eval: %s %s" % (tmp_format, eval(tmp_format)))
        hash_result, delta_hash = hash(A, deltaA, B, deltaB)
        print("DeltaA, DeltaB:", deltaA, deltaB)
        print("Hash:", hash_result, delta_hash)

        check_result(hash_result)
        ##############################################################################
    else:
        ##############################################################################
        for l in range(20):
            for k in range(20):
                for j in range(20):
                    for i in range(20):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)
                        hash_result, delta_hash = hash(A, deltaA, B, deltaB)
                        print("DeltaA, DeltaB:", deltaA, deltaB)
                        print("Hash:", hash_result, delta_hash)

                        check_result(hash_result)
        ##############################################################################


if __name__ == "__main__":
    main()
