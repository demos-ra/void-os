"""how a JSON text becomes the relations of its instances"""
__all__ = ['instances', 'named', 'NamesNotUniqueError', 'NotAJSONTextError']
from typing import Any

def instances(octets: bytes) -> tuple[dict[str, Any,], dict[str, Any,], list[str],]:
    try:
        json_text_1_utf_8_decode = str(octets, 'utf-8')
    except UnicodeDecodeError:
        raise NotAJSONTextError('not a JSON text: not UTF-8')
    return _json_text(json_text_1_utf_8_decode)

def named(instances: dict[str, Any,], pointer: str) -> dict[str, Any,]:
    return _json_pointer(instances, pointer)

class NamesNotUniqueError(Exception):
    """An object whose names are not all unique MUST end the read as names not unique, its reason the JSON Pointer to the first object, in the order written, that repeats one, in its URI fragment representation."""

class NotAJSONTextError(Exception):
    """JSON text MUST reject what is not a JSON text as not a JSON text."""
_fragment = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$&'()*+,;=:@/?"

def _json_pointer(instances, pointer):
    records = instances['records']
    named = records[:1]
    if pointer and not pointer.startswith('/'):
        named = []
    for token in pointer.split('/')[1:]:
        named = [record for record in records if named and record[1] == named[0][0] and record[2] == '/' + token]
    return {'sheet name': 'instances', 'header': instances['header'], 'records': named}

