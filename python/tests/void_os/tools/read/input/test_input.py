import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestInput(unittest.TestCase):

    def test_read_input_1(self):
        """The pathname MUST be absolute."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read-input.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_read_input_2(self):
        """A pathname naming a directory MUST name each regular file in it whose name does not begin with a dot, in the order of their names' code points, the directories within it not read, and each other entry named in not read as skipped."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read-input.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_read_input_3(self):
        """A pathname that names neither a directory nor a regular file, a directory that cannot be listed, and a file named directly that cannot be read MUST be refused with the reason: names neither a directory nor a regular file, cannot be listed, or cannot be read."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read-input.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_read_input_4(self):
        """The same file reached by two pathnames MUST be one file, named by its resolved pathname."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read-input.4', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_read_input_5(self):
        """A pathname that is not absolute MUST be refused as not absolute."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read-input.5', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
