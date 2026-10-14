import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestConversion(unittest.TestCase):

    def test_conversion_1(self):
        """A file whose name ends .mtsv MUST be read by the parser."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('conversion.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_conversion_2(self):
        """A file whose extension names a format MUST be read by that format's module: .csv by csv, .json by json, .xlsx by xlsx and .ods by ods, each from the nodes package reads, and .sqlite by sqlite."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('conversion.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_conversion_3(self):
        """What a file holds that MTSV does not MUST be left behind, each thing named as its format's module names it, in order."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('conversion.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_conversion_4(self):
        """A file whose extension names no format MUST end its conversion as no format; one that cannot be read, as failed, its reason cannot be read; and one whose conversion ends with an error, as failed, its reason that error's name."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('conversion.4', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
