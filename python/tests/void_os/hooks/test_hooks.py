import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestHooks(unittest.TestCase):

    def test_hooks_1(self):
        """Each hook event MUST be run by a harness's command hook as the void-os command with the event, as that harness names it, as its operand: a session's start, a subagent's start, a prompt submitted, a tool call succeeded, a subagent's finish, and the model's finish."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.1', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_hooks_2(self):
        """The input's name MUST be the resolved pathname of the place the harness reports: the environment variable harness variables names for place, where it is set; else the first member harness members names for place, in that relation's order, that the hook input holds; else the working directory the hook is handed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.2', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_hooks_3(self):
        """The context MUST be composed before the hook input is inserted, so that a hook never gives back its own input."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.3', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_hooks_5(self):
        """A hook input that JSON text rejects, or that the converter rejects, MUST end the hook as non-conforming, nothing being written on standard output."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.5', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_hooks_6(self):
        """A data bank that cannot keep or give what it stores MUST end the hook as keeping failed, nothing being written on standard output."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.6', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_hooks_7(self):
        """The hook input MUST be read whole from standard input as one JSON text, before the context is composed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.7', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_hooks_8(self):
        """The answer hook output's context gives MUST be written on standard output in UTF-8, and nothing where it gives nothing."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('hooks.8', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])
