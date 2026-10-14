"""how MTSV text becomes sheets"""
__all__ = ['load', 'loads', 'NotMTSVError']
from typing import Any

def load(octets: bytes) -> list[dict[str, Any,]]:
    try:
        parser_4_utf_8_decode = str(octets, 'utf-8')
    except UnicodeDecodeError as error:
        prefix = str(octets[:error.start], 'utf-8')
        raise NotMTSVError(_where(prefix, len(prefix)))
    return loads(parser_4_utf_8_decode)

def loads(text: str) -> list[dict[str, Any,]]:
    return _mtsv_file(text)

class NotMTSVError(Exception):
    """The parser MUST raise not MTSV for text that does not conform, its reason the number of the line where it stops conforming, counted from 1."""

def _mtsv_file(text):
    position = 0
    if text.startswith('\ufeff'):
        position = 1

    def mtsv_file():
        sheets = []
        if position < len(text) and not ff():
            sheets.append(first_sheet())
        while ff():
            sheets.append(named_sheet())
        return sheets

    def first_sheet():
        return sheet_body('')

    def named_sheet():
        nonlocal position
        position = position + 1
        name = sheet_name()
        eol()
        return sheet_body(name)

    def sheet_body(name):
        if position == len(text) or ff():
            return {'sheet name': name, 'header': None, 'records': []}
        fields = header()
        records = []
        while position < len(text) and not ff():
            start = position
            values = record()
            if len(values) != len(fields):
                raise NotMTSVError(_where(text, start))
            records.append(values)
        return {'sheet name': name, 'header': fields, 'records': records}

    def header():
        return record()

    def record():
        nonlocal position
        fields = [field()]
        while text.startswith('\t', position):
            position = position + 1
            fields.append(field())
        eol()
        return fields

    def field():
        nonlocal position
        start = position
        while position < len(text) and field_char(text[position]):
            position = position + 1
        return text[start:position]

    def sheet_name():
        return field()

    def field_char(character):
        return character not in '\t\n\f\r'

    def ff():
        return text.startswith('\f', position)

    def eol():
        nonlocal position
        if text.startswith('\n', position):
            position = position + 1
        elif text.startswith('\r\n', position):
            position = position + 2
        else:
            raise NotMTSVError(_where(text, position))
    return mtsv_file()

def _where(text, position):
    return str(text.count('\n', 0, position) + 1)
