#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions Type Implementation - Python 3.x

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
"""

# https://docs.python.org/3.7/reference/datamodel.html

import sys
from fractions import Fraction

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

SQRT_THREE: float = 3.0 ** 0.5


class Eisenstein:
    def __init__(self, co_real, co_omega=0):

        assert isinstance(co_real, int)
        assert isinstance(co_omega, int)
        self.co_real = co_real
        self.co_omega = co_omega

    def __str__(self):
        if self.co_real.denominator == self.co_omega.denominator == 1:
            result = "Eisenstein(%d, %d)" % (
                self.co_real.numerator,
                self.co_omega.numerator,
            )
        else:
            result = "EisensteinFraction(four=(%d, %d, %d, %d))" % (
                self.co_real.numerator,
                self.co_real.denominator,
                self.co_omega.numerator,
                self.co_omega.denominator,
            )
        return result

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.co_real == other.co_real and self.co_omega == other.co_omega

    def __add__(self, other):
        return Eisenstein(self.co_real + other.co_real, self.co_omega + other.co_omega)

    def __sub__(self, other):
        return Eisenstein(self.co_real - other.co_real, self.co_omega - other.co_omega)

    def __mul__(self, other):
        # (a+bw)(c+dw)=(ac-bd)+(bc+ad-db)w
        # https://en.wikipedia.org/wiki/Eisenstein_integer

        if isinstance(other, int):
            other = Eisenstein(other)

        return Eisenstein(
            (self.co_real * other.co_real) - (self.co_omega * other.co_omega),
            (self.co_omega * other.co_real)
            + (self.co_real * other.co_omega)
            - (self.co_omega * other.co_omega),
        )

    def __abs__(self):
        """
        Absolute Value of a Complex Number.
        The absolute value of a complex number , a+bi (also called the modulus )
        is defined as the distance between the origin (0,0) and the point (a,b)
        in the complex plane.

        If you use complex form for computation and compute it via abs i.e.
        abs(var.get_complex_form) <- this form return 0.99999 for 1+1w
        You will get imprecise result.
        Current, more complex form gives precise 1 as answer for 1,1w

        :param var: number
        :return: distance between 0,0 and var
        """
        return (
            (self.co_real - (self.co_omega / 2)) ** 2 + 3 * (self.co_omega ** 2) / 4
        ) ** 0.5

    __rmul__ = __mul__
    __radd__ = __add__

    @property
    def get_complex_form(self) -> complex:
        """
        (a,bw)->(x,iy), where x,y: float, a,b: integer
        :return: Complex number from Eisenstein
        """
        return complex(
            self.co_real - (self.co_omega / 2), (self.co_omega * SQRT_THREE) / 2
        )

    @property
    def get_norm(self):
        """
        wolframalfa
        query: w = ( -1 + i sqrt(3) ) / 2 ; ( a + b w^2 ) ( a + b w )
        answer: a^2 - ab + b^2

        :return: Norm in algebraic sense
        """
        return self.co_real ** 2 - self.co_real * self.co_omega + self.co_omega ** 2

    def __floordiv__(self, other):
        """
        This is Cardinal numbers division operation
        If we wan to divide two Eisenstein numbers
        we need to use // operators.
        When we use / we should get and error.
        """
        if isinstance(other, int):
            other = Eisenstein(other)

        co_real = (
            self.co_real * other.co_real
            + self.co_omega * other.co_omega
            - self.co_real * other.co_omega
        )
        co_omega = self.co_omega * other.co_real - self.co_real * other.co_omega

        # This is other way of getting the same result - check
        assert get_eisenstein_form(
            self.get_complex_form / other.get_complex_form
        ) == Eisenstein(int(co_real / other.get_norm), int(co_omega / other.get_norm))

        return Eisenstein(int(co_real / other.get_norm), int(co_omega / other.get_norm))

    def __truediv__(self, other):
        """
        This operation is not allowed in Eisenstein numbers
        """
        assert False

    def __mod__(self, other):
        K = get_eisenstein_form(self.get_complex_form / other.get_complex_form)
        # This debug code is important - it creates queries for
        # wolframalfa that can be checked if mod function works correctly

        # print(
        #    # self = K * other + R
        #    'w = ( -1 + i sqrt(3) ) / 2 ; %r %r + %r ; expected %r'
        #    % (K, other, self - K * other, self)
        # )

        return self - K * other

    def div_mod(self, other):
        a = self.co_real
        b = self.co_omega
        c = other.co_real
        d = other.co_omega
        bottom = other.get_norm
        e = a * c + b * d - a * d
        f = b * c - a * d
        g, h = divmod(e, bottom)
        i, j = divmod(f, bottom)
        result = (Eisenstein(g, i), Eisenstein(h, j))
        return result

    def math_view(self):
        return "(%s, %sw)" % (self.co_real, self.co_omega)


def get_dot_product(x: Eisenstein, y: Eisenstein):
    """
    Dot product
    https://www.quora.com/What-is-dot-product-of-two-complex-numbers
    google: "if dot product is zero" -> angle 90 degrees

    :return: dot product of two complex numbers
    """
    a = x.co_real
    b = x.co_omega
    c = y.co_real
    d = y.co_omega
    result = a * c + b * d - (b * c + a * d) / 2
    return result


def get_eisenstein_form(var: complex):
    """
    (x,iy) -> (a,bw), where x,y: float, a,b: integer
    :return: Eisenstein number from complex
    """
    x = var.real
    y = var.imag
    return Eisenstein(round(x + y / SQRT_THREE), round((2 * y) / SQRT_THREE))


def gcd(x: Eisenstein, y: Eisenstein):
    """Calculate the Greatest Common Divisor of a and b.

    Paper: Efficient algorithms for gcd and cubic residuosity
           in the ring of Eisenstein integers
    http://cs.au.dk/~gudmund/Documents/cubicres.pdf

    Unless b==0, the result will have the same sign as b (so that when
    b is divided by it, the result comes out positive).
    """

    if abs(y) > abs(x):
        x, y = y, x
    while get_dot_product(x, y):
        x, y = y, x % y
    return x