def _json_text(text):
    position = 0
    instances = []
    runs = []
    not_carried = []
    objects = []

    def json_text():
        ws()
        value('', '', '')
        ws()
        if position < len(text):
            refused()

    def begin_array():
        ws()
        literal('[')
        ws()

    def begin_object():
        ws()
        literal('{')
        ws()

    def end_array():
        ws()
        literal(']')
        ws()

    def end_object():
        ws()
        literal('}')
        ws()

    def name_separator():
        ws()
        literal(':')
        ws()

    def value_separator():
        ws()
        literal(',')
        ws()

    def ws():
        nonlocal position
        while position < len(text) and text[position] in ' \t\n\r':
            position = position + 1

    def value(parent, pointer, place):
        record = [str(len(instances)), parent, pointer, '', '']
        instances.append(record)
        if text.startswith('f', position):
            record[3] = 'boolean'
            record[4] = false()
        elif text.startswith('n', position):
            record[3] = 'null'
            null()
        elif text.startswith('t', position):
            record[3] = 'boolean'
            record[4] = true()
        elif text.startswith('{', position):
            record[3] = 'object'
            object(record[0], place)
        elif text.startswith('[', position):
            record[3] = 'array'
            array(record[0], place)
        elif text.startswith('"', position):
            record[3] = 'string'
            record[4] = carried(string(), record[0], place)
        else:
            record[3] = 'number'
            record[4] = number()

    def false():
        literal('false')
        return 'false'

    def null():
        literal('null')

    def true():
        literal('true')
        return 'true'

    def object(instance, place):
        begin_object()
        names = []
        objects.append([place, names])
        if not text.startswith('}', position):
            member(instance, place, names)
            ws()
            while text.startswith(',', position):
                value_separator()
                member(instance, place, names)
                ws()
        end_object()

    def member(instance, place, names):
        name = string()
        name_separator()
        names.append(name)
        token = _reference_token(name)
        if token != name.replace('~', '~0').replace('/', '~1'):
            not_carried.append(place + '/' + token)
        value(instance, '/' + token, place + '/' + token)

    def array(instance, place):
        begin_array()
        index = 0
        if not text.startswith(']', position):
            value(instance, '/0', place + '/0')
            ws()
            while text.startswith(',', position):
                value_separator()
                index = index + 1
                value(instance, '/' + str(index), place + '/' + str(index))
                ws()
        end_array()

    def number():
        start = position
        if text.startswith('-', position):
            minus()
        int()
        if text.startswith('.', position):
            frac()
        if text.startswith('e', position) or text.startswith('E', position):
            exp()
        return text[start:position]

    def decimal_point():
        literal('.')

    def digit1_9():
        nonlocal position
        if position == len(text) or text[position] not in '123456789':
            refused()
        position = position + 1

    def e():
        nonlocal position
        if position == len(text) or text[position] not in 'eE':
            refused()
        position = position + 1

    def exp():
        e()
        if text.startswith('-', position):
            minus()
        elif text.startswith('+', position):
            plus()
        digits(1)

    def frac():
        decimal_point()
        digits(1)

    def int():
        if text.startswith('0', position):
            zero()
        else:
            digit1_9()
            digits(0)

    def minus():
        literal('-')

    def plus():
        literal('+')

    def zero():
        literal('0')

    def string():
        quotation_mark()
        characters = []
        while not text.startswith('"', position):
            characters.append(char())
        quotation_mark()
        return paired(characters)

    def char():
        nonlocal position
        if not text.startswith('\\', position):
            return unescaped()
        escape()
        character = text[position:position + 1]
        position = position + 1
        if character == 'u':
            return chr(hexadecimal(4))
        if character == '' or character not in '"\\/bfnrt':
            refused()
        return '"\\/\b\f\n\r\t'['"\\/bfnrt'.index(character)]

    def escape():
        literal('\\')

    def quotation_mark():
        literal('"')

    def unescaped():
        nonlocal position
        if position == len(text) or text[position] < ' ' or text[position] in '"\\':
            refused()
        position = position + 1
        return text[position - 1]

    def literal(word):
        nonlocal position
        if not text.startswith(word, position):
            refused()
        position = position + len(word)

    def digits(least):
        nonlocal position
        start = position
        while position < len(text) and text[position] in '0123456789':
            position = position + 1
        if position - start < least:
            refused()

    def hexadecimal(count):
        nonlocal position
        hexdig = text[position:position + count]
        if len(hexdig) < count or not all((character in '0123456789abcdefABCDEF' for character in hexdig)):
            refused()
        position = position + count
        code = 0
        for character in hexdig.lower():
            code = code * 16 + '0123456789abcdef'.index(character)
        return code

    def paired(characters):
        result = []
        for character in characters:
            if result and '\ud800' <= result[-1] <= '\udbff' and '\udc00' <= character <= '\udfff':
                result[-1] = chr(65536 + (ord(result[-1]) - 55296) * 1024 + ord(character) - 56320)
            else:
                result.append(character)
        return ''.join(result)

    def carried(characters, instance, place):
        kept = []
        for index, character, in enumerate(characters):
            if not ('\ud800' <= character <= '\udfff' or character == '\r' and characters[index + 1:index + 2] != '\n'):
                kept.append(character)
        if len(kept) < len(characters):
            not_carried.append(place)
        value = ''.join(kept)
        if '\f' not in value and '\n' not in value and '\t' not in value:
            return value
        for page_number, page, in enumerate(value.split('\f')):
            for line_number, line, in enumerate(page.replace('\r\n', '\n').split('\n')):
                for run_number, run, in enumerate(line.split('\t')):
                    runs.append([instance, str(page_number), str(line_number), str(run_number), run])
        return ''

    def refused():
        raise NotAJSONTextError('not a JSON text: at character ' + str(position + 1))
    json_text()
    for place, names, in objects:
        for index, name, in enumerate(names):
            if name in names[:index]:
                raise NamesNotUniqueError('#' + _percent_encoding(place))
    return {'sheet name': 'instances', 'header': ['_instance', '_parent', '_pointer', '_type', '_value'], 'records': instances}, {'sheet name': 'runs', 'header': ['_instance', '_page', '_line', '_position', '_value'], 'records': runs}, not_carried,

def _percent_encoding(text):
    return ''.join([character if character in _fragment else ''.join(['%' + format(octet, '02X') for octet in bytes(character, 'utf-8')]) for character in text])

def _reference_token(name):
    token = name.replace('~', '~0').replace('/', '~1')
    return ''.join([character for character in token if character not in '\t\n\f\r' and not '\ud800' <= character <= '\udfff'])
