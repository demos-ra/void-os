"""what a filter expression is, and which records it keeps"""
__all__ = ['kept', 'RefusedError']
import re
from typing import Any

def kept(sheets: list[dict[str, Any,]], filter: str) -> list[dict[str, Any,]]:
    holds = _filter(filter)
    return [{'sheet name': sheet['sheet name'], 'header': sheet['header'], 'records': [record for record in sheet['records'] if holds(record, sheet['records'])]} for sheet in sheets]

class RefusedError(Exception):
    """A filter not written as filter-expression.1 writes it MUST be refused."""

def _equal(left, right):
    if isinstance(left, list) and isinstance(right, list):
        return len(left) == len(right) and all((_equal(first, second) for first, second, in zip(left, right)))
    return isinstance(left, bool) == isinstance(right, bool) and left == right

def _filter(written):
    position = 0

    def logical_expr():
        return logical_or_expr()

    def logical_or_expr():
        operands = [logical_and_expr()]
        while ahead('||'):
            operands.append(logical_and_expr())
        return lambda current, root: any((operand(current, root) for operand in operands))

    def logical_and_expr():
        operands = [basic_expr()]
        while ahead('&&'):
            operands.append(basic_expr())
        return lambda current, root: all((operand(current, root) for operand in operands))

    def basic_expr():
        nonlocal position
        if take('!'):
            blank()
            negated = paren_expr() if at('(') else test_expr()
            return lambda current, root: not negated(current, root)
        if at('('):
            return paren_expr()
        if at('match') or at('search'):
            return test_expr()
        start = position
        left = comparable()
        operator = comparison_op()
        if operator is None:
            position = start
            return test_expr()
        return comparison_expr(left, operator, comparable())

    def paren_expr():
        expect('(')
        blank()
        inner = logical_expr()
        blank()
        expect(')')
        return inner

    def test_expr():
        if at('@') or at('$'):
            query = singular_query()
            return lambda current, root: len(query(current, root)) > 0
        return function_expr()

    def comparison_expr(left, operator, right):
        compare = {'==': _equal, '!=': lambda first, second: not _equal(first, second), '<': _less, '<=': lambda first, second: _less(first, second) or _equal(first, second), '>': lambda first, second: _less(second, first), '>=': lambda first, second: _less(second, first) or _equal(first, second)}[operator]
        return lambda current, root: compare(left(current, root), right(current, root))

    def literal():
        if at('"') or at("'"):
            return string_literal()
        for word, value, in [['true', True], ['false', False], ['null', None]]:
            if take(word):
                return value
        return number()

    def comparable():
        if at('@') or at('$'):
            return singular_query()
        value = literal()
        return lambda current, root: [value]

    def comparison_op():
        for operator in ['==', '!=', '<=', '>=', '<', '>']:
            if ahead(operator):
                return operator
        return None

    def singular_query():
        relative = take('@')
        if not relative:
            expect('$')
        segments = singular_query_segments()
        return lambda current, root: _selected(current if relative else root, segments)

    def singular_query_segments():
        nonlocal position
        segments = []
        while True:
            start = position
            blank()
            if at('.') or at('["') or at("['"):
                segments.append(name_segment())
            elif at('['):
                segments.append(index_segment())
            else:
                position = start
                return segments

    def name_segment():
        nonlocal position
        if take('['):
            string_literal()
            expect(']')
            return lambda value: []
        expect('.')
        start = position
        while written[position:position + 1] != '' and _name_char(written[position], position == start):
            position += 1
        if position == start:
            refuse()
        return lambda value: []

    def index_segment():
        expect('[')
        index = integer()
        if abs(index) > 9007199254740991:
            refuse()
        expect(']')
        return lambda value: [value[index]] if isinstance(value, list) and -len(value) <= index < len(value) else []

    def number():
        start = position
        if not take('-0'):
            integer()
        if take('.'):
            digits()
        if take('e') or take('E'):
            take('-') or take('+')
            digits()
        return float(written[start:position])

    def function_expr():
        nonlocal position
        start = position
        while 'a' <= written[position:position + 1] <= 'z':
            position += 1
        name = written[start:position]
        if name not in ['match', 'search']:
            refuse()
        expect('(')
        blank()
        value = comparable()
        blank()
        expect(',')
        blank()
        pattern = comparable()
        blank()
        expect(')')
        return lambda current, root: _matched(value(current, root), pattern(current, root), name == 'match')

    def string_literal():
        nonlocal position
        quote = written[position]
        position += 1
        characters = []
        while not take(quote):
            if written[position:position + 1] == '' or written[position] < ' ':
                refuse()
            position += 1
            if written[position - 1] != '\\':
                characters.append(written[position - 1])
            elif take('u') and len(written[position:position + 4]) == 4 and all((digit in '0123456789abcdefABCDEF' for digit in written[position:position + 4])):
                position += 4
                characters.append(chr(int(written[position - 4:position], 16)))
            elif written[position:position + 1] in ['b', 'f', 'n', 'r', 't', '/', '\\', quote]:
                position += 1
                characters.append({'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t'}.get(written[position - 1], written[position - 1]))
            else:
                refuse()
        return ''.join(characters)

    def integer():
        start = position
        if not take('0'):
            take('-')
            if not '1' <= written[position:position + 1] <= '9':
                refuse()
            digits()
        return int(written[start:position])

    def digits():
        nonlocal position
        start = position
        while '0' <= written[position:position + 1] <= '9':
            position += 1
        if position == start:
            refuse()

    def blank():
        nonlocal position
        while written[position:position + 1] != '' and written[position] in ' \t\n\r':
            position += 1

    def at(token):
        return written.startswith(token, position)

    def take(token):
        nonlocal position
        if at(token):
            position += len(token)
            return True
        return False

    def ahead(token):
        nonlocal position
        start = position
        blank()
        if take(token):
            blank()
            return True
        position = start
        return False

    def expect(token):
        if not take(token):
            refuse()

    def refuse():
        raise RefusedError('not a filter expression at character ' + str(position + 1) + ': ' + written)
    holds = logical_expr()
    if position < len(written):
        refuse()
    return holds

def _less(left, right):
    if len(left) != 1 or len(right) != 1:
        return False
    if isinstance(left[0], str) and isinstance(right[0], str):
        return left[0] < right[0]
    return _number(left[0]) and _number(right[0]) and left[0] < right[0]

def _matched(value, pattern, whole):
    if len(value) != 1 or len(pattern) != 1 or not isinstance(value[0], str) or not isinstance(pattern[0], str):
        return False
    try:
        return (re.fullmatch if whole else re.search)(pattern[0], value[0]) is not None
    except re.error:
        return False

def _name_char(character, first):
    if character.isascii():
        return character.isalpha() or character == '_' or not first and character.isdigit()
    return not '\ud800' <= character <= '\udfff'

def _number(value):
    return isinstance(value, (int, float,)) and not isinstance(value, bool)

def _selected(node, segments):
    found = [node]
    for segment in segments:
        found = segment(found[0]) if found else []
    return found
