# coding: utf-8

import unittest
import doctest
import PACKAGE

# load doctests
def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(PACKAGE))
    return tests

class Test_1(unittest.TestCase):
    def setUp(self):
        pass

    def test_1(self):
        self.assertEqual(PACKAGE.FUNCTION(), RESULT, MESSAGE)
