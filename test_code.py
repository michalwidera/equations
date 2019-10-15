#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
./test_code.py --fast; red_green_bar.py $? $COLUMNS
red_green_bar.py is taken from https://github.com/kwadrat/rgb_tdd.git
"""

import sys
import unittest
from pathlib import Path

from eisenstein_fractions import EisensteinFraction
from eisenstein_operations import hash_a, add
from eisenstein import get_dot_product
from number_test import TestEisensteinNumbers
from fraction_test import TestEisensteinFractionNumbers
import data_sets
import parameters


def runningInTravis():

    home = str(Path.home())
    fields = home.strip().split("/")
    if "travis" in fields:
        return True

    return False


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


fast_test_ls = [TestEisensteinNumbers, TestEisensteinFractionNumbers]


slow_test_ls = [TestEisensteinFractionTimeSeriesOperations]


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


def add_all_fast(suite):
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def add_all_slow(suite):
    for one_test in slow_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_only_fast_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    return summary_status(suite)


def perform_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    add_all_slow(suite)
    return summary_status(suite)


if __name__ == "__main__":
    result = 1  # assuming failure of test script
    if len(sys.argv) >= 2 and sys.argv[1] == "--fast":
        result = perform_only_fast_tests()
    elif len(sys.argv) >= 3 and sys.argv[1] == "--setscale":
        TestRange = int(sys.argv[2])
        parameters.cfg_prm.set_range(TestRange)
        result = perform_tests()
    elif runningInTravis():
        print("Wow! We are under Travis CI!")
        TestRange = 10
        parameters.cfg_prm.set_range(TestRange)
        result = perform_tests()
    else:
        result = perform_tests()  # go ahead with defaults
    sys.exit(result)
