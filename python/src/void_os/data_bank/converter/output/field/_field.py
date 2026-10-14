"""how a value is written as a field's text"""
__all__ = ['fields']
from typing import Any

def fields(cells: dict[str, Any,], input: list[dict[str, Any,]]) -> list[dict[str, Any,]]:
    instances = {record[0] + '\n' + record[1]: record for record in input[0]['records']}
    texts = [record[:4] + [instances[record[1] + '\n' + record[4]][4 if record[3] == '_type' else 5]] for record in cells['records']]
    return [{'sheet name': 'cells', 'header': ['location', '_input value', '_instance', 'column', 'value'], 'records': texts}, input[1]]
