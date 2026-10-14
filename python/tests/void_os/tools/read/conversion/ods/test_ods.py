import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestOds(unittest.TestCase):

    def test_ods_1(self):
        """ods MUST read each table of a spreadsheet document as one sheet, named as the table, each cell's text as its value, and leave behind every type, formula and style a cell holds, each named by the cell's reference in A1 style, a space, and its attribute's name: office:value-type and the value attribute it selects, table:formula or table:style-name."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('ods.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_ods_2(self):
        """A cell's text that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('ods.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_ods_3(self):
        """A spreadsheet document whose nodes hold no part content.xml, or whose body holds no office:spreadsheet, MUST end the load as failed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('ods.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
