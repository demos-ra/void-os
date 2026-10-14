"""what the converter is given: the module specification and the input values, read through JSON text into relations"""
__all__ = ['read', 'NonConformingError']
import types
from typing import Any
from void_os.data_bank.converter.input.schema import _schema
from void_os.data_bank.converter.input.value import _value

def read(module_specification: bytes, input_values: list[bytes], start: int | float, relational_model: types.ModuleType) -> tuple[list[dict[str, Any,]], list[dict[str, Any,]], list[str],]:
    try:
        relations = _schema.schema(module_specification, relational_model)
        values, not_carried, = _value.values(input_values, start, relational_model)
        return relations, values + [_schema.validate(relations, values, relational_model)], not_carried,
    except _schema.NonConformingError as error:
        raise NonConformingError(str(error))
    except _value.NonConformingError as error:
        raise NonConformingError(str(error))

class NonConformingError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
