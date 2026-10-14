import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestOverview(unittest.TestCase):

    def test_overview_1(self):
        """The overview MUST hold one record for each input of _inputs, in its order, its values as _inputs gives them, and its first, last and activity from that input's days."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('overview.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_overview_2(self):
        """activity MUST hold one character for each day from first to last: for a day of n values, the block of the eight lower blocks from U+2581 to U+2588 whose rank is 8n divided by m, rounded up, m the most values of any day; and a space for a day with none."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('overview.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
