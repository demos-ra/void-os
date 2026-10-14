"""how each record is identified, and how a place within a value is named"""
__all__ = ['keys']
from typing import Any

def keys(records: dict[str, Any,], instances: dict[str, Any,]) -> dict[str, Any,]:
    held = {record[0] + '\n' + record[1]: record for record in instances['records']}
    keyed = []
    for record in records['records']:
        pointer = ''
        instance = record[2]
        if record[3] != '':
            while instance != record[3]:
                pointer = held[record[1] + '\n' + instance][3] + pointer
                instance = held[record[1] + '\n' + instance][2]
        keyed.append([record[0], record[1], record[2], record[3], pointer])
    return {'sheet name': 'keys', 'header': ['location', '_input value', '_instance', '_parent', '_pointer'], 'records': keyed}
