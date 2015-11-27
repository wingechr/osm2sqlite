# coding: utf-8

import unittest
import doctest
import osm2sqlite.osm


# load doctests
def load_tests(loader, tests, ignore):
    _ = loader, ignore
    tests.addTests(doctest.DocTestSuite(osm2sqlite.osm))
    return tests


class Test1(unittest.TestCase):
    def setUp(self):
        pass

    def test_clean_str(self):
        self.assertEqual(osm2sqlite.osm.default_clean_str(""",\n\r;"'"""), ':  :', 'striong clean failed')
