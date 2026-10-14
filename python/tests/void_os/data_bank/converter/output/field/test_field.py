import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestField(unittest.TestCase):

    def test_field_1(self):
        """Each field MUST hold its instance's text as JSON text gives its _value, null as an empty field."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('field.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_field_2(self):
        """In the sheet of instances, the fields after a record's keys MUST be _type, its instance's primitive type, and _value, its instance's text, as JSON text gives them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('field.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_field_3(self):
        """A string value that holds FF, a line break or HT MUST be written as an empty field, its text written as runs of text to the sheet of runs."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('field.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
