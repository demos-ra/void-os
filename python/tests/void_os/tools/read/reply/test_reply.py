import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestReply(unittest.TestCase):

    def test_reply_1(self):
        """The report MUST be the sheets file, not read, left behind and sheets, in that order, each with its header even when it holds no record."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('reply.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_reply_2(self):
        """The map MUST be the sheet fields: the name of each field of each sheet chosen."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('reply.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_reply_3(self):
        """The reply MUST be written by the generator."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('reply.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_reply_5(self):
        """Every reply MUST be the report, then, with a pathname alone, the map, and with a selection, the values chosen."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('reply.5', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
