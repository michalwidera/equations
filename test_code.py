#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
./test_code.py; red_green_bar.py $? $COLUMNS
red_green_bar.py is taken from https://github.com/kwadrat/rgb_tdd.git
"""

import sys
import unittest

from eisenstein import Eisenstein, gcd
from eisenstein_fractions import *
from eisenstein_operations import *
from pathlib import Path


def runningInTravis():

    home = str(Path.home())
    fields = home.strip().split("/")
    if "travis" in fields:
        return True

    return False


class TestEisensteinNumbers(unittest.TestCase):
    def test_substraction_values(self):
        """
        TestEisensteinNumbers:
        wolframalfa.com
        w = ( -1 + i sqrt(3) ) / 2 ; c = ( 1 + 2 w ) - ( 2 + 4 w )
        result: -1 - 2w
        """
        a = Eisenstein(1, 2)
        b = Eisenstein(2, 4)
        c = a - b
        self.assertEqual(c, Eisenstein(-1, -2))

    def test_add_values(self):
        """
        TestEisensteinNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; c = ( 1 + 2w ) + ( 20 + 30w )
        result: 32w + 21
        """
        a = Eisenstein(1, 2)
        b = Eisenstein(20, 30)
        c = a + b
        self.assertEqual(c, Eisenstein(21, 32))

    def test_multiplication(self):
        """
        TestEisensteinNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; c = ( 1 + 2 w ) * ( 2 + 4 w )
        answer: c = -6
        """
        a = Eisenstein(1, 2)
        b = Eisenstein(2, 4)
        c = a * b
        self.assertEqual(c, Eisenstein(-6, 0))

    def test_multiply_imag_by_imag(self):
        a = Eisenstein(0, 1)
        b = Eisenstein(0, 1)
        c = a * b
        self.assertEqual(c, Eisenstein(-1, -1))

    def test_modulo_operation(self):
        """
        TestEisensteinNumbers:

        wolframalfa.com:
        query: w = ( -1 + i sqrt(3) ) / 2 ;  (2, 0w)(2, 0w) + (1, 0w)
        expected: (5, 0w)

        query: w = ( -1 + i sqrt(3) ) / 2 ; (3, 0w) (2, 0w) + (-1, 2w)
        expected (5, 2w)

        query: w = ( -1 + i sqrt(3) ) / 2 ; (5, 1w) (1, 0w)
        expected (5, 0w)
        """
        a = 5
        self.assertEqual(1, a % 2)  # int
        a = Eisenstein(5, 0)
        self.assertEqual(Eisenstein(1, 0), a % 2)  # Eisenstein
        a = Eisenstein(5, 2)
        self.assertEqual(Eisenstein(1, 0), a % Eisenstein(2, 0))  # Eisenstein
        a = Eisenstein(5, 1)
        self.assertEqual(Eisenstein(0, 0), a % Eisenstein(1, 0))  # Eisenstein

    def test_gcd(self):
        """
        TestEisensteinNumbers:
        """
        a = Eisenstein(2, 0)
        b = Eisenstein(2, 0)
        self.assertEqual(gcd(a, b), Eisenstein(2, 0))

        a = Eisenstein(2, 0)
        b = Eisenstein(4, 0)
        self.assertEqual(gcd(a, b), Eisenstein(2, 0))

        a = Eisenstein(2, 1)
        b = Eisenstein(4, 2)
        self.assertEqual(gcd(a, b), Eisenstein(2, 1))

    def test_presentation(self):
        a = Eisenstein(2, 2)
        self.assertEqual(a.__str__(), "(2,2w)")

    def test_norm(self):
        a = Eisenstein(2, 0)
        self.assertEqual(a.get_norm, 4)
        a = Eisenstein(3, 0)
        self.assertEqual(a.get_norm, 9)
        a = Eisenstein(0, 5)
        self.assertEqual(a.get_norm, 25)
        a = Eisenstein(0, 7)
        self.assertEqual(a.get_norm, 49)
        a = Eisenstein(2, 3)
        self.assertEqual(a.get_norm, 7)

        a = Eisenstein(-2, -3)
        self.assertEqual(a.get_norm, 7)

    def test_floor_div(self):
        a = Eisenstein(3, 4)
        b = Eisenstein(11, 19)
        c = a * b
        self.assertEqual(c // a, b)

    def test_div_mod(self):
        obj_a = Eisenstein(2, 3)
        obj_b = Eisenstein(1, 0)
        self.assertEqual(obj_a / obj_b, Eisenstein(2, 3))
        self.assertEqual(obj_a // obj_b, Eisenstein(2, 3))

        obj_a = Eisenstein(4, 8)
        obj_b = Eisenstein(2, 2)
        self.assertEqual(obj_a / obj_b, Eisenstein(4, 2))
        self.assertEqual(obj_a // obj_b, Eisenstein(4, 2))


class TestEisensteinFractionNumbers(unittest.TestCase):
    def test_multiplication(self):
        """
        TestEisensteinFractionNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; c = ( 1 + 2 w ) * ( 2 + 4 w )
        answer: c = -6
        """
        a = EisensteinFraction(Fraction(1 / 2))
        b = EisensteinFraction(2)
        c = a * b
        self.assertEqual(c, 1)

        a = EisensteinFraction(Eisenstein(2, 1))
        b = EisensteinFraction(Fraction(1 / 2))
        c = a * b
        self.assertEqual(c, EisensteinFraction(1, Fraction(1 / 2)))

    def test_alternation(self):
        # covering issue __rmul__ = __mul__ ,  __radd__ = __add__
        a = Fraction(1 / 2)
        b = EisensteinFraction(2)
        c = a * b
        self.assertEqual(c, 1)

    def test_division(self):
        """
        TestEisensteinFractionNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; a = ( 2 + 4 w ); b = ( 2 + 4 w ) ; c = a / b
        answer: c = 1
        """

        a = EisensteinFraction(Fraction(1 / 2))
        b = EisensteinFraction(Fraction(4 / 2))
        c = a / b
        self.assertEqual(c, 1 / 4)

        a = EisensteinFraction(4)
        b = EisensteinFraction(2)
        c = a / b
        self.assertEqual(c, EisensteinFraction(2))

        a = EisensteinFraction(0, 2)
        b = EisensteinFraction(0, 4)
        self.assertEqual(a, EisensteinFraction(Eisenstein(0, 2)))
        self.assertEqual(b, EisensteinFraction(Eisenstein(0, 4)))
        c = a / b
        self.assertEqual(c, 1 / 2)

    def test_add_values(self):
        """
        TestEisensteinFractionNumbers:
        """

        # 2 + 2 = 4
        a = EisensteinFraction(Fraction(4 / 2))
        b = EisensteinFraction(Fraction(6 / 3))
        c = a + b
        self.assertEqual(c, 4)

        a = EisensteinFraction(Fraction(1 / 2))
        b = EisensteinFraction(Fraction(1 / 4))
        c = a + b
        self.assertEqual(c, 3 / 4)

        a = EisensteinFraction(Eisenstein(1, 1))
        b = EisensteinFraction(Eisenstein(1, -1))
        c = a + b
        self.assertEqual(c, EisensteinFraction(Eisenstein(2, 0)))

    def test_inverse(self):
        a = EisensteinFraction(Fraction(1 / 2), Fraction(1 / 2))
        c = EisensteinFraction(1) / a
        self.assertEqual(c, EisensteinFraction(0, -2))

    def test_types_mix(self):
        """
        TestEisensteinFractionNumbers:
        """

        # 2 + 2 = 4
        a = EisensteinFraction(Fraction(4 / 2))
        b = Fraction(6 / 3)
        c = a + b
        self.assertEqual(c, 4)

        a = EisensteinFraction(Fraction(1 / 2))
        b = Fraction(1 / 4)
        c = a + b
        self.assertEqual(c, 3 / 4)

        a = EisensteinFraction(Eisenstein(1, 1))
        b = Fraction(1 / 2)
        c = a + b
        self.assertEqual(c, EisensteinFraction(Fraction(3 / 2), 1))

    def test_substract_values(self):
        """
        TestEisensteinFractionNumbers:
        """

        # 2 - 2 = 0
        a = EisensteinFraction(Fraction(4 / 2))
        b = EisensteinFraction(Fraction(6 / 3))
        c = a - b
        self.assertEqual(c, 0)

        # 3/1 - 1/1 = 2/1
        a = EisensteinFraction(Fraction(3 / 1))
        b = EisensteinFraction(Fraction(1 / 1))
        c = a - b
        self.assertEqual(c, 2)

        a = EisensteinFraction(3, 1)
        b = EisensteinFraction(1, 1)
        c = a - b
        self.assertEqual(c, EisensteinFraction(2, 0))

    def test_comparasion(self):
        a = EisensteinFraction(Eisenstein(1, 2))
        b = EisensteinFraction(1, 2)
        self.assertEqual(a == b, True)

        a = Eisenstein(1, 2)
        b = EisensteinFraction(1, 2)
        self.assertEqual(a == b, True)
        self.assertEqual(b == a, True)

        a = EisensteinFraction(Fraction(1 / 2))
        b = Fraction(1 / 2)
        self.assertEqual(a == b, True)
        self.assertEqual(b == a, True)

        a = EisensteinFraction(2)
        b = 2
        self.assertEqual(a == b, True)
        self.assertEqual(b == a, True)

    def test_presentation(self):
        a = Eisenstein(2, 2)
        self.assertEqual(a.__str__(), "(2,2w)")
        a = EisensteinFraction(Fraction(1 / 2), 2)
        self.assertEqual(a.__str__(), "(1/2,2w)")

    def test_floor_and_ceil(self):
        a = EisensteinFraction(Fraction(1 / 2), 2)

        self.assertEqual(Eisenstein(0, 2), a.floor)
        self.assertEqual(Eisenstein(1, 2), a.ceil)

        a = EisensteinFraction(Fraction(1 / 3), 2)
        self.assertEqual(Eisenstein(0, 2), a.floor)
        self.assertEqual(Eisenstein(1, 2), a.ceil)

        a = EisensteinFraction(Fraction(3 / 4), Fraction(3 / 4))

        self.assertEqual(Eisenstein(0, 0), a.floor)
        self.assertEqual(Eisenstein(1, 1), a.ceil)

    def test_round(self):
        a = EisensteinFraction(Fraction(1 / 2), Fraction(3 / 4))
        self.assertEqual(Eisenstein(0, 1), a.round)

        a = EisensteinFraction(Fraction(-3 / 4), Fraction(1 / 2))
        self.assertEqual(Eisenstein(-1, 0), a.round)

    def test_abs(self):
        """
        Hint:
        abs(1+1i) = sqrt(2)
        abs(1+1w) = 1

        Beware: if you make computations via complex form you will hit 0.999 as answer
        and then you need to use self.assertAlmostEqual(1, eisensteinAbs(a), 10)
        """
        a = EisensteinFraction(1, 1)
        self.assertEqual(1, abs(a))
        a = EisensteinFraction(2, 2)
        self.assertEqual(2, abs(a))

        a = EisensteinFraction(2, 2)
        self.assertAlmostEqual(abs(a.get_complex_form), abs(a), 10)
        a = EisensteinFraction(1, 1)
        self.assertAlmostEqual(abs(a.get_complex_form), abs(a), 10)

        a = EisensteinFraction(-2, 3)
        self.assertAlmostEqual(abs(a.get_complex_form), abs(a), 10)
        a = EisensteinFraction(4, 5)
        self.assertAlmostEqual(abs(a.get_complex_form), abs(a), 10)


class TestEisensteinFractionTimeSeriesOperations(unittest.TestCase):
    def testHashOne(self):
        deltaA = EisensteinFraction(1, 0)
        deltaB = EisensteinFraction(1, 0)
        if get_dot_product(deltaA, deltaB) > 0:
            hash_result, delta_hash = hash(data_sets.A, deltaA, data_sets.B, deltaB)
            check_result_hash(hash_result)
        else:
            SystemExit("dot product =< 0")

    def testHashMatrix(self):
        if runningInTravis():
            TEST_RANGE = 10
        else:
            TEST_RANGE = 5

        for l in range(TEST_RANGE):
            for k in range(TEST_RANGE):
                for j in range(TEST_RANGE):
                    for i in range(TEST_RANGE):
                        deltaA = EisensteinFraction(i + 1, l)
                        deltaB = EisensteinFraction(j + 1, k)
                        if get_dot_product(deltaA, deltaB) > 0:
                            hash_result, delta_hash = hash(
                                data_sets.A, deltaA, data_sets.B, deltaB
                            )
                            check_result_hash(hash_result)
                        else:
                            pass
                            # ("SKIP orthogonal", deltaA, deltaB)

    def testAddMatix(self):
        if runningInTravis():
            TEST_RANGE = 10
        else:
            TEST_RANGE = 5

        for l in range(TEST_RANGE):
            for k in range(TEST_RANGE):
                for j in range(TEST_RANGE):
                    for i in range(TEST_RANGE):
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
    if runningInTravis():
        print("Wow! We are under Travis CI!")
    if len(sys.argv) >= 2 and sys.argv[1] == "--fast":
        result = perform_only_fast_tests()
    else:
        result = perform_tests()
    sys.exit(result)
