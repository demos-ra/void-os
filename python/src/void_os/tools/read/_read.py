"""how a pathname is read as MTSV: a file, a directory of files, or the data bank"""
__all__ = ['read', 'KeepingFailedError', 'RefusedError']
import os
import types
from typing import Any
from void_os.tools.read.conversion import _conversion
from void_os.tools.read.input import _input
from void_os.tools.read.reply import _reply

def read(values: dict[str, Any,], pathname: str, sheet: str, records: str, fields: str, filter: str, join: str, relational_model: types.ModuleType, data_bank: types.ModuleType) -> str:
    bank = os.path.realpath(data_bank.folder(values, relational_model))
    place = os.path.realpath(pathname) if pathname.startswith('/') else pathname
    alone = sheet + records + fields + filter + join == ''
    try:
        given = _banked(values, place, bank, alone, data_bank, relational_model) if place == bank or place.startswith(bank + '/') else _files(pathname, place, relational_model)
        file = {'sheet name': 'file', 'header': ['file', 'source'], 'records': given[2]}
        chosen = relational_model.chosen(given[0], {'sheet name': 'origins', 'header': ['sheet', 'file'], 'records': given[1]}, file, given[3], sheet, records, fields, filter, join)
    except data_bank.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _input.RefusedError as error:
        raise RefusedError(str(error))
    except relational_model.RefusedError as error:
        raise RefusedError(str(error))
    return _reply.reply([file, {'sheet name': 'not read', 'header': ['file', 'status', 'reason'], 'records': given[4]}, {'sheet name': 'left behind', 'header': ['file', 'what'], 'records': given[5]}, chosen[1]], [{'sheet name': 'fields', 'header': ['file', 'sheet', 'field', 'field name'], 'records': _map(chosen)}] if alone else chosen[0], relational_model)

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class RefusedError(Exception):
    """A file named directly whose conversion ends as no format or failed MUST end the read as refused, its reason that error's name, then, for failed, a colon, a space and that error's reason.

A pathname, a file, a selection or a filter refused MUST end the read as refused, with its reason."""

def _banked(values: dict[str, Any,], place: str, bank: str, alone: bool, data_bank: types.ModuleType, relational_model: types.ModuleType) -> list[Any]:
    names = data_bank.names(values, relational_model)
    inputs = [relation for relation in names if relation['sheet name'] == '_inputs'][0]['records']
    if place == bank and alone:
        return [names, [[str(index + 1), '1'] for index, relation, in enumerate(names)], [['1', bank]], 'file', [], []]
    if place == bank:
        sheets = []
        origins = []
        for index, given, in enumerate(inputs):
            for relation in data_bank.records(values, given[0], 0, int(given[1]) - 1, [], relational_model):
                sheets.append(relation)
                origins.append([str(len(sheets)), str(index + 1)])
        return [sheets, origins, [[str(index + 1), given[0]] for index, given, in enumerate(inputs)], '_input', [], []]
    for given in inputs:
        if place == os.path.realpath(given[2]):
            sheets = data_bank.records(values, given[0], 0, int(given[1]) - 1, [], relational_model) + [data_bank.stored(values, given[0], 0, int(given[1]) - 1, relational_model)]
            return [sheets, [[str(index + 1), '1'] for index, relation, in enumerate(sheets)], [['1', given[0]]], 'file', [], []]
    raise RefusedError('names no input of the data bank')

def _files(pathname: str, place: str, relational_model: types.ModuleType) -> list[Any]:
    members = _input.members(pathname)
    sheets = []
    origins = []
    left = list(members[1]['records'])
    behind = []
    for number, source, in members[0]['records']:
        if number not in [record[0] for record in members[1]['records']]:
            converted = [[], []]
            try:
                converted = _conversion.sheets(source, relational_model)
            except _conversion.NoFormatError:
                if source == place:
                    raise RefusedError('no format')
                left.append([number, 'no format', ''])
            except _conversion.FailedError as error:
                if source == place:
                    raise RefusedError('failed: ' + str(error))
                left.append([number, 'failed', str(error)])
            for relation in converted[0]:
                sheets.append(relation)
                origins.append([str(len(sheets)), number])
            for what in converted[1]:
                behind.append([number, what])
    return [sheets, origins, members[0]['records'], 'file', left, behind]

def _map(chosen: tuple[list[dict[str, Any,]], dict[str, Any,],]) -> list[list[str]]:
    found = []
    for index, relation, in enumerate(chosen[0]):
        for position, name, in enumerate(relation['header'] or []):
            found.append([chosen[1]['records'][index][0], chosen[1]['records'][index][1], str(position + 1), name])
    return found
