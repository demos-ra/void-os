"""how a JSON file becomes sheets"""
__all__ = ['load', 'CannotBeRepresentedError', 'NamesNotUniqueError', 'NotAJSONTextError']
import types
from typing import Any

def load(octets: bytes, relational_model: types.ModuleType) -> tuple[list[dict[str, Any,]], list[str],]:
    try:
        instances, runs, not_carried, = relational_model.instances(octets)
    except relational_model.NotAJSONTextError as error:
        raise NotAJSONTextError(str(error))
    except relational_model.NamesNotUniqueError as error:
        raise NamesNotUniqueError(str(error))
    if runs['records']:
        raise CannotBeRepresentedError('cannot be represented')
    held = instances['records']
    return [{'sheet name': _string(held, _member(held, element, '/sheet name')), 'header': _strings(held, _member(held, element, '/header')), 'records': [_strings(held, record) for record in _elements(held, _member(held, element, '/records'))]} for element in _elements(held, '0')], not_carried,

class CannotBeRepresentedError(Exception):
    """A value that is not a string, or a field that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""

class NamesNotUniqueError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NotAJSONTextError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

def _elements(held: list[list[str]], instance: str) -> list[str]:
    _typed(held, instance, 'array')
    return [record[0] for record in held if record[1] == instance]

def _member(held: list[list[str]], instance: str, pointer: str) -> str:
    _typed(held, instance, 'object')
    found = [record[0] for record in held if record[1] == instance and record[2] == pointer]
    if not found:
        raise CannotBeRepresentedError('cannot be represented')
    return found[0]

def _string(held: list[list[str]], instance: str) -> str:
    record = _typed(held, instance, 'string')
    if any((character in record[4] for character in '\t\n\f\r')):
        raise CannotBeRepresentedError('cannot be represented')
    return record[4]

def _strings(held: list[list[str]], instance: str) -> list[str]:
    return [_string(held, element) for element in _elements(held, instance)]

def _typed(held: list[list[str]], instance: str, kind: str) -> list[str]:
    found = [record for record in held if record[0] == instance and record[3] == kind]
    if not found:
        raise CannotBeRepresentedError('cannot be represented')
    return found[0]
