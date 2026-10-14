"""how a harness's hook events reach the data bank, and what they give back"""
__all__ = ['hook', 'KeepingFailedError', 'NonConformingError']
import os
import sys
import types
from typing import Any
from void_os.hooks.hook_input import _hook_input
from void_os.hooks.hook_output import _hook_output

def hook(values: dict[str, Any,], event: str, working_directory: str, relational_model: types.ModuleType, data_bank: types.ModuleType) -> None:
    hooks_7_read_standard_input = sys.stdin.buffer.read()
    try:
        given = relational_model.instances(hooks_7_read_standard_input)
    except relational_model.NotAJSONTextError:
        raise NonConformingError('non-conforming')
    except relational_model.NamesNotUniqueError:
        raise NonConformingError('non-conforming')
    place = ''
    for entry in _harness_variables:
        if place == '' and entry['column'] == 'place':
            hooks_2_environment_variable = os.environ.get(entry['variable'])
            if hooks_2_environment_variable is not None:
                place = hooks_2_environment_variable
    for entry in _harness_members:
        if place == '' and entry['column'] == 'place':
            named = relational_model.named(given[0], entry['pointer'])
            if named['records']:
                place = named['records'][0][4]
    if place == '':
        place = working_directory
    hooks_2_resolve_pathname = os.path.realpath(place, strict=True)
    try:
        answer = _hook_output.context(values, event, hooks_2_resolve_pathname, given[0], relational_model, data_bank)
        _hook_input.insert(values, hooks_2_resolve_pathname, event, hooks_7_read_standard_input, relational_model, data_bank)
    except _hook_output.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _hook_input.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _hook_input.NonConformingError as error:
        raise NonConformingError(str(error))
    if answer != '':
        hooks_8_utf_8_encode = bytes(answer, 'utf-8')
        sys.stdout.buffer.write(hooks_8_utf_8_encode)

class KeepingFailedError(Exception):
    """A data bank that cannot keep or give what it stores MUST end the hook as keeping failed, nothing being written on standard output."""

class NonConformingError(Exception):
    """A hook input that JSON text rejects, or that the converter rejects, MUST end the hook as non-conforming, nothing being written on standard output."""
_harness_members = [{'column': 'place', 'pointer': '/cwd', 'harness': 'Codex'}, {'column': 'place', 'pointer': '/workspace_roots/0', 'harness': 'Cursor'}, {'column': 'agent', 'pointer': '/agent_id', 'harness': 'Claude Code'}, {'column': 'agent', 'pointer': '/agent_id', 'harness': 'Codex'}, {'column': 'agent', 'pointer': '/subagent_id', 'harness': 'Cursor'}, {'column': 'session', 'pointer': '/session_id', 'harness': 'Claude Code'}, {'column': 'session', 'pointer': '/session_id', 'harness': 'Codex'}, {'column': 'session', 'pointer': '/conversation_id', 'harness': 'Cursor'}, {'column': 'turn', 'pointer': '/prompt_id', 'harness': 'Claude Code'}, {'column': 'turn', 'pointer': '/turn_id', 'harness': 'Codex'}, {'column': 'turn', 'pointer': '/generation_id', 'harness': 'Cursor'}, {'column': 'model', 'pointer': '/model', 'harness': 'Claude Code'}, {'column': 'model', 'pointer': '/model', 'harness': 'Codex'}, {'column': 'model', 'pointer': '/model', 'harness': 'Cursor'}]
_harness_variables = [{'column': 'place', 'variable': 'CLAUDE_PROJECT_DIR', 'harness': 'Claude Code'}]
