import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestSqlite(unittest.TestCase):

    def test_sqlite_1(self):
        """sqlite MUST read each table of a database as one sheet, named as the table, its column names the header, each value the text CAST AS TEXT gives it and a NULL an empty field, and leave behind views, indexes, triggers and the objects whose names begin with sqlite_, each named by its type, a space, and its name, as sqlite_schema holds them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sqlite.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_sqlite_2(self):
        """A value whose typeof is blob, or a field that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sqlite.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_sqlite_3(self):
        """A file that does not begin with the database header's magic string MUST end the load as failed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sqlite.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
