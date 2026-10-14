import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestKey(unittest.TestCase):

    def test_key_1(self):
        """Every record MUST begin with its primary key, its fixed variables first, as void-os.1 requires of every datum."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('key.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_key_2(self):
        """A record of the sheet of the input values MUST have one key column, _input value, the zero-based position of its input value in the input; where that sheet is the sheet of instances or a kind's sheet, its records are keyed as key.3 keys them, the record of an input value leaving _parent and _pointer empty."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('key.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_key_3(self):
        """A record of any other sheet but the sheet of runs MUST begin with _input value; then _instance, the zero-based position of its instance among the instances of its input value, the value itself first, counted in the order written; then _parent, the _instance of the record whose instance holds its own, which with _input value is a foreign key, possibly into its own relation; then _pointer, the JSON Pointer to its instance evaluated from that record's instance. A record whose instance is its location's own, a subschema applying to the same location, has the _input value and _instance of its location's record and leaves _parent and _pointer empty. No key holds the access path from the input value to its instance."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('key.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_key_4(self):
        """A record of the sheet of runs MUST begin with the _input value and _instance of its string, then _page, _line and _position, each a count of the unit FF, LF or HT moves to."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('key.4', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
