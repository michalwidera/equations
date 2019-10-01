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
            raise TypeError("Arguments should be an ints, Fractions or one Eisenstein")

        assert isinstance(self.real, Fraction)
        assert isinstance(self.imag, Fraction)

    def __add__(self, other):
        other = self.__upgrade_number(other)
        return EisensteinFraction(self.real + other.real, self.imag + other.imag)

    def __sub__(self, other):
        other = self.__upgrade_number(other)
        return EisensteinFraction(self.real - other.real, self.imag - other.imag)

    def __mul__(self, other):
        other = self.__upgrade_number(other)
        return EisensteinFraction(
            (self.real * other.real) - (self.imag * other.imag),
            (self.imag * other.real)
            + (self.real * other.imag)
            - (self.imag * other.imag),
        )

    def __truediv__(self, other):
        other = self.__upgrade_number(other)
        return self * EisensteinFraction(
            (other.real - other.imag) / other.get_norm, (-other.imag) / other.get_norm
        )

    __rmul__ = __mul__
    __radd__ = __add__

    def __upgrade_number(self, other):
        """
        This function will upgrade argument to EisensteinFraction

        :param other: int, Fraction Eisenstien, EisensteinFraction
        :return:  same value but EisensteinFraction type
        """
        if isinstance(other, (int, Fraction)):
            other = EisensteinFraction(other, 0)
        elif isinstance(other, Eisenstein):
            other = EisensteinFraction(other)

        assert isinstance(self.real, Fraction)
        assert isinstance(self.imag, Fraction)

        return other
