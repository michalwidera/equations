#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

import random
import unittest
from fractions import Fraction
from math import ceil, floor, sqrt

import data_sets
import parameters
import test_eisenstein_operations as eis_checks

from gauss_fractions import GaussFraction, get_dot_product
from gauss_operations import (
    add_Gauss_Fraction,
    ceil_sqrt,
    dehasheven_Gauss_Fraction,
    dehashodd_Gauss_Fraction,
    diff_Gauss_Fraction,
    floor_abs_multiple,
    floor_sqrt,
    hash_Gauss_Fraction,
)


def matrix_pairs():
    TestRange = parameters.cfg_prm.test_range
    for l in range(TestRange):
        for k in range(TestRange):
            for j in range(TestRange):
                for i in range(TestRange):
                    yield GaussFraction(i + 1, l), GaussFraction(j + 1, k)


def random_pairs(count=300, seed=1):
    """Pary o ujemnych i ulamkowych skladowych, ktorych macierz nie obejmuje."""
    rng = random.Random(seed)

    def q():
        return Fraction(rng.randint(-12, 12), rng.randint(1, 12))

    while count:
        deltaA, deltaB = GaussFraction(q(), q()), GaussFraction(q(), q())
        if deltaA.get_norm == 0 or deltaB.get_norm == 0:
            continue
        count -= 1
        yield deltaA, deltaB


def check_hash_dehash(test, deltaA, deltaB):
    hash_result, delta_hash = hash_Gauss_Fraction(data_sets.A, deltaA, data_sets.B, deltaB)
    eis_checks.check_result_hash(hash_result)

    odd_result, delta_odd = dehashodd_Gauss_Fraction(hash_result, delta_hash, deltaB)
    test.assertEqual(delta_odd, deltaA)
    test.assertTrue(eis_checks.check_result_is_only_alpha_sequence(odd_result))

    even_result, delta_even = dehasheven_Gauss_Fraction(hash_result, delta_hash, deltaA)
    test.assertEqual(delta_even, deltaB)
    test.assertTrue(eis_checks.check_result_is_only_number_sequence(even_result))


def check_add_diff(test, deltaA, deltaB):
    add_result, delta_add = add_Gauss_Fraction(data_sets.A, deltaA, data_sets.B, deltaB)
    test.assertFalse(eis_checks.check_result_add(add_result))

    diff_result, delta_diff = diff_Gauss_Fraction(add_result, deltaA, deltaB)
    test.assertFalse(eis_checks.check_result_is_number_sequence(diff_result))

    diff_result, delta_diff = diff_Gauss_Fraction(add_result, deltaB, deltaA)
    test.assertFalse(eis_checks.check_result_is_alpha_sequence(diff_result))


class TestGaussFractionNumbers(unittest.TestCase):
    def test_multiplication(self):
        # (1+2i)(3-i) = 5+5i
        self.assertEqual(GaussFraction(1, 2) * GaussFraction(3, -1), GaussFraction(5, 5))
        self.assertEqual(2 * GaussFraction(Fraction(1, 2), 1), GaussFraction(1, 2))

    def test_division(self):
        a = GaussFraction(Fraction(1, 3), Fraction(-2, 5))
        b = GaussFraction(Fraction(7, 2), 4)
        self.assertEqual((a / b) * b, a)
        self.assertEqual(GaussFraction(1) / GaussFraction(0, 1), GaussFraction(0, -1))

    def test_norm_and_dot(self):
        self.assertEqual(GaussFraction(3, 4).get_norm, 25)
        self.assertEqual(GaussFraction(Fraction(1, 2), Fraction(1, 2)).get_norm, Fraction(1, 2))
        self.assertEqual(get_dot_product(GaussFraction(1, 2), GaussFraction(3, -1)), 1)

    def test_no_float_arguments(self):
        self.assertRaises(TypeError, GaussFraction, 0.5)


class TestExactModulus(unittest.TestCase):
    def test_floor_ceil_sqrt_brute_force(self):
        for num in range(0, 300):
            for den in range(1, 40):
                x = Fraction(num, den)
                f = floor_sqrt(x)
                self.assertTrue(f * f <= x < (f + 1) ** 2)
                c = ceil_sqrt(x)
                self.assertTrue(c * c >= x and (c == 0 or (c - 1) ** 2 < x))

    def test_float_sqrt_is_wrong_where_isqrt_is_right(self):
        # x = 10^16 - 1/3 lezy tuz pod kwadratem 10^8; float(x) zaokragla do 10^16.
        x = Fraction(10 ** 16) - Fraction(1, 3)
        self.assertEqual(int(float(x) ** 0.5), 10 ** 8)
        self.assertEqual(floor_sqrt(x), 10 ** 8 - 1)

    def test_float_complex_abs_trap(self):
        # Dla tej pary floor(n*|delta|) liczony przez abs(complex(float, float))
        # myli sie przy n = 26 (N(delta) = 1/4, 26*|delta| = 13).
        deltaA = GaussFraction(Fraction(-1, 2), -1)
        deltaB = GaussFraction(Fraction(1, 6), -1)
        delta = deltaB / (deltaA + deltaB)
        n = 26
        di = n * delta
        float_floor = floor(abs(complex(float(di.co_real), float(di.co_imag))))
        self.assertEqual(floor_abs_multiple(n, delta), 13)
        self.assertNotEqual(float_floor, 13)
        check_hash_dehash(self, deltaA, deltaB)


class TestGaussFractionTimeSeriesOperations(unittest.TestCase):
    def test_hash_dehash_matrix(self):
        for deltaA, deltaB in matrix_pairs():
            if get_dot_product(deltaA, deltaB) > 0:
                check_hash_dehash(self, deltaA, deltaB)

    def test_add_diff_matrix(self):
        for deltaA, deltaB in matrix_pairs():
            check_add_diff(self, deltaA, deltaB)

    def test_hash_dehash_random(self):
        for deltaA, deltaB in random_pairs():
            if get_dot_product(deltaA, deltaB) > 0:
                check_hash_dehash(self, deltaA, deltaB)

    def test_add_diff_random(self):
        for deltaA, deltaB in random_pairs():
            check_add_diff(self, deltaA, deltaB)


if __name__ == "__main__":
    unittest.main()
