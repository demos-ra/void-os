"""the name and the header of each sheet"""
__all__ = ['sheets']
from typing import Any

def sheets(layout: list[dict[str, Any,]]) -> list[dict[str, Any,]]:
    kinds = {record[0]: record for record in layout[0]['records']}
    places = layout[4]['records']
    names = {}
    relations = []
    for place in sorted([record for record in places if record[1] == ''], key=lambda record: int(record[2])):
        relation = kinds[place[0]]
        parts = [_doubled(record[2]) for record in layout[1]['records'] if record[0] == place[0]]
        if relation[2] in ['instances', 'runs']:
            names[place[0]] = place[0]
        elif relation[2] in ['input values', 'kind']:
            names[place[0]] = '.'.join(parts)
        else:
            names[place[0]] = '.'.join([names[relation[1]]] + parts)
        keys = ['_input value', '_instance', '_page', '_line', '_position'] if relation[2] == 'runs' else ['_input value'] if relation[2] == 'input values' else ['_input value', '_instance', '_parent', '_pointer']
        columns = sorted([record for record in places if record[0] == place[0] and record[1] != ''], key=lambda record: int(record[2]))
        labels = [record[1] if record[1] in ['_type', '_value'] else '.'.join((_doubled(part[3]) for part in layout[3]['records'] if part[0] == place[0] and part[1] == record[1])) for record in columns]
        relations.append({'sheet name': names[place[0]], 'header': keys + labels, 'records': []})
    return relations

def _doubled(name: str) -> str:
    return '_' + name if name.startswith('_') else name
