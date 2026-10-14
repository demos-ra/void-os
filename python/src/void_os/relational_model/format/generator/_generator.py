"""how sheets become MTSV text"""
__all__ = ['dump', 'dumps', 'CannotBeRepresentedError']
from typing import Any

def dump(sheets: list[dict[str, Any,]]) -> bytes:
    generator_3_utf_8_encode = bytes(dumps(sheets), 'utf-8')
    return generator_3_utf_8_encode

def dumps(sheets: list[dict[str, Any,]]) -> str:
    return _mtsv_file(sheets)

class CannotBeRepresentedError(Exception):
    """The generator MUST raise cannot be represented for a field or sheet name that holds HT, LF, FF or CR, its reason the sheet's position, the record's position and the field's position, joined by a space, the sheet and the field counted from 1, the record 0 for the sheet name, 1 for the header and from 2 for the records."""

def _mtsv_file(sheets):

    def mtsv_file():
        texts = []
        for number, sheet, in enumerate(sheets):
            texts.append(named_sheet(sheet, str(number + 1)))
        return ''.join(texts)

    def named_sheet(sheet, place):
        return ff() + sheet_name(sheet['sheet name'], place + ' 0 1') + eol() + sheet_body(sheet, place)

    def sheet_body(sheet, place):
        if sheet['header'] is None:
            if sheet['records']:
                raise CannotBeRepresentedError('records without a header cannot be represented: ' + place)
            return ''
        texts = [header(sheet['header'], place + ' 1')]
        for number, fields, in enumerate(sheet['records']):
            if len(fields) != len(sheet['header']):
                raise CannotBeRepresentedError('a record must have as many fields as its header: ' + place + ' ' + str(number + 2))
            texts.append(record(fields, place + ' ' + str(number + 2)))
        return ''.join(texts)

    def header(fields, place):
        return record(fields, place)

    def record(fields, place):
        if not fields:
            raise CannotBeRepresentedError('a record must have a field: ' + place)
        texts = []
        for number, value, in enumerate(fields):
            texts.append(field(value, place + ' ' + str(number + 1)))
        return '\t'.join(texts) + eol()

    def field(value, place):
        for character in value:
            if not field_char(character):
                raise CannotBeRepresentedError(place)
        return value

    def sheet_name(value, place):
        return field(value, place)

    def field_char(character):
        return character not in '\t\n\f\r'

    def ff():
        return '\f'

    def eol():
        return '\n'
    return mtsv_file()
