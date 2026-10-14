import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestFilter(unittest.TestCase):

    def test_filter_1(self):
        """The option --filter MUST keep, at every level, the records for which the filter holds, as query decides."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('filter.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
