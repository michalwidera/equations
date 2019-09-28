#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Rational Fractions Type Implementation - Python 3.x
   Copyright (c) 2019 Michal Widera

   Defined operations on Eisenstein integers:
   https://en.wikipedia.org/wiki/Eisenstein_integer
"""

import math

# https://docs.python.org/3.7/reference/datamodel.html


class Eisenstein:
    def __init__(self, a=0, b=0):

        if isinstance(a, int) and isinstance(b, int):
            self.a = a
            self.b = b
        else:
            raise TypeError("arguments should be an int")

    @staticmethod
    def __upgrade_int(other):
        if isinstance(other, int):
            other = Eisenstein(other, 0)
        return other

    def __repr__(self):
        return "(%s, %sw)" % (self.a, self.b)

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b

    def __add__(self, other):
        other = self.__upgrade_int(other)
        return Eisenstein(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        other = self.__upgrade_int(other)
        return Eisenstein(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        # (a+bw)(c+dw)=(ac-bd)+(bc+ad-db)w
        # https://en.wikipedia.org/wiki/Eisenstein_integer
        other = self.__upgrade_int(other)
        return Eisenstein(
            (self.a * other.a) - (self.b * other.b),
            (self.b * other.a) + (self.a * other.b) - (self.b * other.b),
        )

    def __abs__(self):
        # |a+bw|^2 = a*a - a*b + b*b
        # https://en.wikipedia.org/wiki/Eisenstein_integer
        return math.sqrt((self.a * self.a) - (self.a * self.b) + (self.b * self.b))

    __rmul__ = __mul__
    __radd__ = __add__

    @property
    def get_complex_form(self):
        """
        (a,bw)->(x,iy), where x,y: float, a,b: integer
        :return: Complex number from Eisenstein
        """
        return complex(self.a - (self.b / 2), (self.b * math.sqrt(3)) / 2)

    @property
    def get_norm(self):
        """
        wolframalfa
        query: w = ( -1 + i sqrt(3) ) / 2 ; ( a + b w^2 ) ( a + b w )
        answer: a^2 - ab + b^2

        :return: Norm in algebraic sense
        """
        return self.a * self.a - self.a * self.b + self.b * self.b

    def __floordiv__(self, other):
        other = self.__upgrade_int(other)
        return get_eisenstein_form(self.get_complex_form / other.get_complex_form)

    def __mod__(self, other):
        other = self.__upgrade_int(other)

        K = get_eisenstein_form(self.get_complex_form / other.get_complex_form)
        # This debug code is important - it creates queries for
        # wolframalfa that can be checked if mod function works correctly

        # print(
        #    # self = K * other + R
        #    'w = ( -1 + i sqrt(3) ) / 2 ; %r %r + %r ; expected %r'
        #    % (K, other, self - K * other, self)
        # )

        return self - K * other


def get_eisenstein_form(var: complex):
    """
    (x,iy) -> (a,bw), where x,y: float, a,b: integer
    :return: Eisenstein number from complex
    """
    x = var.real
    y = var.imag
    return Eisenstein(round(x + y / math.sqrt(3)), round((2 * y) / math.sqrt(3)))


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
    while y.a:
        # if b == Eisenstein(0, 0):
        #    return a
        # I don't like that while y.a: , what about y.b != 0 ?
        x, y = y, x % y
    return x


class EisensteinFraction:
    def __init__(self, numerator=0, denominator=1):

        if isinstance(numerator, Eisenstein):
            self.n = numerator
        elif isinstance(numerator, int):
            self.n = Eisenstein(numerator, 0)
        else:
            raise TypeError("numerator should be a int or Eisenstein")

        if isinstance(denominator, Eisenstein):
            self.d = denominator
        elif isinstance(denominator, int):
            self.d = Eisenstein(denominator, 0)
        else:
            raise TypeError("denominator should be a int or Eisenstein")

        gcd_val = gcd(self.n, self.d)

        if gcd_val != Eisenstein(0, 0):
            self.n = self.n // gcd_val
            self.d = self.d // gcd_val

    def __eq__(self, other):
        return self.n == other.n and self.d == other.d

    def __repr__(self):
        return "(%s/%s)" % (self.n, self.d)

    def __add__(self, other):
        if isinstance(other, int):
            other = EisensteinFraction(Eisenstein(other, 0), 1)
        return EisensteinFraction(self.n * other.d + other.n * self.d, self.d * other.d)

    def __sub__(self, other):
        if isinstance(other, int):
            other = EisensteinFraction(Eisenstein(other, 0), 1)
        return EisensteinFraction(self.n * other.d - other.n * self.d, self.d * other.d)

    def __mul__(self, other):
        if isinstance(other, int):
            other = EisensteinFraction(Eisenstein(other, 0), 1)

        return EisensteinFraction(self.n * other.n, self.d * other.d)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = EisensteinFraction(Eisenstein(other, 0), 1)
        if isinstance(self, int):
            other = EisensteinFraction(Eisenstein(other, 0), 1)
        if isinstance(self, Eisenstein):
            other = EisensteinFraction(other, 1)
        return self * inverse(other)

    __rmul__ = __mul__
    __radd__ = __add__


def floor(var: EisensteinFraction) -> int:
    # TODO need figure out how to implement Floor function
    return int(1)


def inverse(e: EisensteinFraction) -> EisensteinFraction:
    """

    query: w = ( -1 + i sqrt(3) ) / 2 ; w^2
    answer: w^2 = - 1/2 i ( sqrt(3) + (-i) )

    w ^ 2 = ( 1 - w )

    :param e: val
    :return: 1/val
    """
    a = e.n.a
    b = e.n.b
    return (
        EisensteinFraction(Eisenstein(a - b, -b), e.n.get_norm)
    ) * EisensteinFraction(e.d, 1)

