"""how positions are written, 2, 1;3, 1-3 or 2-*, counted from 1, and which positions a selection names"""
__all__ = ['named', 'written', 'RefusedError']
from typing import Any

def named(written: str, count: int | float) -> dict[str, Any,]:
    return {'sheet name': 'positions', 'header': ['position'], 'records': [[str(found)] for found in _selection(written, count)]}

def written(positions: dict[str, Any,]) -> str:
    return _runs(positions)

class RefusedError(Exception):
    """A selection not written as positions.1 writes it MUST be refused."""

def _runs(positions):
    spans = []
    for record in positions['records']:
        number = int(record[0])
        if spans and spans[-1][1] + 1 == number:
            spans[-1][1] = number
        else:
            spans.append([number, number])
    return ';'.join([str(first) if first == last else str(first) + '-' + str(last) for first, last, in spans])

def _selection(written, count):

    def selection():
        named = []
        for spec in written.split(';'):
            for found in singlespec(spec):
                if found not in named:
                    named.append(found)
        return named

    def singlespec(spec):
        separator = spec.find('-')
        if separator == -1:
            start = position(spec)
            if 1 <= start <= count:
                return [start]
            return []
        start = position(spec[:separator])
        end = position(spec[separator + 1:])
        if start > end:
            return []
        return list(range(max(start, 1), min(end, count) + 1))

    def position(text):
        if text == '*':
            return count
        return number(text)

    def number(text):
        if text == '' or not all((character in '0123456789' for character in text)):
            raise RefusedError('a selection must be written as 2, 1;3, 1-3 or 2-*: ' + written)
        return int(text)
    return selection()
