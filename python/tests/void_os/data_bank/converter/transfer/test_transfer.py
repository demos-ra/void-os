import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestTransfer(unittest.TestCase):

    def test_transfer_1(self):
        """The transfer MUST take the input's tree to relations in normal form, each subordinate relation taking its parent's primary key as a foreign key; where a kind is referred to from several places or holds itself, a foreign key refers to the kind's one relation."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('transfer.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_transfer_2(self):
        """A schema's subschemas MUST be taken from its keywords in the order items, additionalItems, properties, patternProperties, additionalProperties, dependencies, if, then, else, allOf, anyOf and oneOf, and within a keyword in the order the schema writes them: the order of the subschemas."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('transfer.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
