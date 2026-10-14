import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestSchema(unittest.TestCase):

    def test_schema_1(self):
        """A module specification MUST supply a schema of draft-07, valid against its metaschema, as a JSON text of any size, any depth of nesting and any length of string, against which every value of its input validates."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_11(self):
        """A $ref MUST be applied as the schema it references, as schema gives it, its other members ignored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.11', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_13(self):
        """Every assertion of the schema MUST be applied in validation."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.13', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_16(self):
        """A keyword that is neither a validation keyword nor $ref MUST be ignored in validation, asserting nothing: format, contentMediaType and contentEncoding among them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.16', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_17(self):
        """The access program schema MUST give each $ref of the schema with the location of the schema it references, its fragment percent-decoded as UTF-8 and evaluated as a JSON Pointer."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.17', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_2(self):
        """The access program validate MUST give, for each instance of each input value, each subschema applied to it and whether the instance is valid against it, and reject an input value that fails an assertion as non-conforming, its reason the value's position, a space, and the JSON Pointer to the deepest instance location where it fails, in its URI fragment representation."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_3(self):
        """The root schema MUST hold a title annotation, which names the sheet of the input values."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_4(self):
        """Every name the schema gives a sheet or a column, a title, a property's name, a key of patternProperties or dependencies, or the last reference token of a $ref, MUST be text a field can hold, holding no HT, LF, FF or CR."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.4', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_5(self):
        """A regular expression of pattern or patternProperties MUST use only the tokens schema authors should limit themselves to: individual characters, simple and complemented character classes and ranges, the quantifiers +, *, ?, {x}, {x,y} and {x,} and their lazy forms, the anchors ^ and $, and simple grouping and alternation, none taken to be anchored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.5', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_6(self):
        """A $ref MUST reference a schema within the supplied schema, the one schema the converter is given."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.6', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_7(self):
        """A $ref's fragment MUST be a JSON Pointer in its URI fragment representation, of the characters a URI fragment holds, $id not being read."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.7', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_8(self):
        """A $ref MUST NOT reach again, at the same instance location through allOf, anyOf, oneOf, not, if, then, else or a dependency, a schema it is applied from."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.8', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_schema_9(self):
        """A module specification that breaks schema.1 or schema.3-8 MUST be rejected as non-conforming."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('schema.9', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
