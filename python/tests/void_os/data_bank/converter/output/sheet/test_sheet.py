import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestSheet(unittest.TestCase):

    def test_sheet_1(self):
        """The sheet of the input values MUST be named by the title of the root schema; where that sheet is the sheet of instances or a kind's sheet, it is named as that sheet is (sheet.2, sheet.3)."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sheet.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_sheet_2(self):
        """A kind's sheet MUST be named by the title of its schema, else the last reference token of its $ref."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sheet.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_sheet_3(self):
        """Every sheet name and field name the converter fixes MUST begin with _: the sheet of instances is named _instances, and the sheet of runs _runs; a name taken or composed from the schema's names is written as void-os.4 writes a name taken from outside."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sheet.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_sheet_4(self):
        """Every other sheet MUST be named by its parent sheet's name and the parts of its path within the parent's instance, each after a full stop: the name of each property between them written as its instance's own, and then: for a property, the property's name; for a keyword, the keyword, then the pattern or zero-based position where the keyword holds more than one subschema, and items for the elements of an element that is itself an array; for a subschema that anyOf, oneOf, if, then, else or a dependency applies, the keyword, then the subschema's title, else a dependency's key, else its zero-based position where the keyword holds more than one subschema."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sheet.4', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_sheet_5(self):
        """Every sheet MUST have a header, its first record, which holds the name of each field, each column labelled with the name of its domain: the key columns by their names, _input value, _instance, _parent, _pointer, _page, _line and _position; a simple domain's column by its property's name; a member of a property written as its instance's own by that property's name, a full stop, and its own name, the role name qualifying the domain name; a member an allOf subschema names by its own name; and _type and _value by those names."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('sheet.5', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
