import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestGenerator(unittest.TestCase):

    def test_generator_1(self):
        """The generator MUST write only MTSV files that conform, as MTSV-DRAFT decides for generators: an FF line before every sheet, the first included, a line break after every record, in UTF-8."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('generator.1', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_generator_2(self):
        """The generator MUST raise cannot be represented for a field or sheet name that holds HT, LF, FF or CR, its reason the sheet's position, the record's position and the field's position, joined by a space, the sheet and the field counted from 1, the record 0 for the sheet name, 1 for the header and from 2 for the records."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('generator.2', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])

    def test_generator_3(self):
        """dump MUST encode the MTSV text in UTF-8."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('generator.3', 1, os.path.dirname(__file__) + '/../../../../../../conformance', _relational_model, _values), [])
