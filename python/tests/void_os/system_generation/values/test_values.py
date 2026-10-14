import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestValues(unittest.TestCase):

    def test_values_1(self):
        """The access program values MUST read the Values from values.mtsv in the folder it is handed, the Values sheet of this specification as each package carries it, by the header Value and Given, giving relation Values of the domains Value and Given."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('values.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_values_2(self):
        """values.mtsv MUST be written from the Values sheet of this specification, its Value and Given columns, as the generator writes a sheet."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('values.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_values_3(self):
        """A values.mtsv that cannot be read, or that the parser rejects, MUST end values as not MTSV."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('values.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
