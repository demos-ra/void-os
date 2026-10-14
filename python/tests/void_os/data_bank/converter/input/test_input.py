import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestInput(unittest.TestCase):

    def test_converter_input_1(self):
        """The converter's input MUST be read in full, the module specification first and then each input value, before any value is transferred."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('converter-input.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_converter_input_2(self):
        """The input MUST give the schema's instances and runs, the input values' _instances and _runs, each value's instances keyed by its position in the whole input, and annotations, as schema validates each input value."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('converter-input.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
