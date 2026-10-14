import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestParser(unittest.TestCase):

    def test_parser_1(self):
        """The parser MUST accept every MTSV file that conforms, as MTSV-DRAFT decides for parsers."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('parser.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_parser_2(self):
        """The parser MUST treat a U+FEFF at the start of the text as an encoding signature, and not as part of the first field."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('parser.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_parser_3(self):
        """The parser MUST raise not MTSV for text that does not conform, its reason the number of the line where it stops conforming, counted from 1."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('parser.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_parser_4(self):
        """load MUST decode its octets as UTF-8, the character set of an MTSV file whose media type names none, before parsing them."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('parser.4', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
