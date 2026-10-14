"""which sheets, records and fields a reader names, as the relational algebra's operations, written by position and by filter"""
__all__ = ['chosen', 'kept', 'RefusedError']
from typing import Any
from void_os.relational_model.query.filter_expression import _filter_expression
from void_os.relational_model.query.operations_on_relations import _operations_on_relations
from void_os.relational_model.query.positions import _positions
from void_os.relational_model.query.set_operations import _set_operations

def chosen(sheets: list[dict[str, Any,]], origins: dict[str, Any,], file: dict[str, Any,], lead: str, sheet: str, records: str, fields: str, filter: str, join: str) -> tuple[list[dict[str, Any,]], dict[str, Any,],]:
    try:
        of = {record[0]: record[1] for record in origins['records']}
        members = []
        for each in dict.fromkeys((of[str(position)] for position in range(1, len(sheets) + 1))):
            given = [sheets[position - 1] for position in range(1, len(sheets) + 1) if of[str(position)] == each]
            given = _operations_on_relations.join(given, _origins_of([each] * len(given)), join, _positions, _filter_expression)
            numbers = [int(found[0]) for found in _positions.named(sheet, len(given))['records']] if sheet else range(1, len(given) + 1)
            members.extend(([each, number, given[number - 1], _operations_on_relations.restrict([given[number - 1]], '', filter, _positions, _filter_expression)[0]] for number in numbers))
        restricted = []
        report = []
        for name in dict.fromkeys((member[2]['sheet name'] for member in members)):
            group = [member for member in members if member[2]['sheet name'] == name]
            outputs = [[member[3], [member]] for member in group] if len({member[0] for member in group}) == 1 else [[united, [member for member in group if (None if member[3]['header'] is None else [lead] + member[3]['header']) == united['header']]] for united in _set_operations.union([member[3] for member in group], _origins_of([member[0] for member in group]), file, lead)]
            for given, parts, in outputs:
                numbers = [int(found[0]) for found in _positions.named(records, len(given['records']))['records']] if records else range(1, len(given['records']) + 1)
                offset = 0
                for part in parts:
                    report.append([part[0], str(part[1]), name, str(len(part[2]['records'])), str(len(part[3]['records'])), _positions.written({'sheet name': 'positions', 'header': ['position'], 'records': [[str(number)] for number in numbers if offset < number <= offset + len(part[3]['records'])]})])
                    offset += len(part[3]['records'])
                restricted.append({'sheet name': name, 'header': given['header'], 'records': [given['records'][number - 1] for number in numbers]})
        return _operations_on_relations.project(restricted, fields, _positions, _filter_expression), {'sheet name': 'sheets', 'header': ['file', 'sheet', 'sheet name', 'records', 'matches', 'positions'], 'records': report},
    except _operations_on_relations.RefusedError as error:
        raise RefusedError(str(error))
    except _positions.RefusedError as error:
        raise RefusedError(str(error))

def kept(sheets: list[dict[str, Any,]], filter: str) -> list[dict[str, Any,]]:
    try:
        return _filter_expression.kept(sheets, filter)
    except _filter_expression.RefusedError as error:
        raise RefusedError(str(error))

class RefusedError(Exception):
    """A selection, filter or join refused MUST end chosen and kept as refused, with its reason."""

def _origins_of(files):
    return {'sheet name': 'origins', 'header': ['sheet', 'file'], 'records': [[str(position), each] for position, each, in enumerate(files, 1)]}
