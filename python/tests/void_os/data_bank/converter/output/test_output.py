import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestOutput(unittest.TestCase):

    def test_output_1(self):
        """The output MUST write the relations as one MTSV file, at its levels file, sheet, record and field."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('output.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_output_2(self):
        """output MUST give the access program sheets of sheet as its own."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('output.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_output_3(self):
        """The file MUST be written by the generator."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('output.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
