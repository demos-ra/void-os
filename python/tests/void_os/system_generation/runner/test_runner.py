import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestRunner(unittest.TestCase):

    def test_runner_1(self):
        """The access program run MUST find the case by its requirement and case among the cases of the file, in the folder conformance it is handed, of the requirement's module, and never by its place on disk, and read the books from the folder spec of the repository, the folder that holds the runner's own file at the path the Files sheet gives it, as module folder gives that file's folder."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_10(self):
        """A file of conformance the parser rejects MUST end run as not MTSV."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.10', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_11(self):
        """The case's access program, where it starts a component, MUST be run as the component's command starts it: a child process in $PWD with the environment of runner.2 alone, its program the command line of the Given of the Value the component's Command names, from the repository runner.1 reads the books from, its operands then the case's arguments; its standard input the case's stdin, each line then LF, in UTF-8, written when it starts, and closed once the lines of standard output read hold a response for each request among the lines written, or standard output ends, a request being a line that holds a JSON object with the members method and id, and a response a line that holds a JSON object with the member id and the member result or error; its standard output the lines read, then the rest."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.11', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_12(self):
        """Each file of octets MUST be placed at its pathname before the call, its octets those of the file it names, beside the file of the case's module or of a node above, nothing in it expanded, the directories its pathname needs made, and its modification time, where modified gives one, set that many seconds before the call."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.12', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_13(self):
        """Each zip package of zip entries MUST be placed at its pathname before the call, the directories its pathname needs made, written as ZIP-APPNOTE writes a ZIP file, its entries in order, each with its name, its method and the CRC-32 of its text in UTF-8, its data that text compressed by DEFLATE where its method is 8 and held as it is otherwise."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.13', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_14(self):
        """Each database of database statements MUST be placed at its pathname before the call, the directories its pathname needs made, built by running its statements in order on a new database there."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.14', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_15(self):
        """The error the call ends with, with its reason where the case gives one, whether standard output holds anything and whether standard error holds a diagnostic, where the case gives them, and each result of results, as its text, MUST be compared, run giving each comparison that does not hold."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.15', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_16(self):
        """Each fixture placed after MUST be compared as its sheets with what is at its pathname: a file, standard output, or a result, run giving each comparison that does not hold."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.16', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_17(self):
        """Each pathname of absent MUST hold nothing after the call, run giving each that does."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.17', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_18(self):
        """Each expected file MUST hold, after the call, the octets of the file it names, beside the file of the case's module or of a node above, run giving each that does not."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.18', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_19(self):
        """Each text of file texts MUST be held within one of the lines, or the incomplete line, of the file it names, run giving each that is not."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.19', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_2(self):
        """A case MUST be run in an empty directory made for it, its resolved pathname $PWD, $PWD/home the user's home folder by the variable the platform reads it from, TZ set to UTC0 and each variable of environment, and no other variable set but PATH and those the platform needs to start a program."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_20(self):
        """A field compared, whose column the Domains rows of the relation its sheet is named by give the type time, MUST match any date-time RFC 3339 writes with the offset Z."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.20', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_21(self):
        """A text read as a JSON text that JSON text rejects MUST be read as holding no instance."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.21', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_22(self):
        """A started component's exit status MUST be the result 1, its standard output what output, stdout lines and the fixture placed at - compare, and its standard error what diagnostic and reason compare."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.22', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_3(self):
        """Each fixture placed before, of the file of the case's module or of a node above, MUST be placed at its pathname before the call, the directories its pathname needs made."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_4(self):
        """The case's access program, where it starts no component, MUST be called on the case's module, loaded from its files as the Files sheet places them in the repository, with the Values as values gives them, or the fixture the case places at its values argument, the case's arguments and the fixtures placed at an argument, by the positions of the Parameters sheet, then each module Compositions hands that module, loaded the same way."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_5(self):
        """Each result of type JSON text MUST be compared by its instances, every instance result instances names and no other, each line of standard output by the instances stdout lines names, and each file of file instances by the instances it names, run giving each comparison that does not hold."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_6(self):
        """$PWD, $HOME, $INPUT and $REPOSITORY MUST be expanded in every value, and nothing else: $HOME/Documents the user's documents folder as PLATFORMDIRS gives it for the platform the case runs on, each / of a pathname the platform's separator, $INPUT $PWD as name within a folder writes it, and $REPOSITORY the repository runner.1 reads the books from."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.6', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_7(self):
        """A value MUST be read as the Written column of its type writes it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.7', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_8(self):
        """A case whose module and access program are empty MUST call nothing, each pathname it names being a file of the repository, relative to it."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.8', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_runner_9(self):
        """A requirement and case that name no case MUST end run as no case."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('runner.9', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
