import unittest
import os
from tests.void_os.system_generation.runner import _runner
from void_os.relational_model import _relational_model
from void_os.system_generation.values import _values

class TestServer(unittest.TestCase):

    def test_server_1(self):
        """The server MUST speak MCP over the stdio transport, reading its standard input and writing its standard output, until its standard input ends."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('server.1', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_server_2(self):
        """The server MUST answer server/discover with its name the Value server name, its version the Value version, and its instructions the Value server instructions with {data bank folder} filled with the folder the data bank's access program folder gives."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('server.2', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_server_3(self):
        """The server MUST offer one tool, named by the Value tool name and described by the Value tool description, whose input schema is an object whose properties are the arguments tool arguments names, each a string named as the parameter of read's read it is handed as, those tool arguments marks required its required properties."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('server.3', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_server_4(self):
        """The tool's result MUST be one text content holding the reply, and no structured content."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('server.4', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_server_5(self):
        """A call refused, or ended as keeping failed, MUST be reported as a tool execution error whose text is the reason."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('server.5', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])

    def test_server_6(self):
        """An argument the tool is not given MUST be handed to read as the empty text."""
        with self.subTest(case=1):
            self.assertEqual(_runner.run('server.6', 1, os.path.dirname(__file__) + '/../../../../../conformance', _relational_model, _values), [])
