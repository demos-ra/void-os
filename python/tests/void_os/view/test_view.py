import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestView(unittest.TestCase):

    def test_view_1(self):
        """The view MUST give, with no operand, the overview of every input the data bank holds, handing overview the data bank's _inputs and one relation days holding each input's days as zoom gives them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.1', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_view_2(self):
        """The view MUST give, with an input's name as its one operand, that input's days, and with a day as its second operand, the turns of that day."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.2', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_view_3(self):
        """The view MUST give, with a position as its third operand, the details of that value, a position being that of a value stored on the day given."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.3', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_view_5(self):
        """The view MUST read the data bank only through its names, records and stored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.5', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_view_6(self):
        """An input, day or position that does not exist MUST be refused with the reason no input, no day or no position, a space, and the operand."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.6', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_view_8(self):
        """The view MUST keep each level by filter's kept where --filter is given, lay it out by terminal's lay out, handing it whether standard output is a terminal as the view is handed it, and give it by terminal's page where standard output is a terminal and by terminal's write where it is not, and handing zoom the offset from UTC the view is handed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.8', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_view_9(self):
        """More than three operands MUST be refused as too many operands."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('view.9', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])
