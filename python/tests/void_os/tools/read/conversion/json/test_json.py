import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestJson(unittest.TestCase):

    def test_json_1(self):
        """json MUST read a JSON file, through JSON text, as sheets: its value an array of objects, each with the members sheet name, header and records, one sheet each."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_json_2(self):
        """A value that is not a string, or a field that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
