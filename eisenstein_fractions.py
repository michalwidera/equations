#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys

if sys.version_info[0] < 3:
    print("You need Python 3 to run this script.")
    sys.exit(1)

from eisenstein import Eisenstein
from fractions import Fraction
from math import floor, ceil


class EisensteinFraction(Eisenstein):
    def __init__(self, obj=None, optional=0, four=None):

        if four is not None:
            (real_num, real_den, omega_num, omega_den) = four
            assert real_den != 0
            assert omega_den != 0
            self.co_real = Fraction(real_num, real_den)
            self.co_omega = Fraction(omega_num, omega_den)
        elif isinstance(obj, (int, Fraction)) and isinstance(optional, (int, Fraction)):
            self.co_real = Fraction(obj)
            self.co_omega = Fraction(optional)
        elif isinstance(obj, (Eisenstein, EisensteinFraction)) and optional == 0:
            self.co_real = Fraction(obj.co_real)
            self.co_omega = Fraction(obj.co_omega)
        else:
            raise TypeError("Arguments should be an ints, Fractions or one Eisenstein")

        assert isinstance(self.co_real, Fraction)
        assert isinstance(self.co_omega, Fraction)

    def __add__(self, other):
        if isinstance(other, (int, Fraction)):
            other = EisensteinFraction(other)

        return EisensteinFraction(
            self.co_real + other.co_real, self.co_omega + other.co_omega
        )

    def __sub__(self, other):
        if isinstance(other, (int, Fraction)):
            other = EisensteinFraction(other)

        return EisensteinFraction(
            self.co_real - other.co_real, self.co_omega - other.co_omega
        )

    def __mul__(self, other):
        if isinstance(other, (int, Fraction)):
            other = EisensteinFraction(other)

        return EisensteinFraction(
            (self.co_real * other.co_real) - (self.co_omega * other.co_omega),
            (self.co_omega * other.co_real)
            + (self.co_real * other.co_omega)
            - (self.co_omega * other.co_omega),
        )

    def __truediv__(self, other):
        if isinstance(other, (int, Fraction, Eisenstein)):
            other = EisensteinFraction(other)

        return self * EisensteinFraction(
            (other.co_real - other.co_omega) / other.get_norm,
            (-other.co_omega) / other.get_norm,
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
        return Eisenstein(int(floor(self.co_real)), int(floor(self.co_omega)))

    @property
    def ceil(self) -> Eisenstein:
        """
        See clarification in floor comment.

        :param var: Eisenstein Fraction
        :return: Floor in Eisenstein Sense
        """
        return Eisenstein(int(ceil(self.co_real)), int(ceil(self.co_omega)))

    @property
    def round(self) -> Eisenstein:
        """
        See clarification in floor comment.

        :param var: Eisenstein Fraction
        :return: Floor in Eisenstein Sense
        """
        return Eisenstein(int(round(self.co_real)), int(round(self.co_omega)))
