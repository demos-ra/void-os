import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestVoidOs(unittest.TestCase):

    def test_void_os_1(self):
        """Every datum void-os keeps or gives MUST be a relation in normal form, an MTSV sheet, each record beginning with its primary key, each field holding one value, and all its records distinct."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.1', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_10(self):
        """The command run with the Value view operand as its first operand MUST run the view, its other operands and its option --filter the view's, handing it whether standard output is a terminal and the machine's offset from UTC, as local offset gives it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.10', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_11(self):
        """An error that ends an access program the command calls MUST be written, by its reason, then LF, on standard error, the command ending with exit status 1."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.11', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_2(self):
        """void-os MUST be relationally complete: query giving restriction, projection, join and union, and the data bank's access program new giving difference, what is new being the values stored less those communicated to the session and agent it is asked for."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.2', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_3(self):
        """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.3', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_4(self):
        """A name void-os takes from outside that begins with _ MUST be written with that _ doubled, so that a name beginning with one _ is always one void-os fixes."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.4', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_5(self):
        """The void-os component MUST be started by the command the Value void-os command names, its operands its arguments."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.5', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_6(self):
        """The command run with no operand MUST start the server, over the standard streams, until its standard input ends."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.6', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_7(self):
        """The command run with one operand that is a hook event MUST run the hook of that event, handing it the working directory the command is run in, and end with exit status 0 where the hook ends without an error."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.7', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_8(self):
        """The command run with any other operands MUST write the Value usage message, then LF, on standard error and end with exit status 1."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.8', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])

    def test_void_os_9(self):
        """Every exit status the command gives other than 0 MUST be 1, as an exit status of 2 blocks a harness and erases a submitted prompt."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('void-os.9', 1, os.path.dirname(__file__) + '/../../../conformance', _relational_model, _values), [])
