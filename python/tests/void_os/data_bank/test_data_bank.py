import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestDataBank(unittest.TestCase):

    def test_data_bank_1(self):
        """The data bank MUST store the files the converter writes for each of its inputs, and communicate them to another system."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('data-bank.1', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])

    def test_data_bank_3(self):
        """The data bank MUST give the access programs of storage and communication as its own: folder, insert and stored of storage, and names, records and new of communication."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('data-bank.3', 1, os.path.dirname(__file__) + '/../../../../conformance', _relational_model, _values), [])
