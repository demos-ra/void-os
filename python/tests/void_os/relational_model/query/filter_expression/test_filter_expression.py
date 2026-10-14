import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestFilterExpression(unittest.TestCase):

    def test_filter_expression_1(self):
        """filter MUST be a filter expression in which @[0] is a record's first field, and keep the records for which it holds."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('filter-expression.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_filter_expression_2(self):
        """A filter not written as filter-expression.1 writes it MUST be refused."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('filter-expression.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
