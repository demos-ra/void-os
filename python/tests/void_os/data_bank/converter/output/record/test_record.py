import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestRecord(unittest.TestCase):

    def test_record_1(self):
        """Each instance, and each run of text, that a relation holds MUST be one record of its sheet."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('record.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
