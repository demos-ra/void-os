import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestOrder(unittest.TestCase):

    def test_order_1(self):
        """Sheets MUST be written in the order of the schema's tree: the sheet of the input values first, each sheet directly followed by its subordinate sheets and theirs in turn, in the order of the subschemas; a property or subschema written as its instance's own gives its sheets in its own place; a kind's sheet, and its subordinate sheets, come in the place of its first reference; and the sheet of instances, where it is not the sheet of the input values, then the sheet of runs, come last."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('order.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_order_2(self):
        """Records MUST be written in the order the input holds them: input values in input order, elements as their array orders them, members and instances as written, an instance before the instances within it, and runs of text in the order of their string."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('order.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_order_3(self):
        """The key columns MUST be written first, then the columns of the simple domains in the order of the schema's tree: a location's own properties in the order the schema writes them, the members of a property written as its instance's own in that property's place, then those an allOf subschema names, in the order of its subschemas."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('order.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
