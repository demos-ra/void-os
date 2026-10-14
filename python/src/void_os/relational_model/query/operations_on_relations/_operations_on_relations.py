"""the less traditional operations on relations: restriction by position or filter, projection by fields, and join on shared columns"""
__all__ = ['join', 'project', 'restrict', 'RefusedError']
import functools
import types
from typing import Any

def join(sheets: list[dict[str, Any,]], origins: dict[str, Any,], join: str, positions: types.ModuleType, filter_expression: types.ModuleType) -> list[dict[str, Any,]]:
    if not join:
        return sheets
    of = {record[0]: record[1] for record in origins['records']}
    grouped = {}
    for position, sheet, in enumerate(sheets, 1):
        grouped.setdefault(of[str(position)], []).append(sheet)
    joined = []
    try:
        for each in grouped.values():
            named = [each[int(found[0]) - 1] for found in positions.named(join, len(each))['records']]
            if named:
                joined.append(functools.reduce(_joined, named))
            joined.extend((sheet for sheet in each if all((sheet is not chosen for chosen in named))))
    except positions.RefusedError as error:
        raise RefusedError(str(error))
    return joined

def project(sheets: list[dict[str, Any,]], fields: str, positions: types.ModuleType, filter_expression: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return [sheet if not fields or sheet['header'] is None else _projected(sheet, [int(found[0]) - 1 for found in positions.named(fields, len(sheet['header']))['records']]) for sheet in sheets]
    except positions.RefusedError as error:
        raise RefusedError(str(error))

def restrict(sheets: list[dict[str, Any,]], records: str, filter: str, positions: types.ModuleType, filter_expression: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        kept = filter_expression.kept(sheets, filter) if filter else sheets
        return [{'sheet name': sheet['sheet name'], 'header': sheet['header'], 'records': [sheet['records'][int(found[0]) - 1] for found in positions.named(records, len(sheet['records']))['records']] if records else sheet['records']} for sheet in kept]
    except filter_expression.RefusedError as error:
        raise RefusedError(str(error))
    except positions.RefusedError as error:
        raise RefusedError(str(error))

class RefusedError(Exception):
    """A join of sheets that share no column MUST be refused."""

def _joined(left, right):
    shared = [name for name in left['header'] or [] if name in (right['header'] or [])]
    if not shared:
        raise RefusedError('the sheets ' + left['sheet name'] + ' and ' + right['sheet name'] + ' share no column')
    others = [index for index, name, in enumerate(right['header']) if name not in shared]
    return {'sheet name': left['sheet name'] + '*' + right['sheet name'], 'header': left['header'] + [right['header'][index] for index in others], 'records': [first + [second[index] for index in others] for first in left['records'] for second in right['records'] if all((first[left['header'].index(name)] == second[right['header'].index(name)] for name in shared))]}

def _projected(sheet, kept):
    if not kept:
        return {'sheet name': sheet['sheet name'], 'header': None, 'records': []}
    return {'sheet name': sheet['sheet name'], 'header': [sheet['header'][index] for index in kept], 'records': [[record[index] for index in kept] for record in sheet['records']]}
