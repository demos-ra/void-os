import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestValue(unittest.TestCase):

    def test_value_1(self):
        """The input values, each a JSON text in UTF-8, MUST be read in the order the module supplies them, the order its source holds them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('value.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_value_2(self):
        """Each value MUST be given its zero-based position in the whole input; an input converted in parts, in order, keeps its positions, so that the sheets each part gives, appended sheet by sheet in the file's order, are the whole input's file."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('value.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_value_3(self):
        """Every input value MUST be accepted, of any size, any depth of nesting and any length of string."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('value.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_value_4(self):
        """An input value JSON text rejects, as not a JSON text or as names not unique, MUST be rejected as non-conforming, its reason its zero-based position in the input, a space, and the JSON Pointer to the place within it, in its URI fragment representation: the first object, in the order written, that repeats a name, or else the value itself."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('value.4', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_value_5(self):
        """What JSON text leaves out MUST be left out of the file, and each place left out reported as not carried by the JSON Pointer to it within the input, whose first reference token is the zero-based position of its input value, as a JSON string."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('value.5', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
