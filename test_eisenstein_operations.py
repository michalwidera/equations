#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

import unittest
import data_sets
import parameters

from eisenstein_fractions import EisensteinFraction
from eisenstein import get_dot_product
from eisenstein_operations import (
    hash_Eisenstein_Fraction,
    add_Eisenstein_Fraction,
    diff_Eisenstein_Fraction,
)


# dehasheven_Eisenstein_Fraction,
# dehashodd_Eisenstein_Fraction,

# A = range(1, 50)
# B = a,b,c ...


def check_result_is_only_number_sequence(Var: list):
    index = 0
    for number in Var:

        if number == data_sets.A[index]:
            pass
        else:
            return True
        index = index + 1
    return False


def check_result_is_only_alpha_sequence(Var: list):
    index = 0
    for alpha in Var:

        if alpha == data_sets.B[index]:
            pass
        else:
            return True
        index = index + 1
    return False


def check_result_is_number_sequence(Var: list):
    index = 0
    for (number, alpha) in Var:

        if number == data_sets.A[index]:
            pass
        else:
            return True
        index = index + 1
    return False


def check_result_is_alpha_sequence(Var: list):
    index = 0
    for (number, alpha) in Var:

        if alpha == data_sets.B[index]:
            pass
        else:
            return True
        index = index + 1
    return False


def check_result_add(Var: list):
    """
    This check goes through Var list (1,a)(2,a)(3,b) ...
    and test if 1>=2>=3>=4
    and a>=b>=c>=
    It means it fails if it not grows
    :param Var: result from add operation
    :return: True if need RaiseException, false - eveything ok
    """
    prevNum = 1
    prevAlpha = "a"
    for (number, alpha) in Var:
        if number == prevNum or number == prevNum + 1:
            pass
        else:
            return True

        prevNum = number

        if alpha != prevAlpha or alpha != chr(ord(prevAlpha) + 1):
            pass
        else:
            return True

        prevAlpha = alpha

    return False


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
    def test_hash_one(self):
        deltaA = EisensteinFraction(1, 0)
        deltaB = EisensteinFraction(1, 0)
        if get_dot_product(deltaA, deltaB) > 0:
            hash_result, delta_hash = hash_Eisenstein_Fraction(
                data_sets.A, deltaA, data_sets.B, deltaB
            )
            check_result_hash(hash_result)
        else:
            SystemExit("dot product =< 0")

    def test_hash_matrix(self):
        TestRange = parameters.cfg_prm.test_range

        for l in range(TestRange):
            for k in range(TestRange):
                for j in range(TestRange):
                    for i in range(TestRange):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)
                        if get_dot_product(deltaA, deltaB) > 0:
                            hash_result, delta_hash = hash_Eisenstein_Fraction(
                                data_sets.A, deltaA, data_sets.B, deltaB
                            )
                            check_result_hash(hash_result)
                        else:
                            pass
                            # ("SKIP orthogonal", deltaA, deltaB)

    def test_add_matrix(self):
        TestRange = parameters.cfg_prm.test_range

        for l in range(TestRange):
            for k in range(TestRange):
                for j in range(TestRange):
                    for i in range(TestRange):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)

                        add_result, delta_add = add_Eisenstein_Fraction(
                            data_sets.A, deltaA, data_sets.B, deltaB
                        )
                        if check_result_add(add_result):
                            raise SystemExit("Add algorithm fails")

    def test_check_function(self):
        """
        This function test check_result_is_number_sequence
        and check_result_is_alpha_sequence
        Both directions - success and failure scenario
        :return:
        """
        var = []
        var.append((1, "a"))
        var.append((2, "b"))
        var.append((3, "c"))
        var.append((4, "d"))
        var.append((5, "e"))
        # This is success scenario
        if check_result_is_number_sequence(var):
            raise SystemExit("Number Fails")
        if check_result_is_alpha_sequence(var):
            raise SystemExit("Alpha Fails")

        # This is alpha failure scenario
        var.append((6, "e"))
        if check_result_is_number_sequence(var):
            raise SystemExit("Number Fails")
        if not check_result_is_alpha_sequence(var):
            raise SystemExit("Alpha Fails")

        # This is number failure scenario
        var.append((6, "e"))
        if not check_result_is_number_sequence(var):
            raise SystemExit("Number Fails")
        if not check_result_is_alpha_sequence(var):
            raise SystemExit("Alpha Fails")

        # Rough check of check_result_add
        if check_result_add(var):
            raise SystemExit("Check sequence Fails")

        # Missing 7 scenario - should be recognized
        var.append((8, "e"))
        if not check_result_add(var):
            raise SystemExit("Check sequence Fails")

    def test_add_diff_matrix(self):
        TestRange = parameters.cfg_prm.test_range

        for l in range(TestRange):
            for k in range(TestRange):
                for j in range(TestRange):
                    for i in range(TestRange):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)

                        add_result, delta_add = add_Eisenstein_Fraction(
                            data_sets.A, deltaA, data_sets.B, deltaB
                        )

                        if check_result_add(add_result):
                            raise SystemExit("Add algorithm fails")

                        diff_result, delta_diff = diff_Eisenstein_Fraction(
                            add_result, deltaA, deltaB
                        )

                        if check_result_is_number_sequence(diff_result):
                            print()
                            print(deltaA)
                            print(deltaA)
                            print("argument:", add_result)
                            print("result: ", diff_result)
                            raise SystemExit("Diff algorithm fails")

                        diff_result, delta_diff = diff_Eisenstein_Fraction(
                            add_result, deltaB, deltaA
                        )

                        if check_result_is_alpha_sequence(diff_result):
                            print()
                            print(deltaA)
                            print(deltaA)
                            print("argument:", add_result)
                            print("result: ", diff_result)
                            raise SystemExit("Diff algorithm fails")

    """
    def test_dehash_matrix(self):
        TestRange = parameters.cfg_prm.test_range

        callCount = 0
        for l in range(TestRange):
            for k in range(TestRange):
                for j in range(TestRange):
                    for i in range(TestRange):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)
                        if get_dot_product(deltaA, deltaB) > 0:
                            hash_result, delta_hash = hash_Eisenstein_Fraction(
                                data_sets.A, deltaA, data_sets.B, deltaB
                            )
                            #check_result_hash(hash_result) Already checked
                            callCount += 1
                            dehashOdd_result, delta_dehashOdd = dehashodd_Eisenstein_Fraction(
                                hash_result, delta_hash, deltaB
                            )

                            assert delta_dehashOdd == deltaA

                            if check_result_is_only_alpha_sequence(dehashOdd_result):
                                print()
                                print("call count", callCount)
                                print(l, k, j, i)
                                print(deltaA, deltaB, get_dot_product(deltaA, deltaB))
                                print((deltaA/deltaB), (deltaB/deltaA))
                                print(hash_result)
                                print(dehashOdd_result)
                                raise SystemExit(
                                    "dehasheven_Eisenstein_Fraction algorithm fails"
                                )

                        else:
                            pass
                            # ("SKIP orthogonal", deltaA, deltaB)
    """
