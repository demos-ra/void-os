"""how a spreadsheet document becomes sheets"""
__all__ = ['load', 'CannotBeRepresentedError', 'FailedError']
from typing import Any

def load(nodes: dict[str, Any,]) -> tuple[list[dict[str, Any,]], list[str],]:
    found = {}
    for part, node, parent, kind, name, value, in nodes['records']:
        if part == 'content.xml':
            found.setdefault(parent, []).append([node, kind, name[name.rfind('}') + 1:], value])
    if not found:
        raise FailedError('failed')
    relations = []
    left = []
    for body in _elements(found, _elements(found, '', 'document-content')[0], 'body'):
        if not _elements(found, body, 'spreadsheet'):
            raise FailedError('failed')
        for spreadsheet in _elements(found, body, 'spreadsheet'):
            for table in _elements(found, spreadsheet, 'table'):
                title = _attributes(found, table)['name']
                records = _records(found, table, left)
                if any((character in field for record in [[title]] + records for field in record for character in '\t\n\f\r')):
                    raise CannotBeRepresentedError('cannot be represented')
                relations.append({'sheet name': title, 'header': records[0] if records else [], 'records': records[1:]})
    return relations, left,

class CannotBeRepresentedError(Exception):
    """A cell's text that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""

class FailedError(Exception):
    """A spreadsheet document whose nodes hold no part content.xml, or whose body holds no office:spreadsheet, MUST end the load as failed."""

def _attributes(found: dict[str, list[list[str]],], node: str) -> dict[str, str,]:
    return dict(([child[2], child[3]] for child in found.get(node, []) if child[1] == 'attribute'))

def _elements(found: dict[str, list[list[str]],], node: str, name: str) -> list[str]:
    return [child[0] for child in found.get(node, []) if child[1] == 'element' and child[2] == name]

def _paragraph(found: dict[str, list[list[str]],], node: str) -> str:
    text = ''
    for child in found.get(node, []):
        if child[1] == 'text':
            text = text + child[3]
        elif child[1] == 'element' and child[2] == 's':
            text = text + ' ' * int(_attributes(found, child[0]).get('c', '1'))
        elif child[1] == 'element' and child[2] == 'tab':
            text = text + '\t'
        elif child[1] == 'element' and child[2] == 'line-break':
            text = text + '\n'
        elif child[1] == 'element':
            text = text + _paragraph(found, child[0])
    return text

def _records(found: dict[str, list[list[str]],], table: str, left: list[str]) -> list[list[str]]:
    records = []
    line = 0
    for row in _rows(found, table):
        cells = []
        for cell in found.get(row, []):
            if cell[1] == 'element' and cell[2] in ['table-cell', 'covered-table-cell']:
                attributes = _attributes(found, cell[0])
                cells.append([int(attributes.get('number-columns-repeated', '1')), '\n'.join((_paragraph(found, item) for item in _elements(found, cell[0], 'p'))), [label for label in ['office:value-type', 'office:value', 'office:date-value', 'office:time-value', 'office:boolean-value', 'office:string-value', 'table:formula', 'table:style-name'] if label[label.find(':') + 1:] in attributes]])
        repeated = int(_attributes(found, row).get('number-rows-repeated', '1'))
        if all((entry[1] == '' and not entry[2] for entry in cells)):
            line = line + repeated
        else:
            last = line + repeated
            while line < last:
                record = []
                column = 0
                for count, text, labels, in cells:
                    if text == '' and not labels:
                        column = column + count
                    else:
                        stop = column + count
                        while column < stop:
                            while len(record) < column:
                                record.append('')
                            record.append(text)
                            left.extend((_reference(column, line) + ' ' + label for label in labels))
                            column = column + 1
                while len(records) < line:
                    records.append([])
                records.append(record)
                line = line + 1
    return records

def _reference(column: int, line: int) -> str:
    letters = ''
    number = column + 1
    while number > 0:
        letters = chr(65 + (number - 1) % 26) + letters
        number = (number - 1) // 26
    return letters + str(line + 1)

def _rows(found: dict[str, list[list[str]],], node: str) -> list[str]:
    rows = []
    for child in found.get(node, []):
        if child[1] == 'element' and child[2] == 'table-row':
            rows.append(child[0])
        elif child[1] == 'element' and child[2] in ['table-header-rows', 'table-rows', 'table-row-group']:
            rows.extend(_rows(found, child[0]))
    return rows
