#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from eisenstein import Eisenstein, gcd
from fractions import Fraction
from math import floor, ceil


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


def eisensteinFloor(var: EisensteinFraction) -> Eisenstein:
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
    assert isinstance(var, EisensteinFraction)
    return Eisenstein(int(floor(var.real)), int(floor(var.imag)))


def eisensteinCeil(var: EisensteinFraction) -> Eisenstein:
    """
    See clarification in floor comment.

    :param var: Eisenstein Fraction
    :return: Floor in Eisenstein Sense
    """
    assert isinstance(var, EisensteinFraction)
    return Eisenstein(int(ceil(var.real)), int(ceil(var.imag)))


def eisensteinRound(var: EisensteinFraction) -> Eisenstein:
    """
    See clarification in floor comment.

    :param var: Eisenstein Fraction
    :return: Floor in Eisenstein Sense
    """
    assert isinstance(var, EisensteinFraction)
    return Eisenstein(int(round(var.real)), int(round(var.imag)))


def eisensteinAbs(var: EisensteinFraction) -> Eisenstein:
    """
    Absolute Value of a Complex Number.
    The absolute value of a complex number , a+bi (also called the modulus )
    is defined as the distance between the origin (0,0) and the point (a,b)
    in the complex plane.

    If you use complex form for computation and compute it via abs i.e.
    abs(var.get_complex_form) <- this form return 0.99999 for 1+1w
    You will get inprecise result.
    Current, more complex form gives precise 1 as answer for 1,1w

    :param var: number
    :return: distance between 0,0 and var
    """
    assert isinstance(var, EisensteinFraction)
    return (var.real ** 2 - var.real * var.imag + ((var.imag) / 4) + (3 / 4)) ** 0.5
