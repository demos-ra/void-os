import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestFile(unittest.TestCase):

    def test_file_1(self):
        """The whole input MUST be given as the sheets of one MTSV file."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('file.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_file_2(self):
        """A file MUST hold every sheet its schema gives that holds a record, in its place in the order of the schema's tree."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('file.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_file_3(self):
        """A file MUST NOT hold a sheet that holds no record."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('file.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
