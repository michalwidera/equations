#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from eisenstein import Eisenstein, gcd
from fractions import Fraction


def upgrade_fraction(other):
    """
    This function will upgrade argument to EisensteinFraction

    :param other: int,Eisenstien, EisensteinFraction
    :return:  same value but EisensteinFraction type
    """
    if isinstance(other, (int, Eisenstein)):
        other = EisensteinFraction(other, 1)
    return other


class EisensteinFraction:
    def __init__(self, numerator, denominator=1):

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

    @property
    def get_fraction_form_real(self) -> Fraction:
        # ( a + bw ) / ( c + dw )
        a = self.n.real
        b = self.n.imag
        c = self.d.real
        d = self.d.imag
        return Fraction(a * c - a * d + d * b) / self.d.get_norm

    @property
    def get_fraction_form_imag(self) -> Fraction:
        # ( a + bw ) / ( c + dw )
        a = self.n.real
        b = self.n.imag
        c = self.d.real
        d = self.d.imag
        return Fraction(b * c - a * d) / self.d.get_norm

    def __eq__(self, other):
        other = upgrade_fraction(other)
        return self.n == other.n and self.d == other.d

    def __repr__(self):
        return "(%s/%s)" % (self.n, self.d)

    def __add__(self, other):
        other = upgrade_fraction(other)
        return EisensteinFraction(self.n * other.d + other.n * self.d, self.d * other.d)

    def __sub__(self, other):
        other = upgrade_fraction(other)
        return EisensteinFraction(self.n * other.d - other.n * self.d, self.d * other.d)

    def __mul__(self, other):
        other = upgrade_fraction(other)
        return EisensteinFraction(self.n * other.n, self.d * other.d)

    def __truediv__(self, other):
        other = upgrade_fraction(other)
        return self * inverse(other)

    __rmul__ = __mul__
    __radd__ = __add__


def floor(var: EisensteinFraction) -> Eisenstein:
    # TODO need figure out how to implement Floor function
    return int(1)


def inverse(val: EisensteinFraction) -> EisensteinFraction:
    """

    query: w = ( -1 + i sqrt(3) ) / 2 ; w^2
    answer: w^2 = - 1/2 i ( sqrt(3) + (-i) )

    w ^ 2 = ( 1 - w )

    :param e: val
    :return: 1/val
    """

    a = val.n.real
    b = val.n.imag
    c = val.d.real
    d = val.d.imag

    return EisensteinFraction(Eisenstein(a - b, -b) * Eisenstein(c, d), val.n.get_norm)
