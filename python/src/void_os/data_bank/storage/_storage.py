"""where and how each input is kept: its folder and file, inserted only, each value whole"""
__all__ = ['communicated', 'folder', 'insert', 'inputs', 'mark_communicated', 'names', 'relations', 'stored', 'KeepingFailedError', 'NonConformingError']
import os
import sys
import time
import types
from datetime import datetime, timezone
from typing import Any

def communicated(values: dict[str, Any,], input_name: str, session: str, agent: str, relational_model: types.ModuleType, converter: types.ModuleType) -> int | float:
    try:
        return next((int(record[3]) for record in _records(values, '_communicated.mtsv', relational_model) if record[:3] == [input_name, session, agent]), 0)
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

def folder(values: dict[str, Any,], relational_model: types.ModuleType, converter: types.ModuleType) -> str:
    return _bank(values)

def insert(values: dict[str, Any,], input_name: str, input_values: list[bytes], module_specification: bytes, event: str, relational_model: types.ModuleType, converter: types.ModuleType) -> int | float:
    try:
        os.makedirs(_bank(values), exist_ok=True)
        _lock(values)
        try:
            return _inserted(values, input_name, input_values, module_specification, event, relational_model, converter)
        finally:
            os.unlink(_at(values, '_lock'))
    except converter.NonConformingError as error:
        raise NonConformingError(str(error))
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

def inputs(values: dict[str, Any,], relational_model: types.ModuleType, converter: types.ModuleType) -> dict[str, Any,]:
    try:
        found = _records(values, '_stored.mtsv', relational_model)
        records = []
        for input_name in dict.fromkeys((record[0] for record in found)):
            storage_11_count = len([record for record in found if record[0] == input_name])
            records.append([input_name, str(storage_11_count), _pathname(values, input_name)])
        return {'sheet name': '_inputs', 'header': ['_input', '_values', '_file'], 'records': records}
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

def mark_communicated(values: dict[str, Any,], input_name: str, session: str, agent: str, count: int | float, relational_model: types.ModuleType, converter: types.ModuleType) -> None:
    if any((character in session + agent for character in '\t\n\f\r')):
        return
    try:
        os.makedirs(_bank(values), exist_ok=True)
        _lock(values)
        try:
            found = [record for record in _records(values, '_communicated.mtsv', relational_model) if record[:3] != [input_name, session, agent]]
            _replace(values, _at(values, '_communicated.mtsv'), [{'sheet name': '_communicated', 'header': ['_input', '_session', '_agent', '_values'], 'records': found + [[input_name, session, agent, str(count)]]}], relational_model)
        finally:
            os.unlink(_at(values, '_lock'))
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

