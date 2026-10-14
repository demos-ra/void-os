import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestZoom(unittest.TestCase):

    def test_zoom_1(self):
        """days MUST hold, for each day an input has values and each event of that day, the number of values stored, the days in order."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('zoom.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_zoom_2(self):
        """turns MUST hold one record for each value stored on the day, in the order stored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('zoom.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_zoom_3(self):
        """A day MUST be the full date of a value's _time at the offset from UTC days and turns are handed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('zoom.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_zoom_4(self):
        """first line MUST be the text, up to its first line break, of the first instance of the value whose type is string and whose text is not empty, in the order the instances are written."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('zoom.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_zoom_5(self):
        """agent, session, turn and model MUST each hold the text of the value's member that harness members names for that column, the first the value holds in that relation's order, and be empty where the value holds none."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('zoom.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
