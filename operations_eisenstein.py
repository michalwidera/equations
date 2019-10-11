#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions and Time Series Algebra mix - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
   https://planetmath.org/StreamInterlaceAndDeinterlace
"""

import data_sets
from eisenstein_fractions import *
from eisenstein import get_dot_product

# TODO I'm not sure how to interpret delta as EisnensteinFraction
#  maybe there should appear norm function and delta
#  became variable like in vhash?
deltaA = EisensteinFraction(1, 2)
deltaB = EisensteinFraction(1, 1)

PROBE_LEN = 40

verbose_result = 0


def hash(A: list, deltaA: EisensteinFraction, B: list, deltaB: EisensteinFraction):
    # TODO check if we need here hash of vhash from operations.py or something completly different
    result = []
    delta = deltaB / (deltaA + deltaB)
    # abs_delta = delta.get_norm
    # print(abs_delta)

    for i in range(PROBE_LEN):
        di = i * delta
        if int(abs(di)) == int(abs(di + delta)):
            result.append(B[i - int(abs(di))])
        else:
            result.append(A[int(abs(di))])

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
            if item != data_sets.A[index]:
                print("Fail A:", item, data_sets.A[index])
                print("len A:", len(alpha), "len B:", len(digit))
                raise SystemExit("This algorithm fails A")

        for index, item in enumerate(alpha):
            if item != data_sets.B[index]:
                print("Fail B:", item, data_sets.B[index])
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
        hash_result, delta_hash = hash(data_sets.A, deltaA, data_sets.B, deltaB)
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
                        if get_dot_product(deltaA, deltaB) > 0:
                            hash_result, delta_hash = hash(
                                data_sets.A, deltaA, data_sets.B, deltaB
                            )
                            print(
                                "DeltaA, DeltaB:",
                                deltaA,
                                deltaB,
                                get_dot_product(deltaA, deltaB),
                                get_dot_product(deltaB, deltaB + deltaA),
                            )
                            print("Hash:", hash_result, delta_hash)

                            check_result(hash_result)
                        else:
                            print("SKIP orthogonal", deltaA, deltaB)
        ##############################################################################


if __name__ == "__main__":
    main()
