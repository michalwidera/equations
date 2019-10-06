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

        self.assertEqual(Eisenstein(0, 2), eisensteinFloor(a))
        self.assertEqual(Eisenstein(1, 2), eisensteinCeil(a))

        a = EisensteinFraction(Fraction(1 / 3), 2)
        self.assertEqual(Eisenstein(0, 2), eisensteinFloor(a))
        self.assertEqual(Eisenstein(1, 2), eisensteinCeil(a))

        a = EisensteinFraction(Fraction(3 / 4), Fraction(3 / 4))

        self.assertEqual(Eisenstein(0, 0), eisensteinFloor(a))
        self.assertEqual(Eisenstein(1, 1), eisensteinCeil(a))

    def test_round(self):
        a = EisensteinFraction(Fraction(1 / 2), Fraction(3 / 4))
        self.assertEqual(Eisenstein(0, 1), eisensteinRound(a))

        a = EisensteinFraction(Fraction(-3 / 4), Fraction(1 / 2))
        self.assertEqual(Eisenstein(-1, 0), eisensteinRound(a))

    def test_abs(self):
        """
        Hint:
        abs(1+1i) = sqrt(2)
        abs(1+1w) = 1 or 0.999999(9) and this should be fixed
        """
        a = EisensteinFraction(1, 1)
        # self.assertAlmostEqual(1, eisensteinAbs(a), 10)
        self.assertEqual(1, eisensteinAbs(a))


fast_test_ls = [TestEisensteinNumbers, TestEisensteinFractionNumbers]


def add_all_fast(suite):
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    return summary_status(suite)


if __name__ == "__main__":
    result = perform_tests()
    sys.exit(result)
