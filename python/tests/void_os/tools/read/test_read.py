import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestRead(unittest.TestCase):

    def test_read_10(self):
        """A file named directly whose conversion ends as no format or failed MUST end the read as refused, its reason that error's name, then, for failed, a colon, a space and that error's reason."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.10', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_read_2(self):
        """A pathname at or within the folder the data bank's access program folder gives MUST be answered by the data bank: the folder by its names, an input's file, the _file of its record of _inputs, by its records, then their records of _stored, and any other pathname within it refused, never by reading its files."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_read_4(self):
        """The data bank's folder read with a selection or a filter MUST be answered by the records of every input, a sheet of one name in several inputs given as the union of their records, each record led by its _input."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_read_6(self):
        """A pathname, a file, a selection or a filter refused MUST end the read as refused, with its reason."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.6', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_read_7(self):
        """Every other pathname MUST be read as the files read › input's members names, each by conversion's sheets, the sheets of every file chosen by the relational model's chosen, and the reply given by reply."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.7', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_read_8(self):
        """A file of a directory whose conversion ends as no format or failed MUST be named in not read, its status that error's name and its reason that error's reason, and the read go on."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.8', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_read_9(self):
        """What a file's conversion leaves behind MUST be named in left behind, one record for each thing, in order."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('read.9', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
