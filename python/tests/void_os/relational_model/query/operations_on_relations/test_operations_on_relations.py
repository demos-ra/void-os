import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestOperationsOnRelations(unittest.TestCase):

    def test_operations_on_relations_1(self):
        """Restriction MUST keep the records whose positions records names and for which filter holds."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('operations-on-relations.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_operations_on_relations_2(self):
        """A sheet left with no field MUST come back empty."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('operations-on-relations.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_operations_on_relations_3(self):
        """Projection MUST keep the fields whose positions fields names."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('operations-on-relations.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_operations_on_relations_4(self):
        """With a filter, records MUST count the records the filter keeps."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('operations-on-relations.4', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_operations_on_relations_5(self):
        """join MUST name sheets of each file as sheet does, and give their natural join on every column whose name they share, before records, filter and fields are applied, the sheet it gives named by the names of the sheets joined, in order, joined by *, as a natural join is written."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('operations-on-relations.5', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_operations_on_relations_6(self):
        """A join of sheets that share no column MUST be refused."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('operations-on-relations.6', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
