import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestFormat(unittest.TestCase):

    def test_format_1(self):
        """format MUST give the access programs of the parser, the generator and JSON text as its own: loads and load, dumps and dump, instances and named."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('format.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
