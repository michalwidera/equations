#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from eisenstein import Eisenstein, gcd
from fractions import Fraction


class EisensteinFraction(Eisenstein):
    def __init__(self, object, optional=0):

        if isinstance(object, (int, Fraction)) and isinstance(
            optional, (int, Fraction)
        ):
            self.real = Fraction(object)
            self.imag = Fraction(optional)
        elif isinstance(object, (Eisenstein, EisensteinFraction)) and optional == 0:
            self.real = Fraction(object.real)
            self.imag = Fraction(object.imag)
        else:
            raise TypeError("Argument should be an int, Fraction or Eisenstein")

        assert isinstance(self.real, Fraction)
        assert isinstance(self.imag, Fraction)

    def __eq__(self, other):
        other = upgrade_fraction(other)
        return self.real == other.real and self.imag == other.imag

    def __repr__(self):
        return "(%s +%sw)" % (self.real, self.imag)

    def __add__(self, other):
        other = upgrade_fraction(other)
        return EisensteinFraction(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        other = upgrade_fraction(other)
        return EisensteinFraction(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        other = upgrade_fraction(other)
        return EisensteinFraction(
            (self.real * other.real) - (self.imag * other.imag),
            (self.imag * other.real)
            + (self.real * other.imag)
            - (self.imag * other.imag),
        )

    def __truediv__(self, other):
        other = upgrade_fraction(other)
        return self * inverse(other)

    __rmul__ = __mul__
    __radd__ = __add__


def inverse(val: EisensteinFraction) -> EisensteinFraction:
    """
    :param e: val
    :return: 1/val
    """

    return EisensteinFraction(
        (val.real - val.imag) / val.get_norm, (-val.imag) / val.get_norm
    )


def upgrade_fraction(other):
    """
    This function will upgrade argument to EisensteinFraction

    :param other: int,Eisenstien, EisensteinFraction
    :return:  same value but EisensteinFraction type
    """
    if isinstance(other, (int, Fraction)):
        other = EisensteinFraction(other, 0)
    elif isinstance(other, Eisenstein):
        other = EisensteinFraction(other)
    return other
