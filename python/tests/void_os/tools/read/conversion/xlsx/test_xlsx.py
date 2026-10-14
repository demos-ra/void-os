import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestXlsx(unittest.TestCase):

    def test_xlsx_1(self):
        """xlsx MUST read each worksheet of a workbook as one sheet, named as the worksheet, each cell's value as its text, and leave behind every type, formula and style a cell holds, each named by the cell's reference, a space, and its name in the cell: t, f or s."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('xlsx.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_xlsx_2(self):
        """A cell's text that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('xlsx.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_xlsx_3(self):
        """A workbook whose part a relationship it reads names is not among its nodes MUST end the load as failed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('xlsx.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
