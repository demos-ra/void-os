"""what one input holds: its days, then the turns of a day"""
__all__ = ['days', 'turns', 'KeepingFailedError']
import types
from datetime import datetime, timedelta
from typing import Any

def days(values: dict[str, Any,], input_name: str, offset: int | float, relational_model: types.ModuleType, data_bank: types.ModuleType) -> dict[str, Any,]:
    counts = {}
    for entry in _stored(values, input_name, relational_model, data_bank):
        key = _date(entry[1], offset) + '\t' + entry[2]
        counts[key] = counts.get(key, 0) + 1
    return {'sheet name': 'days', 'header': ['input', 'day', 'event', 'values'], 'records': [[input_name] + key.split('\t') + [str(count)] for key, count, in counts.items()]}

def turns(values: dict[str, Any,], input_name: str, day: str, offset: int | float, relational_model: types.ModuleType, data_bank: types.ModuleType) -> dict[str, Any,]:
    chosen = [entry for entry in _stored(values, input_name, relational_model, data_bank) if _date(entry[1], offset) == day]
    found = []
    if chosen:
        try:
            sheets = data_bank.records(values, input_name, int(chosen[0][0]), int(chosen[len(chosen) - 1][0]), [], relational_model)
        except data_bank.KeepingFailedError as error:
            raise KeepingFailedError(str(error))
        runs = _sheet(sheets, '_runs')
        for entry in chosen:
            instances = {'sheet name': 'instances', 'header': ['_instance', '_parent', '_pointer', '_type', '_value'], 'records': [['0', '', '', 'object', '']] + [record[1:] for record in _sheet(sheets, '_instances') if record[0] == entry[0]]}
            held = [run for run in runs if run[0] == entry[0]]
            found.append([input_name, entry[0], entry[1], entry[2]] + [_member(instances, held, column, relational_model) for column in ['agent', 'session', 'turn', 'model']] + [_first_line(instances, held)])
    return {'sheet name': 'turns', 'header': ['input', 'value', 'time', 'event', 'agent', 'session', 'turn', 'model', 'first line'], 'records': found}

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

def _date(time: str, offset: int | float) -> str:
    zoom_3_full_date_at_offset = (datetime.fromisoformat(time) + timedelta(minutes=offset)).date().isoformat()
    return zoom_3_full_date_at_offset

def _first_line(instances: dict[str, Any,], runs: list[list[str]]) -> str:
    for instance in instances['records']:
        if instance[3] == 'string' and _text(instance, runs) != '':
            return _text(instance, runs).split('\n')[0]
    return ''
_harness_members = [{'column': 'place', 'pointer': '/cwd', 'harness': 'Codex'}, {'column': 'place', 'pointer': '/workspace_roots/0', 'harness': 'Cursor'}, {'column': 'agent', 'pointer': '/agent_id', 'harness': 'Claude Code'}, {'column': 'agent', 'pointer': '/agent_id', 'harness': 'Codex'}, {'column': 'agent', 'pointer': '/subagent_id', 'harness': 'Cursor'}, {'column': 'session', 'pointer': '/session_id', 'harness': 'Claude Code'}, {'column': 'session', 'pointer': '/session_id', 'harness': 'Codex'}, {'column': 'session', 'pointer': '/conversation_id', 'harness': 'Cursor'}, {'column': 'turn', 'pointer': '/prompt_id', 'harness': 'Claude Code'}, {'column': 'turn', 'pointer': '/turn_id', 'harness': 'Codex'}, {'column': 'turn', 'pointer': '/generation_id', 'harness': 'Cursor'}, {'column': 'model', 'pointer': '/model', 'harness': 'Claude Code'}, {'column': 'model', 'pointer': '/model', 'harness': 'Codex'}, {'column': 'model', 'pointer': '/model', 'harness': 'Cursor'}]

def _member(instances: dict[str, Any,], runs: list[list[str]], column: str, relational_model: types.ModuleType) -> str:
    for entry in _harness_members:
        if entry['column'] == column:
            named = relational_model.named(instances, entry['pointer'])
            if named['records']:
                return _text(named['records'][0], runs)
    return ''

def _sheet(sheets: list[dict[str, Any,]], name: str) -> list[list[str]]:
    return [record for sheet in sheets if sheet['sheet name'] == name for record in sheet['records']]

def _stored(values: dict[str, Any,], input_name: str, relational_model: types.ModuleType, data_bank: types.ModuleType) -> list[list[str]]:
    try:
        count = sum((int(record[1]) for record in _sheet(data_bank.names(values, relational_model), '_inputs') if record[0] == input_name))
        stored = data_bank.stored(values, input_name, 0, count - 1, relational_model)
    except data_bank.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    header = stored['header']
    return [[record[header.index('_input value')], record[header.index('_time')], record[header.index('_event')]] for record in stored['records']]

def _text(instance: list[str], runs: list[list[str]]) -> str:
    content = instance[4]
    page = 0
    line = 0
    position = 0
    for run in runs:
        if run[1] == instance[0]:
            while page < int(run[2]):
                content = content + '\f'
                page = page + 1
                line = 0
                position = 0
            while line < int(run[3]):
                content = content + '\n'
                line = line + 1
                position = 0
            while position < int(run[4]):
                content = content + '\t'
                position = position + 1
            content = content + run[5]
    return content
