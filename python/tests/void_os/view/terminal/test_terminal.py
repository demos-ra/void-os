import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestTerminal(unittest.TestCase):

    def test_terminal_1(self):
        """Where lay out is handed that standard output is not a terminal, a level MUST be written as MTSV text, by the generator."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_terminal_2(self):
        """Where lay out is handed that standard output is a terminal, each sheet MUST begin on a page of its own, FF before it, its sheet name on the first line, its header in bold, then its records, each field of the header and of the records padded to the width of its column's widest field, the fields of a line joined by the Value column gap."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_terminal_3(self):
        """A field's width MUST be the sum of its characters' widths, a wide or fullwidth character taking two columns and every other character one."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_terminal_4(self):
        """Bold MUST be set and reset by the select graphic rendition control function, with the parameters 1 and 0."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_terminal_5(self):
        """A control character in a field or sheet name MUST be written as its control picture, so that no field moves the cursor or changes the terminal."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_terminal_6(self):
        """The text MUST be written on standard output in UTF-8."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.6', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_terminal_7(self):
        """The text MUST be piped, in UTF-8, through the command the environment variable the Value pager variable names holds, run as the command string of sh -c, and through more where it is null or not set."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('terminal.7', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
