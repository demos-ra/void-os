import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestRelationalModel(unittest.TestCase):

    def test_relational_model_1(self):
        """The relational model MUST give the access programs of format and query as its own: loads and load, dumps and dump, instances and named, chosen and kept."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relational-model.1', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])
