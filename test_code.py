#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
./test_code.py --fast; red_green_bar.py $? $COLUMNS
red_green_bar.py is taken from https://github.com/kwadrat/rgb_tdd.git
"""

import sys
if sys.version_info[0] < 3:
    print('You need to run this with Python 3')
    sys.exit(1)

import unittest
from pathlib import Path

from number_test import TestEisensteinNumbers
from fraction_test import TestEisensteinFractionNumbers
from series_test import TestEisensteinFractionTimeSeriesOperations
import parameters


def runningInTravis():

    home = str(Path.home())
    fields = home.strip().split("/")
    if "travis" in fields:
        return True

    return False


fast_test_ls = [TestEisensteinNumbers, TestEisensteinFractionNumbers]


slow_test_ls = [TestEisensteinFractionTimeSeriesOperations]


def add_all_fast(suite):
    for one_test in fast_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def add_all_slow(suite):
    for one_test in slow_test_ls:
        suite.addTest(unittest.makeSuite(one_test))


def summary_status(suite):
    text_test_result = unittest.TextTestRunner().run(suite)
    return not not (text_test_result.failures or text_test_result.errors)


def perform_only_fast_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    return summary_status(suite)


def perform_tests():
    suite = unittest.TestSuite()
    add_all_fast(suite)
    add_all_slow(suite)
    return summary_status(suite)


if __name__ == "__main__":
    result = 1  # assuming failure of test script
    if len(sys.argv) >= 2 and sys.argv[1] == "--fast":
        result = perform_only_fast_tests()
    elif len(sys.argv) >= 3 and sys.argv[1] == "--setscale":
        TestRange = int(sys.argv[2])
        parameters.cfg_prm.set_range(TestRange)
        result = perform_tests()
    elif runningInTravis():
        print("Wow! We are under Travis CI!")
        TestRange = 10
        parameters.cfg_prm.set_range(TestRange)
        result = perform_tests()
    else:
        result = perform_tests()  # go ahead with defaults
    sys.exit(result)
