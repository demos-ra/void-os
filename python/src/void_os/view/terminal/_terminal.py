"""how a level is laid out on a terminal, and when it is written as MTSV instead"""
__all__ = ['lay_out', 'page', 'write']
import os
import subprocess
import sys
import types
import unicodedata
from typing import Any

def lay_out(values: dict[str, Any,], sheets: list[dict[str, Any,]], is_a_terminal: bool, relational_model: types.ModuleType) -> str:
    if not is_a_terminal:
        return relational_model.dumps(sheets)
    gap = dict(values['records'])['column gap']
    text = ''
    for sheet in sheets:
        lines = [[_picture(field) for field in sheet['header']]] + [[_picture(field) for field in record] for record in sheet['records']]
        widths = [max((_width(line[column]) for line in lines)) for column in range(len(sheet['header']))]
        padded = [gap.join((line[column] + ' ' * (widths[column] - _width(line[column])) for column in range(len(line)))) for line in lines]
        text = text + '\f' + _picture(sheet['sheet name']) + '\n\x1b[1m' + padded[0] + '\x1b[0m\n'
        for line in padded[1:]:
            text = text + line + '\n'
    return text

def page(values: dict[str, Any,], text: str, relational_model: types.ModuleType) -> None:
    terminal_7_environment_variable = os.environ.get(dict(values['records'])['pager variable'])
    command = 'more'
    if terminal_7_environment_variable:
        command = terminal_7_environment_variable
    terminal_7_utf_8_encode = bytes(text, 'utf-8')
    subprocess.run(command, shell=True, input=terminal_7_utf_8_encode)

def write(text: str, relational_model: types.ModuleType) -> None:
    terminal_6_utf_8_encode = bytes(text, 'utf-8')
    sys.stdout.buffer.write(terminal_6_utf_8_encode)

def _picture(text: str) -> str:
    return ''.join((chr(9216 + ord(character)) if ord(character) < 32 else chr(9249) if ord(character) == 127 else character for character in text))

def _width(text: str) -> int:
    return sum((2 if unicodedata.east_asian_width(character) in ('W', 'F',) else 1 for character in text))
