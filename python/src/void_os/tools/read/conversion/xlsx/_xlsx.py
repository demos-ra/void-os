"""how a workbook becomes sheets"""
__all__ = ['load', 'CannotBeRepresentedError', 'FailedError']
from typing import Any

def load(nodes: dict[str, Any,]) -> tuple[list[dict[str, Any,]], list[str],]:
    found = {}
    for part, node, parent, kind, name, value, in nodes['records']:
        found.setdefault(part + '\t' + parent, []).append([node, kind, name[name.rfind('}') + 1:], value])
    workbook = next((relation[2] for relation in _relations(found, '') if relation[0] == 'officeDocument'))
    targets = _relations(found, workbook)
    shared = []
    for relation in targets:
        if relation[0] == 'sharedStrings':
            shared = [_string(found, relation[2], item) for item in _elements(found, relation[2], _elements(found, relation[2], '', 'sst')[0], 'si')]
    relations = []
    left = []
    for sheet in _elements(found, workbook, _elements(found, workbook, _elements(found, workbook, '', 'workbook')[0], 'sheets')[0], 'sheet'):
        attributes = _attributes(found, workbook, sheet)
        records = _records(found, next((relation[2] for relation in targets if relation[1] == attributes['id'])), shared, left)
        if any((character in field for record in [[attributes['name']]] + records for field in record for character in '\t\n\f\r')):
            raise CannotBeRepresentedError('cannot be represented')
        relations.append({'sheet name': attributes['name'], 'header': records[0] if records else [], 'records': records[1:]})
    return relations, left,

class CannotBeRepresentedError(Exception):
    """A cell's text that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""

class FailedError(Exception):
    """A workbook whose part a relationship it reads names is not among its nodes MUST end the load as failed."""

def _attributes(found: dict[str, list[list[str]],], part: str, node: str) -> dict[str, str,]:
    return dict(([child[2], child[3]] for child in found.get(part + '\t' + node, []) if child[1] == 'attribute'))

def _elements(found: dict[str, list[list[str]],], part: str, node: str, name: str) -> list[str]:
    return [child[0] for child in found.get(part + '\t' + node, []) if child[1] == 'element' and child[2] == name]

def _position(reference: str) -> list[int]:
    column = 0
    line = 0
    for character in reference:
        if character in '0123456789':
            line = line * 10 + int(character)
        else:
            column = column * 26 + ord(character) - 64
    return [column - 1, line - 1]

def _records(found: dict[str, list[list[str]],], part: str, shared: list[str], left: list[str]) -> list[list[str]]:
    records = []
    for data in _elements(found, part, _elements(found, part, '', 'worksheet')[0], 'sheetData'):
        for row in _elements(found, part, data, 'row'):
            for cell in _elements(found, part, row, 'c'):
                attributes = _attributes(found, part, cell)
                position = _position(attributes['r'])
                text = ''.join((_text(found, part, value) for value in _elements(found, part, cell, 'v')))
                if attributes.get('t') == 's':
                    text = shared[int(text)]
                elif attributes.get('t') == 'inlineStr':
                    text = ''.join((_string(found, part, inline) for inline in _elements(found, part, cell, 'is')))
                while len(records) <= position[1]:
                    records.append([])
                while len(records[position[1]]) <= position[0]:
                    records[position[1]].append('')
                records[position[1]][position[0]] = text
                if 't' in attributes:
                    left.append(attributes['r'] + ' t')
                if _elements(found, part, cell, 'f'):
                    left.append(attributes['r'] + ' f')
                if 's' in attributes:
                    left.append(attributes['r'] + ' s')
    return records

def _relations(found: dict[str, list[list[str]],], part: str) -> list[list[str]]:
    place = part[:part.rfind('/') + 1]
    pathname = place + '_rels/' + part[part.rfind('/') + 1:] + '.rels'
    relations = []
    for relationship in _elements(found, pathname, _elements(found, pathname, '', 'Relationships')[0], 'Relationship'):
        attributes = _attributes(found, pathname, relationship)
        target = attributes['Target'][1:] if attributes['Target'].startswith('/') else place + attributes['Target']
        if not any((key.startswith(target + '\t') for key in found)):
            raise FailedError('failed')
        relations.append([attributes['Type'][attributes['Type'].rfind('/') + 1:], attributes['Id'], target])
    return relations

def _string(found: dict[str, list[list[str]],], part: str, node: str) -> str:
    text = ''
    for child in found.get(part + '\t' + node, []):
        if child[1] == 'element' and child[2] == 't':
            text = text + _text(found, part, child[0])
        elif child[1] == 'element' and child[2] == 'r':
            text = text + _string(found, part, child[0])
    return text

def _text(found: dict[str, list[list[str]],], part: str, node: str) -> str:
    return ''.join((child[3] for child in found.get(part + '\t' + node, []) if child[1] == 'text'))
