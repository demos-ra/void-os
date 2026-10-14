"""which records a level keeps, by the filter query gives"""
__all__ = ['kept', 'RefusedError']
import types
from typing import Any

def kept(level: list[dict[str, Any,]], filter: str, relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return relational_model.kept(level, filter)
    except relational_model.RefusedError as error:
        raise RefusedError(str(error))

class RefusedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
