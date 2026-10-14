import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestHookOutput(unittest.TestCase):

    def test_hook_output_1(self):
        """On an event context members gives, the context MUST be, where the event begins the context, the data bank's names, then what is new of the input to the session and agent the hook input names, each by the first member harness members names for it, in that relation's order, that the hook input holds, less the values whose hook input names the same session and agent, each value then its records of _stored, as many whole values as the Value context limit holds."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-output.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_hook_output_4(self):
        """What is new beyond the Value context limit MUST be cut to the last whole values it holds, every value still being marked communicated and remaining readable through the data bank."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-output.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_hook_output_5(self):
        """On every other event, the context MUST be empty."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-output.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_hook_output_6(self):
        """The context MUST be MTSV text written by the generator."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-output.6', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_hook_output_7(self):
        """An event answer members or context members gives MUST be answered as one JSON object holding, at each pointer answer members gives that event, its value, and at the pointer context members gives it, the context."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-output.7', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_hook_output_8(self):
        """An event neither answer members nor context members gives MUST be answered by nothing."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hook-output.8', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
