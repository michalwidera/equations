#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
./test_code.py; red_green_bar.py $? $COLUMNS
red_green_bar.py is taken from https://github.com/kwadrat/rgb_tdd.git
"""

import sys
import unittest

from eisenstein import Eisenstein, EisensteinFraction, gcd
from fractions import Fraction


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


class TestEisensteinFractionNumbers(unittest.TestCase):
    def test_multiplication(self):
        """
        TestEisensteinFractionNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; c = ( 1 + 2 w ) * ( 2 + 4 w )
        answer: c = -6
        """
        a = EisensteinFraction(Eisenstein(1, 0), Eisenstein(2, 0))
        b = EisensteinFraction(Eisenstein(4, 0), Eisenstein(2, 0))
        c = a * b
        self.assertEqual(c, EisensteinFraction(Eisenstein(1, 0), Eisenstein(1, 0)))

    def test_division(self):
        """
        TestEisensteinFractionNumbers:
        wolframalfa.com
        query: w = w = ( -1 + i sqrt(3) ) / 2 ; a = ( 2 + 4 w ); b = ( 2 + 4 w ) ; c = a / b
        answer: c = 1
        """

        a = EisensteinFraction(Eisenstein(1, 0), Eisenstein(2, 0))
        b = EisensteinFraction(Eisenstein(2, 0), Eisenstein(4, 0))
        c = a / b
        self.assertEqual(c, EisensteinFraction(1))

        a = EisensteinFraction(4)
        b = EisensteinFraction(2)
        c = a / b
        self.assertEqual(c, EisensteinFraction(2))

    def test_add_values(self):
        """
        TestEisensteinFractionNumbers:
        """

        a = EisensteinFraction(4, 2)
        b = EisensteinFraction(6, 3)
        c = a + b
        self.assertEqual(c, EisensteinFraction(4))

        a = EisensteinFraction(1, 2)
        b = EisensteinFraction(1, 4)
        c = a + b
        self.assertEqual(c, EisensteinFraction(3, 4))

        a = EisensteinFraction(Eisenstein(1, 1), 1)
        b = EisensteinFraction(Eisenstein(1, -1), 1)
        c = a + b
        self.assertEqual(c, EisensteinFraction(2, 1))

        a = EisensteinFraction(0, Eisenstein(2, -1))
        b = EisensteinFraction(0, Eisenstein(1, 1))
        c = a + b
        self.assertEqual(c, EisensteinFraction(0, 1))

    def test_substract_values(self):
        """
        TestEisensteinFractionNumbers:
        """

        # 2 - 2 = 0
        a = EisensteinFraction(4, 2)
        b = EisensteinFraction(6, 3)
        c = a - b
        self.assertEqual(c, EisensteinFraction(0, 1))

        # 3/1 - 1/1 = 2/1
        a = EisensteinFraction(3, 1)
        b = EisensteinFraction(1, 1)
        c = a - b
        self.assertEqual(c, EisensteinFraction(2, 1))

        # (3,1)/1 - 1/1 = 2/1
        a = EisensteinFraction(Eisenstein(3, 1), 1)
        b = EisensteinFraction(1, 1)
        c = a - b
        self.assertEqual(c, EisensteinFraction(Eisenstein(2, 1), 1))

    def test_fraction_format_values(self):
        a = EisensteinFraction(Eisenstein(3, 1), 1)
        self.assertEqual(a.get_fraction_form_real, 3)
        self.assertEqual(a.get_fraction_form_imag, 1)

        a = EisensteinFraction(3, 2)
        self.assertEqual(a.get_fraction_form_real, Fraction(3 / 2))
        self.assertEqual(a.get_fraction_form_imag, Fraction(0))

        # That blow my mind!
        b = EisensteinFraction(Eisenstein(0, 30), Eisenstein(0, 20))
        self.assertEqual(b.get_fraction_form_real, Fraction(3 / 2))
        self.assertEqual(b.get_fraction_form_imag, Fraction(0 / 1))

        a = EisensteinFraction(Eisenstein(3, 1), 2)
        self.assertEqual(a.get_fraction_form_real, Fraction(3 / 2))
        self.assertEqual(a.get_fraction_form_imag, Fraction(1 / 2))


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
