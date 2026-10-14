import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestTools(unittest.TestCase):

    def test_tools_1(self):
        """The tools MUST give the access program serve of the server as their own."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('tools.1', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])
