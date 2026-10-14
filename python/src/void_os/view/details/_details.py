"""one value in full: every record of every sheet it gives"""
__all__ = ['details', 'KeepingFailedError']
import types
from typing import Any

def details(values: dict[str, Any,], input_name: str, position: int | float, relational_model: types.ModuleType, data_bank: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return data_bank.records(values, input_name, position, position, [], relational_model) + [data_bank.stored(values, input_name, position, position, relational_model)]
    except data_bank.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
