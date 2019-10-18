#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need to run this with Python 3")
    sys.exit(1)

from eisenstein import Eisenstein, gcd
from fractions import Fraction
from math import floor, ceil


class EisensteinFraction(Eisenstein):
    def __init__(self, obj, optional=0):

        if isinstance(obj, (int, Fraction)) and isinstance(optional, (int, Fraction)):
            self.real = Fraction(obj)
            self.imag = Fraction(optional)
        elif isinstance(obj, (Eisenstein, EisensteinFraction)) and optional == 0:
            self.real = Fraction(obj.real)
            self.imag = Fraction(obj.imag)
        else:
            raise TypeError("Arguments should be an ints, Fractions or one Eisenstein")

        assert isinstance(self.real, Fraction)
        assert isinstance(self.imag, Fraction)

    def __add__(self, other):
        return EisensteinFraction(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        return EisensteinFraction(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        return EisensteinFraction(
            (self.real * other.real) - (self.imag * other.imag),
            (self.imag * other.real)
            + (self.real * other.imag)
            - (self.imag * other.imag),
        )

    def __truediv__(self, other):
        return self * EisensteinFraction(
            (other.real - other.imag) / other.get_norm, (-other.imag) / other.get_norm
        )

    __rmul__ = __mul__
    __radd__ = __add__

    @property
    def floor(self) -> Eisenstein:
        """
        Floor is not defined well
        google: floor complex number
        answer1: https://math.stackexchange.com/questions/2095674/floor-function-in-complex-plane
        answer2: https://math.stackexchange.com/questions/1764832/what-is-lfloor-i-rfloor
        Little unceranity, mess, etc.

        This is another example. First, we define Numbers then Fractions, then Floor and rest of stuff
        :param var: Eisenstein Fraction
        :return: Floor in Eisenstein Sense
        """
        return Eisenstein(int(floor(self.real)), int(floor(self.imag)))

    @property
    def ceil(self) -> Eisenstein:
        """
        See clarification in floor comment.

        :param var: Eisenstein Fraction
        :return: Floor in Eisenstein Sense
        """
        return Eisenstein(int(ceil(self.real)), int(ceil(self.imag)))

    @property
    def round(self) -> Eisenstein:
        """
        See clarification in floor comment.

        :param var: Eisenstein Fraction
        :return: Floor in Eisenstein Sense
        """
        return Eisenstein(int(round(self.real)), int(round(self.imag)))
