import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestConverter(unittest.TestCase):

    def test_converter_1(self):
        """The converter MUST read an input of JSON values that a module specification describes, and write the whole input as one MTSV file."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('converter.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_converter_5(self):
        """The access program sheets MUST give _sheets and _fields of the input named: every sheet the schema gives, by its place in the order of the schema's tree, and the name of each field of its header."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('converter.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
