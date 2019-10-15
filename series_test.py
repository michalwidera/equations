#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need to run this with Python 3")
    sys.exit(1)

import unittest

from eisenstein_fractions import EisensteinFraction
from eisenstein import get_dot_product
from eisenstein_operations import hash_a, add
import data_sets
import parameters


def check_result_add(Var: list):

    prevNum = 1
    prevAlpha = "a"
    for (number, alpha) in Var:
        if number == prevNum or number == prevNum + 1:
            pass
        else:
            print(number, prevNum)
            raise SystemExit("Add algorithm fails")

        prevNum = number

        if alpha != prevAlpha or alpha != chr(ord(prevAlpha) + 1):
            pass
        else:
            raise SystemExit("Add algorithm fails")

        prevAlpha = alpha


def check_result_hash(Var: list):

    alpha = []
    digit = []

    for item in Var:

        if type(item) is str:
            alpha.append(item)
        else:
            digit.append(item)

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


class TestEisensteinFractionTimeSeriesOperations(unittest.TestCase):
    def testHashOne(self):
        deltaA = EisensteinFraction(1, 0)
        deltaB = EisensteinFraction(1, 0)
        if get_dot_product(deltaA, deltaB) > 0:
            hash_result, delta_hash = hash_a(data_sets.A, deltaA, data_sets.B, deltaB)
            check_result_hash(hash_result)
        else:
            SystemExit("dot product =< 0")

    def testHashMatrix(self):
        TestRange = parameters.cfg_prm.test_range

        for l in range(TestRange):
            for k in range(TestRange):
                for j in range(TestRange):
                    for i in range(TestRange):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)
                        if get_dot_product(deltaA, deltaB) > 0:
                            hash_result, delta_hash = hash_a(
                                data_sets.A, deltaA, data_sets.B, deltaB
                            )
                            check_result_hash(hash_result)
                        else:
                            pass
                            # ("SKIP orthogonal", deltaA, deltaB)

    def testAddMatix(self):
        TestRange = parameters.cfg_prm.test_range

        for l in range(TestRange):
            for k in range(TestRange):
                for j in range(TestRange):
                    for i in range(TestRange):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)

                        add_result, delta_add = add(
                            data_sets.A, deltaA, data_sets.B, deltaB
                        )
                        check_result_add(add_result)
