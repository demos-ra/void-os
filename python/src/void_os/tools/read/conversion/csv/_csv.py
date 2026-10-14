"""how a CSV file becomes a sheet"""
__all__ = ['load', 'CannotBeRepresentedError']
from typing import Any

def load(octets: bytes) -> tuple[list[dict[str, Any,]], list[str],]:
    try:
        csv_1_utf_8_decode = str(octets, 'utf-8')
    except UnicodeDecodeError:
        raise CannotBeRepresentedError('cannot be represented')
    found = _records(csv_1_utf_8_decode)
    if any((character in field for record in found for field in record for character in '\t\n\f\r')):
        raise CannotBeRepresentedError('cannot be represented')
    return [{'sheet name': '', 'header': found[0] if found else [], 'records': found[1:]}], [],

class CannotBeRepresentedError(Exception):
    """A field that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""

def _records(text: str) -> list[list[str]]:
    found = []
    record = []
    field = ''
    quoted = False
    previous = ''
    for character in text.replace('\r\n', '\n'):
        if character == '"':
            if previous == '"' and not quoted:
                field = field + '"'
            quoted = not quoted
        elif character == ',' and not quoted:
            record.append(field)
            field = ''
        elif character == '\n' and not quoted:
            record.append(field)
            found.append(record)
            record = []
            field = ''
        else:
            field = field + character
        previous = character
    if field or record:
        record.append(field)
        found.append(record)
    return found
