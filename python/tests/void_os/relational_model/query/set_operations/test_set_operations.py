import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestSetOperations(unittest.TestCase):

    def test_set_operations_1(self):
        """The union MUST give each sheet name once, its records those of every sheet of that name in the files or inputs read, in their order, each record led by the file or the _input it came from."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('set-operations.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_set_operations_2(self):
        """Sheets of one name whose headers differ MUST be given apart by the union."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('set-operations.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
