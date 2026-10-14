"""the MCP server and the one tool it offers"""
__all__ = ['serve']
import types
from typing import Any
from void_os.tools.read import _read
from void_os.tools.server import _server

def serve(values: dict[str, Any,], relational_model: types.ModuleType, data_bank: types.ModuleType) -> None:
    return _server.serve(values, relational_model, data_bank, _read)
