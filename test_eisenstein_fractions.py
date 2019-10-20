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
        self.assertEqual(c, Eisenstein(1))

        a = EisensteinFraction(Eisenstein(2, 1))
        b = EisensteinFraction(Fraction(1, 2))
        c = a * b
        self.assertEqual(c, EisensteinFraction(1, Fraction(1, 2)))

    def test_alternation(self):
        # covering issue __rmul__ = __mul__ ,  __radd__ = __add__
        a = EisensteinFraction(Fraction(1, 2))
        b = EisensteinFraction(2)
        c = a * b
        self.assertEqual(c, EisensteinFraction(four=(1, 1, 0, 1)))

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
        self.assertEqual(c, EisensteinFraction(four=(1, 4, 0, 1)))

        a = EisensteinFraction(4)
        b = EisensteinFraction(2)
        c = a / b
        self.assertEqual(c, EisensteinFraction(2))

        a = EisensteinFraction(0, 2)
        b = EisensteinFraction(0, 4)
        self.assertEqual(a, EisensteinFraction(Eisenstein(0, 2)))
        self.assertEqual(b, EisensteinFraction(Eisenstein(0, 4)))
        c = a / b
        self.assertEqual(c, EisensteinFraction(four=(1, 2, 0, 1)))

    def test_add_values(self):
        # 2 + 2 = 4
        a = EisensteinFraction(Fraction(4, 2))
        b = EisensteinFraction(Fraction(6, 3))
        c = a + b
        self.assertEqual(c, EisensteinFraction(four=(4, 1, 0, 1)))

        a = EisensteinFraction(Fraction(1, 2))
        b = EisensteinFraction(Fraction(1, 4))
        c = a + b
        self.assertEqual(c, EisensteinFraction(four=(3, 4, 0, 1)))

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
        b = EisensteinFraction(Fraction(6, 3))
        c = a + b
        self.assertEqual(c, EisensteinFraction(four=(4, 1, 0, 1)))

        a = EisensteinFraction(Fraction(1, 2))
        b = EisensteinFraction(Fraction(1, 4))
        c = a + b
        self.assertEqual(c, EisensteinFraction(four=(3, 4, 0, 1)))

        a = EisensteinFraction(Eisenstein(1, 1))
        b = EisensteinFraction(Fraction(1, 2))
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
        self.assertEqual(c, EisensteinFraction(four=(0, 1, 0, 1)))

        # 3/1 - 1/1 = 2/1
        a = EisensteinFraction(Fraction(3, 1))
        b = EisensteinFraction(Fraction(1, 1))
        c = a - b
        self.assertEqual(c, EisensteinFraction(four=(2, 1, 0, 1)))

        a = EisensteinFraction(3, 1)
        b = EisensteinFraction(1, 1)
        c = a - b
        self.assertEqual(c, EisensteinFraction(2, 0))

    def test_comparison(self):
        a = EisensteinFraction(Eisenstein(1, 2))
        b = EisensteinFraction(1, 2)
        self.assertEqual(a == b, True)

        a = Eisenstein(1, 2)
        b = EisensteinFraction(1, 2)
        self.assertEqual(a == b, True)
        self.assertEqual(b == a, True)

    def test_presentation(self):
        a = Eisenstein(2, 2)
        self.assertEqual(str(a), "Eisenstein(2, 2)")
        a = EisensteinFraction(Fraction(1, 2), 2)
        self.assertEqual(str(a), "EisensteinFraction(four=(1, 2, 2, 1))")

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

    def test_four_parts(self):
        obj = EisensteinFraction(four=(1, 2, 3, 4))
        self.assertEqual(str(obj), "EisensteinFraction(four=(1, 2, 3, 4))")
        obj = EisensteinFraction(four=(5, 6, 7, 11))
        self.assertEqual(str(obj), "EisensteinFraction(four=(5, 6, 7, 11))")

    def test_two_parts(self):
        a = Fraction(12, 13)
        b = Fraction(-17, 19)
        c = EisensteinFraction(two=(a, b))
        self.assertEqual(str(c), "EisensteinFraction(four=(12, 13, -17, 19))")

    def test_another_add_values(self):
        a = EisensteinFraction(four=(1, 2, 3, 4))
        b = EisensteinFraction(four=(1, 3, 3, 4))
        c = a + b
        self.assertEqual(str(c), "EisensteinFraction(four=(5, 6, 3, 2))")

        a = EisensteinFraction(four=(1, 2, 3, 4))
        c = a + 2
        self.assertEqual(str(c), "EisensteinFraction(four=(5, 2, 3, 4))")

        a = EisensteinFraction(four=(1, 2, 3, 4))
        c = a + Eisenstein(2)
        self.assertEqual(str(c), "EisensteinFraction(four=(5, 2, 3, 4))")

    def test_another_substract_values(self):
        a = EisensteinFraction(four=(1, 2, 3, 4))
        b = EisensteinFraction(four=(1, 3, 3, 4))
        c = a - b
        self.assertEqual(str(c), "EisensteinFraction(four=(1, 6, 0, 1))")

        a = EisensteinFraction(four=(1, 1, 3, 4))
        c = a - 1
        self.assertEqual(str(c), "EisensteinFraction(four=(0, 1, 3, 4))")

    def test_multiply_values(self):
        a = EisensteinFraction(four=(1, 2, 3, 5))
        b = EisensteinFraction(four=(7, 11, 13, 17))
        c = a * b
        self.assertEqual(c.math_view(), "(-263/1870, 571/1870w)")
        self.assertEqual(str(c), "EisensteinFraction(four=(-263, 1870, 571, 1870))")
        self.assertEqual(repr(c), "EisensteinFraction(four=(-263, 1870, 571, 1870))")

    def test_no_arguments(self):
        self.assertRaises(TypeError, EisensteinFraction)

    def test_norm(self):
        obj_a = EisensteinFraction(four=(1, 1, 1, 1))
        self.assertEqual(obj_a.get_norm, 1)
        obj_a = EisensteinFraction(four=(1, 1, 1, 2))
        self.assertEqual(obj_a.get_norm, Fraction(3, 4))

    def test_compare_values(self):
        obj_a = EisensteinFraction(four=(2, 4, 2, 3))
        obj_b = EisensteinFraction(four=(1, 2, 6, 9))
        self.assertEqual(obj_a == obj_b, True)

    def test_div_mod(self):
        obj_a = EisensteinFraction(four=(2, 1, 3, 1))
        obj_b = EisensteinFraction(four=(1, 1, 0, 1))
        obj_c = obj_a / obj_b
        self.assertEqual(obj_c, EisensteinFraction(four=(2, 1, 3, 1)))

        obj_a = EisensteinFraction(four=(4, 1, 6, 1))
        obj_b = EisensteinFraction(four=(1, 1, 0, 1))
        obj_c = obj_a / 2
        self.assertEqual(obj_c, EisensteinFraction(four=(2, 1, 3, 1)))

    def test_fraction_as_integer(self):
        a = EisensteinFraction(four=(2, 1, -3, 1))
        self.assertEqual(str(a), "Eisenstein(2, -3)")

    def test_division_by_eisenstein(self):
        a = EisensteinFraction(four=(1, 1, -3, 2))
        b = a / Eisenstein(2)
        self.assertEqual(b, EisensteinFraction(four=(1, 2, -3, 4)))
        c = a / Eisenstein(3, 0)
        self.assertEqual(c, EisensteinFraction(four=(1, 3, -1, 2)))

    def test_division_by_integer(self):
        a = EisensteinFraction(four=(1, 1, -3, 2)) / 2
        self.assertEqual(a, EisensteinFraction(four=(1, 2, -3, 4)))
        b = Eisenstein(2, 0) / 2
        self.assertEqual(b, EisensteinFraction(four=(1, 1, 0, 1)))
        c = Eisenstein(4, 0) / 2
        self.assertEqual(c, EisensteinFraction(four=(2, 1, 0, 1)))
        # this is Integer+Integer(w) Numbers div

    def test_multiplication_by_integer(self):
        a = 2 * EisensteinFraction(four=(1, 1, -3, 2))
        self.assertEqual(a, EisensteinFraction(four=(2, 1, -6, 2)))
        b = 2 * Eisenstein(2, 0)
        self.assertEqual(b, EisensteinFraction(four=(4, 1, 0, 1)))
        a = EisensteinFraction(four=(1, 1, -3, 2)) * 2
        self.assertEqual(a, EisensteinFraction(four=(2, 1, -6, 2)))
        b = Eisenstein(2, 0) * 2
        self.assertEqual(b, EisensteinFraction(four=(4, 1, 0, 1)))
