#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Gaussian Rational Fractions Type Implementation - Python 3.x

   Rational complex numbers a + b*i, where a, b are Fractions.
   https://en.wikipedia.org/wiki/Gaussian_rational
"""

import sys

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

from fractions import Fraction


class GaussFraction:
    def __init__(self, co_real=0, co_imag=0):
        if not isinstance(co_real, (int, Fraction)) or not isinstance(
            co_imag, (int, Fraction)
        ):
            raise TypeError("Arguments should be ints or Fractions")
        self.co_real = Fraction(co_real)
        self.co_imag = Fraction(co_imag)

    def __str__(self):
        return "GaussFraction(%s, %s)" % (self.co_real, self.co_imag)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if isinstance(other, (int, Fraction)):
            other = GaussFraction(other)
        return self.co_real == other.co_real and self.co_imag == other.co_imag

    def __add__(self, other):
        if isinstance(other, (int, Fraction)):
            other = GaussFraction(other)
        return GaussFraction(self.co_real + other.co_real, self.co_imag + other.co_imag)

    def __sub__(self, other):
        if isinstance(other, (int, Fraction)):
            other = GaussFraction(other)
        return GaussFraction(self.co_real - other.co_real, self.co_imag - other.co_imag)

    def __mul__(self, other):
        # (a+bi)(c+di) = (ac-bd) + (ad+bc)i
        if isinstance(other, (int, Fraction)):
            other = GaussFraction(other)
        return GaussFraction(
            self.co_real * other.co_real - self.co_imag * other.co_imag,
            self.co_real * other.co_imag + self.co_imag * other.co_real,
        )

    def __truediv__(self, other):
        # x / y = x * conj(y) / N(y)
        if isinstance(other, (int, Fraction)):
            other = GaussFraction(other)
        n = other.get_norm
        return self * GaussFraction(other.co_real / n, -other.co_imag / n)

    __rmul__ = __mul__
    __radd__ = __add__

    @property
    def get_norm(self) -> Fraction:
        """
        Norm in algebraic sense: a^2 + b^2 = |a+bi|^2.
        Exact Fraction - use it instead of abs() (abs would need a square root).
        """
        return self.co_real ** 2 + self.co_imag ** 2


def get_dot_product(x: GaussFraction, y: GaussFraction) -> Fraction:
    """
    Dot product Re(x * conj(y)) = ac + bd.
    """
    return x.co_real * y.co_real + x.co_imag * y.co_imag
