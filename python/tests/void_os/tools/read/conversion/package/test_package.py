import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestPackage(unittest.TestCase):

    def test_package_1(self):
        """A zip entry MUST be read stored or deflated, the compression methods its package's format allows."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('package.1', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_package_2(self):
        """Each entry of a package whose name ends .xml or .rels MUST be read as XML into the relation nodes, each element, attribute and run of character data one node, each name expanded with its namespace, a namespace declaration being no node."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('package.2', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_package_3(self):
        """A package that is not a zip file, or an entry it reads as XML that is not well-formed, MUST end the read of its package as failed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('package.3', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])

    def test_package_4(self):
        """A zip entry compressed otherwise MUST end the read of its package as compression method not allowed."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('package.4', 1, os.path.dirname(__file__) + '/../../../../../../../conformance', _relational_model, _values), [])
