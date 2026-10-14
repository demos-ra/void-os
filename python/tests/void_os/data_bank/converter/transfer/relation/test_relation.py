import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestRelation(unittest.TestCase):

    def test_relation_1(self):
        """A relation is a sheet, and the input values MUST be written as one relation, the sheet of the input values; where a $ref references the root schema, the root schema is a kind, and the sheet of the input values is its kind's one sheet."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_10(self):
        """A property that allows exactly one type, object, and that its schema does not require, MUST be written as a subordinate sheet, of one record or none."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.10', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_11(self):
        """A subschema that anyOf, oneOf, if, then, else or a dependency applies to the same location, and that allows exactly one type, object, MUST be written as a subordinate sheet of that location's sheet, where the location is not placed branch by branch (relation.12), whose records are the instances whose annotations it collects: under each branch of anyOf and oneOf an instance is valid against, under if where valid, under then or else as if decides, and under a dependency's schema where the instance holds its key."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.11', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_12(self):
        """A child location whose anyOf or oneOf gives its branches, and that allows other than exactly one type, or that relation.8 does not write as its instance's own and whose own schema, apart from its branches, gives it no column and no sheet but those the whole file shares, MUST be placed branch by branch: each instance as the location would be if its schema were the first branch, in the order of the subschemas, that the instance is valid against, a property's being taken as not required, the location having no record of its own."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.12', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_13(self):
        """A property that allows exactly one type, array, whose items is one schema, MUST be written as the sheet of its elements, and an element that is itself an array as a subordinate sheet of its own; and one whose items is an array of schemas as a sheet of one record per array, with a subordinate sheet for each schema of items and for additionalItems, each holding the elements at its positions."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.13', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_14(self):
        """A string that holds FF, a line break or HT MUST be written as its runs of text, as JSON text gives them, to the file's one sheet of runs, which the schema gives where any location can hold a string, each run one record with its page, line and position."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.14', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_15(self):
        """Every other value MUST be written molten, to the file's one sheet of instances, which the schema gives where any location is written molten: a property that allows other than exactly one type and is not placed branch by branch (relation.12), or one simple type but is not required; a child location whose subschema allows other than exactly one type and is not placed branch by branch; a member no schema covers (relation.16), and an element at a position no schema of items or additionalItems covers; and the input values themselves, where the root schema allows other than exactly one type, object or array. It holds every instance within the value, the value itself included; where the root schema allows other than exactly one type, object or array, the sheet of the input values is the sheet of instances."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.15', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_16(self):
        """Each value MUST be written once. A schema covers a member that its properties names or that a pattern of its patternProperties matches; a member is written by its location's own schema where that covers it; else by the first subschema, in the order of the subschemas, whose annotations the instance collects and that covers it; else by the first additionalProperties that applies, which takes only the members its schema does not cover; else it is written molten (relation.15)."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.16', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_17(self):
        """A sheet MUST NOT be given a column from an allOf subschema for a property that its location's own schema or an earlier allOf subschema names; where a member is written by an earlier sheet, its field in a later one is empty, its value found by the same key."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.17', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_18(self):
        """The relation module MUST give each relation the schema gives with the parts of its path, each column with the parts of its label, and each record and cell."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.18', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_19(self):
        """A sheet MUST NOT be shaped from not, whose annotations are ignored, propertyNames, which applies to names, definitions, which applies to nothing by itself, or contains, whose elements items places."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.19', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_2(self):
        """The schema a $ref references is a kind; every instance that a $ref applies to a child location, or to the same location through anyOf, oneOf, if, then, else or a dependency, MUST be written to its kind's one sheet, placed by the kind's schema alone, as a child location's instances are, wherever it is referenced."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_3(self):
        """A $ref that allOf applies MUST be read as adding to its instance's own schema, not as a kind."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_4(self):
        """The primitive types an instance location allows MUST be taken as those its type keyword lists, all six where it has none, narrowed by every subschema allOf applies there and by the union of the branches of anyOf and oneOf."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.4', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_5(self):
        """By those types, and by whether its schema requires it, each value MUST be written in one of three places: a column of the record that holds it, a simple domain (relation.6, relation.8); a sheet of its own, a nonsimple domain (relation.9-14); or the sheet of instances, molten (relation.15)."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.5', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_6(self):
        """A property that its schema requires, that is not a kind, and that allows exactly one type, string, number, boolean or null, a simple domain, MUST be written as a column of its sheet, its field holding the property's value."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.6', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_7(self):
        """A subordinate sheet whose child instances allow exactly one type, string, number, boolean or null, MUST have one column, _value."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.7', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_8(self):
        """A property that its schema requires, that is not a kind, and that allows exactly one type, object, and every subschema allOf applies to a location that allows exactly one type, object, MUST be written as its instance's own: the members such a property holds, and those such a subschema names, written as members of the instance that holds them, and the subschemas the keywords of either apply taken as that instance's."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.8', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_relation_9(self):
        """Each subschema applied to child locations that is a property that allows exactly one type, array, or items, each schema of items given as an array, additionalItems, a pattern of patternProperties, or additionalProperties, a repeating group, MUST be struck from its parent and written as a subordinate sheet of its own, whose records are its child instances."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('relation.9', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
