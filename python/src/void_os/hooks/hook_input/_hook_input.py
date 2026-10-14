"""how a hook's input is inserted into the data bank"""
__all__ = ['insert', 'KeepingFailedError', 'NonConformingError']
import types
from typing import Any

def insert(values: dict[str, Any,], input_name: str, event: str, hook_input: bytes, relational_model: types.ModuleType, data_bank: types.ModuleType) -> int | float:
    try:
        return data_bank.insert(values, input_name, [hook_input], bytes(dict(values['records'])['hook input schema'], 'utf-8'), event, relational_model)
    except data_bank.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except data_bank.NonConformingError as error:
        raise NonConformingError(str(error))

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NonConformingError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
