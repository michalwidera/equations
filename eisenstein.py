#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Eisenstein Irrational Fractions Type Implementation - Python 3.x
   Copyright (c) 2019 Michal Widera
"""

from decimal import Decimal
import math

# https://docs.python.org/3.7/reference/datamodel.html




class Eisenstein:

    def __init__(self, a=0, b=0):

        if isinstance(a, int) and isinstance(b, int):
            self.a = a
            self.b = b
        else:
            raise TypeError("arguments should be an int")

    def __upgrade_int(other):
        if isinstance(other, int):
            other = Eisenstein(other, 0)
        return other
  
    def __repr__(self):
        return "(%s, %sw)" % (self.a, self.b)

    def __add__(self, other):
        other = __upgrade_int(other)
        return Eisenstein(self.a + other.a, self.b + other.b)

    def __sub__(self, other):
        other = __upgrade_int(other)
        return Eisenstein(self.a - other.a, self.b - other.b)

    def __mul__(self, other):
        # (a+bw)(c+dw)=(ac-bd)+(bc+ad-db)w
        # https://en.wikipedia.org/wiki/Eisenstein_integer
        other = __upgrade_int(other)
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

    # sprawdzic
    # wolfram alpha : w = ( -1 + i sqrt(3) ) / 2 ; z = ( a + b * w ) * ( a + b * ( w ^ 2 ) )-> z = a^2 - ab + b^2
    def __mod__(self, other):
        other = __upgrade_int(other)
        w = (-1 + math.sqrt(3)) / 2
        adivb = complex(self.a, self.b * w) / complex(other.a, other.b * w)
        a = adivb.real
        b = adivb.imag

        K = Eisenstein(round(a + b / math.sqrt(3)), round((b * 2) / math.sqrt(3)))
        print(
            "self = K * other + R : %r = %r * %r + %r"
            % (self, K, other, self - K * other)
        )
        return self - K * other

    def gcd(a, b):
        """Calculate the Greatest Common Divisor of a and b.

        Unless b==0, the result will have the same sign as b (so that when
        b is divided by it, the result comes out positive).
        """
        while b:
            a, b = b, a % b
        return a


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


def test():
    E1 = Eisenstein(2, 1)
    E2 = Eisenstein(22, 4)

    # print(gcd(E1, 2))

    E3 = E1 + E2
    E4 = E2 - E1
    E5 = E1 * E2
    E6 = 2 * E1 * 2

    print(E1, E2, E3, E4, E5, E6)

    print(math.pow(abs(E5), 2))

    EF1 = EisensteinFraction(E1, 1)
    EF2 = EisensteinFraction(E2, 1)

    print("EF2 + EF1", EF1 + EF2)
    print("EF2 / EF1", EF2 / EF1)

    print(EF2 * 3)

    print("modulo E2 % 3", E2, 3, E2 % 3)
    print("modulo 22 % 3", 22, 3, 22 % 3)
    # print("gcd 22,2:", Eisenstein.gcd(E2, E1))

    print("Success.")


def inverse(e: EisensteinFraction):
    a = e.n.a
    b = e.n.b
    return (
        EisensteinFraction(a - b, a * a - a * b + b * b)
        - EisensteinFraction(Eisenstein(0, -b), a * a - a * b + b * b)
    ) * EisensteinFraction(e.d, 1)


if __name__ == "__main__":
    test()
