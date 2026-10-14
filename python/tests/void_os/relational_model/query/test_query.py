import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestQuery(unittest.TestCase):

    def test_query_1(self):
        """query MUST give the access program kept of filter expression as its own."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('query.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_query_2(self):
        """Selection MUST give restriction by records and filter, projection by fields, join by join, and union by the sheets of one name from several origins."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('query.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_query_3(self):
        """chosen MUST take the file each sheet is of from origins, so that sheet and join count and name the sheets of each file, and lead each record of a union by lead, file its file's position and _input its file's source."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('query.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_query_4(self):
        """sheets MUST give each sheet chosen of each file: its records, the records of it the filter keeps, and the positions of those named in the sheet it is given in."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('query.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_query_5(self):
        """A selection, filter or join refused MUST end chosen and kept as refused, with its reason."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('query.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
