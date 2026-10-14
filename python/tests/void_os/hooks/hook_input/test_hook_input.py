import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestHookInput(unittest.TestCase):

    def test_hook_input_2(self):
        """The hook input MUST be inserted into the data bank as one value of the input, its module specification the Value hook input schema, on the event the command is run with."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-input.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
