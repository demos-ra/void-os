"""what a hook gives the harness as context, and in which form"""
__all__ = ['context', 'KeepingFailedError']
import json
import types
from typing import Any

def context(values: dict[str, Any,], event: str, input_name: str, hook_input: dict[str, Any,], relational_model: types.ModuleType, data_bank: types.ModuleType) -> str:
    taken = [entry for entry in _answer_members if entry['event'] == event]
    placed = [entry for entry in _context_members if entry['event'] == event]
    if not taken and not placed:
        return ''
    answer = {}
    for entry in taken:
        _place(answer, entry['pointer'], json.loads(entry['value']))
    if placed:
        try:
            text = _composed(values, placed[0]['begins'], input_name, hook_input, relational_model, data_bank)
        except data_bank.KeepingFailedError as error:
            raise KeepingFailedError(str(error))
        for entry in placed:
            _place(answer, entry['pointer'], text)
    hook_output_7_json_text_write = json.dumps(answer, ensure_ascii=False, separators=(',', ':',))
    return hook_output_7_json_text_write

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
_answer_members = [{'event': 'SessionStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SessionStart"'}, {'event': 'SessionStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SessionStart"'}, {'event': 'SubagentStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SubagentStart"'}, {'event': 'SubagentStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SubagentStart"'}, {'event': 'UserPromptSubmit', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"UserPromptSubmit"'}, {'event': 'UserPromptSubmit', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"UserPromptSubmit"'}, {'event': 'subagentStart', 'harness': 'Cursor', 'pointer': '/permission', 'value': '"allow"'}, {'event': 'beforeSubmitPrompt', 'harness': 'Cursor', 'pointer': '/continue', 'value': 'true'}]

def _composed(values: dict[str, Any,], begins: bool, input_name: str, hook_input: dict[str, Any,], relational_model: types.ModuleType, data_bank: types.ModuleType) -> str:
    names = data_bank.names(values, relational_model) if begins else []
    session = _member(hook_input, 'session', relational_model)
    agent = _member(hook_input, 'agent', relational_model)
    fresh = data_bank.new(values, input_name, session, agent, [], relational_model)
    owned = _own(fresh, session, agent, relational_model)
    positions = [record[1] for record in fresh[-1]['records'] if record[1] not in owned]
    for index in range(len(positions)):
        text = relational_model.dumps(names + [relation for position in positions[index:] for relation in [_kept(each, 0, [position]) for each in fresh[:-1]] + [_kept(fresh[-1], 1, [position])] if relation['records']])
        if len(text) <= int(dict(values['records'])['context limit']):
            return text
    return relational_model.dumps(names)
_context_members = [{'event': 'SessionStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': True}, {'event': 'SessionStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': True}, {'event': 'SubagentStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': True}, {'event': 'SubagentStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': True}, {'event': 'UserPromptSubmit', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': False}, {'event': 'UserPromptSubmit', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': False}, {'event': 'sessionStart', 'harness': 'Cursor', 'pointer': '/additional_context', 'begins': True}, {'event': 'postToolUse', 'harness': 'Cursor', 'pointer': '/additional_context', 'begins': False}]
_harness_members = [{'column': 'place', 'pointer': '/cwd', 'harness': 'Codex'}, {'column': 'place', 'pointer': '/workspace_roots/0', 'harness': 'Cursor'}, {'column': 'agent', 'pointer': '/agent_id', 'harness': 'Claude Code'}, {'column': 'agent', 'pointer': '/agent_id', 'harness': 'Codex'}, {'column': 'agent', 'pointer': '/subagent_id', 'harness': 'Cursor'}, {'column': 'session', 'pointer': '/session_id', 'harness': 'Claude Code'}, {'column': 'session', 'pointer': '/session_id', 'harness': 'Codex'}, {'column': 'session', 'pointer': '/conversation_id', 'harness': 'Cursor'}, {'column': 'turn', 'pointer': '/prompt_id', 'harness': 'Claude Code'}, {'column': 'turn', 'pointer': '/turn_id', 'harness': 'Codex'}, {'column': 'turn', 'pointer': '/generation_id', 'harness': 'Cursor'}, {'column': 'model', 'pointer': '/model', 'harness': 'Claude Code'}, {'column': 'model', 'pointer': '/model', 'harness': 'Codex'}, {'column': 'model', 'pointer': '/model', 'harness': 'Cursor'}]

def _kept(relation: dict[str, Any,], column: int, chosen: list[str]) -> dict[str, Any,]:
    return {'sheet name': relation['sheet name'], 'header': relation['header'], 'records': [record for record in relation['records'] if record[column] in chosen]}

def _member(instances: dict[str, Any,], column: str, relational_model: types.ModuleType) -> str:
    for entry in _harness_members:
        if entry['column'] == column:
            named = relational_model.named(instances, entry['pointer'])
            if named['records']:
                return named['records'][0][4]
    return ''

def _own(fresh: list[dict[str, Any,]], session: str, agent: str, relational_model: types.ModuleType) -> list[str]:
    owned = []
    for record in fresh[-1]['records']:
        instances = {'sheet name': 'instances', 'header': ['_instance', '_parent', '_pointer', '_type', '_value'], 'records': [entry[1:] for relation in fresh if relation['sheet name'] == '_instances' for entry in relation['records'] if entry[0] == record[1]]}
        if _member(instances, 'session', relational_model) == session and _member(instances, 'agent', relational_model) == agent:
            owned.append(record[1])
    return owned

def _place(answer: dict[str, Any,], pointer: str, value: Any) -> None:
    tokens = [token.replace('~1', '/').replace('~0', '~') for token in pointer.split('/')[1:]]
    held = answer
    for token in tokens[:-1]:
        held = held.setdefault(token, {})
    held[tokens[-1]] = value
