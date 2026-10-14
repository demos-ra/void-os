import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestDetails(unittest.TestCase):

    def test_details_1(self):
        """details MUST give every record of the value in every sheet it gives, then its record of _stored, each sheet in its place in the order."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('details.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
