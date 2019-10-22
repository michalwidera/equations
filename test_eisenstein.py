#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

import unittest

from eisenstein import Eisenstein, gcd


class TestEisensteinNumbers(unittest.TestCase):
    def test_true_div(self):
        """
        This code is to better understand meaning of eisenstein division
        :return:
        """
        selfy = Eisenstein(1, 2)
        other = 2

        a = selfy.co_real
        b = selfy.co_omega
        if type(other) is int:
            g = a / other
            h = b / other
        else:
            c = other.co_real
            d = other.co_omega
            bottom = other.get_norm
            e = a * c + b * d - a * d
            f = b * c - a * d
            g = e / bottom
            h = f / bottom
        result = Eisenstein(int(g), int(h))

        self.assertEqual(result, selfy.__floordiv__(other))

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

        a = Eisenstein(1, 2)
        b = 1
        c = a + b
        self.assertEqual(c, Eisenstein(2, 2))

        a = Eisenstein(1, 2)
        b = 1
        c = b + a
        self.assertEqual(c, Eisenstein(2, 2))

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

        a = Eisenstein(1, 2)
        b = 2
        c = a * b
        self.assertEqual(c, Eisenstein(2, 4))

        a = Eisenstein(1, 2)
        b = 2
        c = b * a
        self.assertEqual(c, Eisenstein(2, 4))

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
        self.assertEqual(Eisenstein(1, 0), a % Eisenstein(2, 0))  # Eisenstein
        a = Eisenstein(5, 2)
        self.assertEqual(Eisenstein(1, 0), a % Eisenstein(2, 0))  # Eisenstein
        a = Eisenstein(5, 1)
        self.assertEqual(Eisenstein(0, 0), a % Eisenstein(1, 0))  # Eisenstein

        a = Eisenstein(5, 2)
        self.assertEqual(Eisenstein(1, 0), a % 2)  # Eisenstein
        a = Eisenstein(5, 1)
        self.assertEqual(Eisenstein(0, 0), a % 1)  # Eisenstein

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
        self.assertEqual(str(a), "Eisenstein(2, 2)")

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
        obj_c = 2
        # self.assertEqual(obj_a / obj_b, Eisenstein(2, 3)) Not allowed!
        self.assertEqual(obj_a // obj_b, Eisenstein(2, 3))
        self.assertEqual(obj_a // obj_c, Eisenstein(1, 1))

        obj_a = Eisenstein(4, 8)
        obj_b = Eisenstein(2, 2)
        obj_c = 2
        # self.assertEqual(obj_a / obj_b, Eisenstein(4, 2)) Not allowed!
        self.assertEqual(obj_a // obj_b, Eisenstein(4, 2))
        self.assertEqual(obj_a // obj_c, Eisenstein(2, 4))

    def test_both_div_and_modulo(self):
        a = Eisenstein(4, 1)
        b = Eisenstein(3, 1)
        c = Eisenstein(2, 1)
        d = a * b + c
        e, f = d.div_mod(a)
        self.assertEqual(e, Eisenstein(3, 1))
        self.assertEqual(f, Eisenstein(7, 2))
