import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestPositions(unittest.TestCase):

    def test_positions_1(self):
        """sheet, records and fields MUST each be written as 2, 1;3, 1-3 or 2-*, counting from 1 within what holds it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('positions.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_positions_2(self):
        """Positions that do not exist MUST be left out."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('positions.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_positions_3(self):
        """positions MUST write each run of consecutive positions, a run of one as its position and a longer run as its first and last joined by -, the runs joined by ;, and no position as the empty text."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('positions.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_positions_4(self):
        """A selection not written as positions.1 writes it MUST be refused."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('positions.4', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
