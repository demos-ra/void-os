import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestCommunication(unittest.TestCase):

    def test_communication_1(self):
        """Communication MUST give what the data bank stores as MTSV, by restriction, and by aggregate only to count an input's values."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('communication.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_communication_2(self):
        """The access program names MUST give three sheets, each record beginning with its primary key: _inputs as storage's inputs gives it; and _sheets and _fields as storage keeps them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('communication.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_communication_3(self):
        """The access program records MUST give the records of the values whose positions lie between first and last, both included, each counted from 0, of the places asked for, or else every place, each place's sheet named as _sheets names it, in the order of the schema's tree, the records kept by the relational model's kept: those whose first field, _input value, equals one of the positions from first to last, each written as its number is."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('communication.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_communication_4(self):
        """The access program new MUST give the records, as records gives them, of the values from the number communicated to the session and agent asked for to the last value stored, then their records of _stored, then mark every value stored communicated to them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('communication.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_communication_5(self):
        """Communication MUST NOT transform or sort what the data bank stores: values as stored, records in stored order."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('communication.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
