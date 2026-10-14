import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestCsv(unittest.TestCase):

    def test_csv_1(self):
        """csv MUST read a CSV file, its octets UTF-8, as one sheet whose sheet name is empty, its first record the header."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('csv.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_csv_2(self):
        """A field that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('csv.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
