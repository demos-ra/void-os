import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestJSONText(unittest.TestCase):

    def test_json_text_1(self):
        """JSON text MUST read a JSON text in UTF-8 as RFC 8259 defines it, a byte order mark at its start not ignored."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_2(self):
        """JSON text MUST give each instance of the text one record of instances, the value itself first and every instance before the instances within it, in the order written, its _parent the instance that holds it and its _pointer the JSON Pointer to it from that instance, ~ in a member name written ~0 and / written ~1."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_3(self):
        """_type MUST be the instance's primitive type, an integer a number, and _value its text: a string's characters, a number as written, true or false, and empty for null, an object and an array."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_4(self):
        """A string that holds FF, a line break or HT MUST have an empty _value, its text written to runs: split at each FF into pages, each page at each LF or CRLF into lines, each line at each HT into runs, a CRLF read as LF."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.4', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_5(self):
        """A CR not followed by LF, a character that is not a Unicode character, and HT, LF, FF or CR in a member name within a pointer MUST be left out, each place one is left out given as not carried by its JSON Pointer within the text."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.5', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_6(self):
        """An object whose names are not all unique MUST end the read as names not unique, its reason the JSON Pointer to the first object, in the order written, that repeats one, in its URI fragment representation."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.6', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_7(self):
        """named MUST give the instance a JSON Pointer names among a text's instances, evaluated from the text's value as RFC 6901 evaluates it, each reference token the _pointer of an instance within the one before it, and no instance where the pointer names none."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.7', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_json_text_8(self):
        """JSON text MUST reject what is not a JSON text as not a JSON text."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('json-text.8', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
