"""what every reply states: the report, then the map or the values"""
__all__ = ['reply']
import types
from typing import Any

def reply(report: list[dict[str, Any,]], answer: list[dict[str, Any,]], relational_model: types.ModuleType) -> str:
    return relational_model.dumps([relation for name in ['file', 'not read', 'left behind', 'sheets'] for relation in report if relation['sheet name'] == name] + answer)
