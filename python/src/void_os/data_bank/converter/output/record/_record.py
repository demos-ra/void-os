"""each instance as one record of its sheet"""
__all__ = ['records']
from typing import Any

def records(transferred: list[dict[str, Any,]]) -> list[dict[str, Any,]]:
    cells = {record[0] + '\n' + record[1] + '\n' + record[2] + '\n' + record[3]: record[4] for record in transferred[1]['records']}
    keys = {record[0] + '\n' + record[1] + '\n' + record[2]: record for record in transferred[2]['records']}
    places = transferred[3]['records']
    relations = []
    for place in sorted([record for record in places if record[1] == '' and record[0] != '_runs'], key=lambda record: int(record[2])):
        columns = [record[1] for record in sorted([record for record in places if record[0] == place[0] and record[1] != ''], key=lambda record: int(record[2]))]
        held = [record for record in transferred[0]['records'] if record[0] == place[0]]
        alone = place[0] == '' and all((record[3] == '' for record in held))
        rows = []
        for record in held:
            key = keys[record[0] + '\n' + record[1] + '\n' + record[2]]
            rows.append(([record[1]] if alone else [record[1], record[2], key[3], key[4]]) + [cells.get(record[0] + '\n' + record[1] + '\n' + record[2] + '\n' + column, '') for column in columns])
        relations.append({'sheet name': place[0], 'header': (['_input value'] if alone else ['_input value', '_instance', '_parent', '_pointer']) + columns, 'records': rows})
    return relations
