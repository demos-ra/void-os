import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestSystemGeneration(unittest.TestCase):

    def test_system_generation_1(self):
        """The access program values MUST give the Values as values reads them, handing it the folder of values' own file, as module folder gives it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('system-generation.1', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])
