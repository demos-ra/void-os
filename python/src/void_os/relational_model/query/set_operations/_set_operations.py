"""the traditional set operations: the union of a sheet across files or inputs"""
__all__ = ['union']
from typing import Any

def union(sheets: list[dict[str, Any,]], origins: dict[str, Any,], file: dict[str, Any,], lead: str) -> list[dict[str, Any,]]:
    files = {record[0]: record[1] for record in origins['records']}
    sources = {record[0]: record[1] for record in file['records']}
    united = []
    for position, sheet, in enumerate(sheets, 1):
        led = files[str(position)] if lead == 'file' else sources[files[str(position)]]
        header = None if sheet['header'] is None else [lead] + sheet['header']
        found = [each for each in united if each['sheet name'] == sheet['sheet name'] and each['header'] == header]
        if not found:
            found = [{'sheet name': sheet['sheet name'], 'header': header, 'records': []}]
            united.append(found[0])
        found[0]['records'].extend(([led] + record for record in sheet['records']))
    return united
