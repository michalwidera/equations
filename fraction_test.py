#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need to run this with Python 3")
    sys.exit(1)

import unittest
from fractions import Fraction

from eisenstein import Eisenstein
from eisenstein_fractions import EisensteinFraction


class TestEisensteinFractionNumbers(unittest.TestCase):
    def test_multiplication(self):
        """
        TestEisensteinFractionNumbers:
        wolframalfa.com
        query: w = ( -1 + i sqrt(3) ) / 2 ; c = ( 1 + 2 w ) * ( 2 + 4 w )
        answer: c = -6
        """
        a = EisensteinFraction(Fraction(1, 2))
        b = EisensteinFraction(2)
        c = a * b
        self.assertEqual(c, 1)

        a = EisensteinFraction(Eisenstein(2, 1))
        b = EisensteinFraction(Fraction(1, 2))
        c = a * b
        self.assertEqual(c, EisensteinFraction(1, Fraction(1, 2)))

    def test_alternation(self):
        # covering issue __rmul__ = __mul__ ,  __radd__ = __add__
        a = Fraction(1, 2)
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

        a = EisensteinFraction(Fraction(1, 2))
        b = EisensteinFraction(Fraction(4, 2))
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
        a = EisensteinFraction(Fraction(4, 2))
        b = EisensteinFraction(Fraction(6, 3))
        c = a + b
        self.assertEqual(c, 4)

        a = EisensteinFraction(Fraction(1, 2))
        b = EisensteinFraction(Fraction(1, 4))
        c = a + b
        self.assertEqual(c, 3 / 4)

        a = EisensteinFraction(Eisenstein(1, 1))
        b = EisensteinFraction(Eisenstein(1, -1))
        c = a + b
        self.assertEqual(c, EisensteinFraction(Eisenstein(2, 0)))

    def test_inverse(self):
        a = EisensteinFraction(Fraction(1, 2), Fraction(1, 2))
        c = EisensteinFraction(1) / a
        self.assertEqual(c, EisensteinFraction(0, -2))

    def test_types_mix(self):
        """
        TestEisensteinFractionNumbers:
        """

        # 2 + 2 = 4
        a = EisensteinFraction(Fraction(4, 2))
        b = Fraction(6, 3)
        c = a + b
        self.assertEqual(c, 4)

        a = EisensteinFraction(Fraction(1, 2))
        b = Fraction(1, 4)
        c = a + b
        self.assertEqual(c, 3 / 4)

        a = EisensteinFraction(Eisenstein(1, 1))
        b = Fraction(1, 2)
        c = a + b
        self.assertEqual(c, EisensteinFraction(Fraction(3, 2), 1))

    def test_substract_values(self):
        """
        TestEisensteinFractionNumbers:
        """

        # 2 - 2 = 0
        a = EisensteinFraction(Fraction(4, 2))
        b = EisensteinFraction(Fraction(6, 3))
        c = a - b
        self.assertEqual(c, 0)

        # 3/1 - 1/1 = 2/1
        a = EisensteinFraction(Fraction(3, 1))
        b = EisensteinFraction(Fraction(1, 1))
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

        a = EisensteinFraction(Fraction(1, 2))
        b = Fraction(1, 2)
        self.assertEqual(a == b, True)
        self.assertEqual(b == a, True)

        a = EisensteinFraction(2)
        b = 2
        self.assertEqual(a == b, True)
        self.assertEqual(b == a, True)

    def test_presentation(self):
        a = Eisenstein(2, 2)
        self.assertEqual(a.__str__(), "(2,2w)")
        a = EisensteinFraction(Fraction(1, 2), 2)
        self.assertEqual(a.__str__(), "(1/2,2w)")

    def test_floor_and_ceil(self):
        a = EisensteinFraction(Fraction(1, 2), 2)

        self.assertEqual(Eisenstein(0, 2), a.floor)
        self.assertEqual(Eisenstein(1, 2), a.ceil)

        a = EisensteinFraction(Fraction(1, 3), 2)
        self.assertEqual(Eisenstein(0, 2), a.floor)
        self.assertEqual(Eisenstein(1, 2), a.ceil)

        a = EisensteinFraction(Fraction(3, 4), Fraction(3, 4))

        self.assertEqual(Eisenstein(0, 0), a.floor)
        self.assertEqual(Eisenstein(1, 1), a.ceil)

    def test_round(self):
        a = EisensteinFraction(Fraction(1, 2), Fraction(3, 4))
        self.assertEqual(Eisenstein(0, 1), a.round)

        a = EisensteinFraction(Fraction(-3, 4), Fraction(1, 2))
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