def names(values: dict[str, Any,], relational_model: types.ModuleType, converter: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return [{'sheet name': '_sheets', 'header': ['_input', '_place', '_sheet name'], 'records': _records(values, '_sheets.mtsv', relational_model)}, {'sheet name': '_fields', 'header': ['_input', '_place', '_position', '_field name'], 'records': _records(values, '_fields.mtsv', relational_model)}]
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

def relations(values: dict[str, Any,], input_name: str, relational_model: types.ModuleType, converter: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return _whole(_sheets(_pathname(values, input_name), relational_model), len([record for record in _records(values, '_stored.mtsv', relational_model) if record[0] == input_name]))
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

def stored(values: dict[str, Any,], input_name: str, first: int | float, last: int | float, relational_model: types.ModuleType, converter: types.ModuleType) -> dict[str, Any,]:
    try:
        return {'sheet name': '_stored', 'header': ['_input', '_input value', '_time', '_event'], 'records': [record for record in _records(values, '_stored.mtsv', relational_model) if record[0] == input_name and first <= int(record[1]) <= last]}
    except relational_model.NotMTSVError:
        raise KeepingFailedError('keeping failed')
    except OSError:
        raise KeepingFailedError('keeping failed')

class KeepingFailedError(Exception):
    """A file system failure, or a file of the data bank the parser rejects, MUST end the access as keeping failed, its reason those words alone, naming no path."""

class NonConformingError(Exception):
    """An input the converter rejects MUST end the insert as non-conforming, nothing being stored."""

def _at(values: dict[str, Any,], name: str) -> str:
    return os.path.join(_bank(values), name)

def _bank(values: dict[str, Any,]) -> str:
    return os.environ.get(_value(values, 'data bank variable')) or os.path.join(_documents(), _value(values, 'data bank folder'))

def _cut(values: dict[str, Any,], input_name: str, start: int, relational_model: types.ModuleType) -> None:
    held = _sheets(_pathname(values, input_name), relational_model)
    if any((int(record[0]) >= start for sheet in held for record in sheet['records'])):
        _replace(values, _pathname(values, input_name), _whole(held, start), relational_model)
    found = _records(values, '_stored.mtsv', relational_model)
    if any((record[0] == input_name and int(record[1]) >= start for record in found)):
        _replace(values, _at(values, '_stored.mtsv'), [{'sheet name': '_stored', 'header': ['_input', '_input value', '_time', '_event'], 'records': [record for record in found if record[0] != input_name or int(record[1]) < start]}], relational_model)

def _documents() -> str:
    if sys.platform == 'android':
        return '/storage/emulated/0/Documents'
    return os.path.join(os.path.expanduser('~'), 'Documents')

def _encoded(segment: str) -> str:
    named = ''.join((chr(octet) if chr(octet) in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~' else '%' + format(octet, '02X') for octet in bytes(segment, 'utf-8')))
    return '_' + named if named.startswith('_') else named

def _inserted(values: dict[str, Any,], input_name: str, input_values: list[bytes], module_specification: bytes, event: str, relational_model: types.ModuleType, converter: types.ModuleType) -> int:
    start = len([record for record in _records(values, '_stored.mtsv', relational_model) if record[0] == input_name])
    text = converter.convert(input_values, module_specification, start, relational_model)[0]
    named = converter.sheets(module_specification, input_name, relational_model)
    os.makedirs(os.path.dirname(_pathname(values, input_name)), exist_ok=True)
    _cut(values, input_name, start, relational_model)
    with open(_pathname(values, input_name), 'ab') as file:
        file.write(bytes(text, 'utf-8'))
    storage_8_time_now = datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    with open(_at(values, '_stored.mtsv'), 'ab') as file:
        file.write(relational_model.dump([{'sheet name': '_stored', 'header': ['_input', '_input value', '_time', '_event'], 'records': [[input_name, str(start + index), storage_8_time_now, event] for index in range(len(input_values))]}]))
    _replace(values, _at(values, '_sheets.mtsv'), [{'sheet name': '_sheets', 'header': named[0]['header'], 'records': _replaced(_records(values, '_sheets.mtsv', relational_model), input_name, named[0]['records'])}], relational_model)
    _replace(values, _at(values, '_fields.mtsv'), [{'sheet name': '_fields', 'header': named[1]['header'], 'records': _replaced(_records(values, '_fields.mtsv', relational_model), input_name, named[1]['records'])}], relational_model)
    return len(input_values)

def _lock(values: dict[str, Any,]) -> None:
    pathname = _at(values, '_lock')
    while True:
        try:
            with open(pathname, 'xb'):
                pass
            return
        except FileExistsError:
            pass
        try:
            if time.time() - os.stat(pathname).st_mtime > float(_value(values, 'lock timeout')):
                os.unlink(pathname)
            else:
                time.sleep(float(_value(values, 'lock wait')))
        except FileNotFoundError:
            pass

def _pathname(values: dict[str, Any,], input_name: str) -> str:
    segments = [_encoded(segment) for segment in input_name.replace(os.sep, '/').split('/') if segment]
    return os.path.join(_bank(values), os.sep.join(segments) + '.mtsv')

def _records(values: dict[str, Any,], name: str, relational_model: types.ModuleType) -> list[list[str]]:
    return [record for sheet in _sheets(_at(values, name), relational_model) for record in sheet['records']]

def _replace(values: dict[str, Any,], pathname: str, held: list[dict[str, Any,]], relational_model: types.ModuleType) -> None:
    with open(pathname + _value(values, 'replace suffix'), 'wb') as file:
        file.write(relational_model.dump(held))
    os.replace(pathname + _value(values, 'replace suffix'), pathname)

def _replaced(found: list[list[str]], input_name: str, given: list[list[str]]) -> list[list[str]]:
    held = [record[0] for record in found]
    place = held.index(input_name) if input_name in held else len(found)
    kept = [record for record in found if record[0] != input_name]
    return kept[:place] + given + kept[place:]

def _sheets(pathname: str, relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        with open(pathname, 'rb') as file:
            return relational_model.load(file.read())
    except FileNotFoundError:
        return []

def _value(values: dict[str, Any,], name: str) -> str:
    return dict(values['records'])[name]

def _whole(held: list[dict[str, Any,]], count: int) -> list[dict[str, Any,]]:
    kept = [{'sheet name': sheet['sheet name'], 'header': sheet['header'], 'records': [record for record in sheet['records'] if int(record[0]) < count]} for sheet in held]
    return [sheet for sheet in kept if sheet['records']]
