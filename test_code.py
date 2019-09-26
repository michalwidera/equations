#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
./test_code.py test; red_green_bar.py $? $COLUMNS
red_green_bar.py is taken from https://github.com/kwadrat/rgb_tdd.git
"""

import sys
import unittest

from eisenstein import Eisenstein


class TestNumbers(unittest.TestCase):
    def test_equal_values(self):
        """
        TestNumbers:
        """
        a = Eisenstein(1, 2)
        b = Eisenstein(20, 30)
        c = a + b
        self.assertEqual(c, Eisenstein(21, 32))


fast_test_ls = [TestNumbers]


def add_all_fast(suite):
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    return summary_status(suite)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "slowtest":
        result = perform_slow_tests()
    else:
        result = perform_tests()
    sys.exit(result)
