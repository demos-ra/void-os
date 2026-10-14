import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestDistributionPackage(unittest.TestCase):

    def test_distribution_package_1(self):
        """python/pyproject.toml MUST declare the build system the Values build requires and build backend name, and the project: name void-os, the version, requires-python, the dependency the Value python dependency mcp gives, license MIT, the [project.scripts] entry of the void-os command, and values.mtsv as package data, and no other table or field."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('distribution-package.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_distribution_package_2(self):
        """javascript/package.json MUST declare the name void-os, the version, the type module, the bin entry of the void-os command naming src/void-os.js, the engines the Value node engine gives, the dependencies the Values javascript dependency server and javascript dependency zod give, the license MIT, its files the folder src alone, which holds values.mtsv, and the mcpName the Value registry name gives, and no other field."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('distribution-package.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_distribution_package_3(self):
        """server.json MUST name the server by the Value registry name, describe it by the Value server description, and list two packages, the npm package and the PyPI package, each named void-os, at the version, each run with no argument over stdio."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('distribution-package.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_distribution_package_4(self):
        """Each README MUST say what void-os is, as scope.1 says it, and how it is installed: pipx install void-os for the PyPI package and npm install --global void-os for the npm package; lay out the modules as the Modules sheet's tree, each by its secret on one line; and, for the PyPI package, hold the Value registry name as the registry's ownership verification names it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('distribution-package.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_distribution_package_5(self):
        """Each LICENSE MUST be the MIT License's text, its copyright line the Value copyright holders."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('distribution-package.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
