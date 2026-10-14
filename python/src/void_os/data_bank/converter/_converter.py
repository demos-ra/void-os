"""how the JSON values a schema describes become relations, written as one MTSV file"""
__all__ = ['convert', 'sheets', 'NonConformingError']
import types
from typing import Any
from void_os.data_bank.converter.input import _input
from void_os.data_bank.converter.output import _output
from void_os.data_bank.converter.transfer import _transfer

def convert(input_values: list[bytes], module_specification: bytes, start: int | float, relational_model: types.ModuleType) -> tuple[str, list[str],]:
    try:
        relations, values, not_carried, = _input.read(module_specification, input_values, start, relational_model)
        return _output.write(_transfer.transfer(relations, values), values, relational_model), not_carried,
    except _input.NonConformingError as error:
        raise NonConformingError(str(error))

def sheets(module_specification: bytes, input_name: str, relational_model: types.ModuleType) -> tuple[dict[str, Any,], dict[str, Any,],]:
    try:
        relations, values, = _input.read(module_specification, [], 0, relational_model)[:2]
        transferred = _transfer.transfer(relations, values)
        named = _output.sheets([transferred[0], transferred[1], transferred[2], transferred[3], transferred[7]], relational_model)
        return {'sheet name': '_sheets', 'header': ['_input', '_place', '_sheet name'], 'records': [[input_name, str(place), relation['sheet name']] for place, relation, in enumerate(named)]}, {'sheet name': '_fields', 'header': ['_input', '_place', '_position', '_field name'], 'records': [[input_name, str(place), str(position), name] for place, relation, in enumerate(named) for position, name, in enumerate(relation['header'])]},
    except _input.NonConformingError as error:
        raise NonConformingError(str(error))

class NonConformingError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
