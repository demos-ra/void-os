"""the order of sheets, records and columns"""
__all__ = ['order']
import urllib.parse
from typing import Any

def order(schema: list[dict[str, Any,]], layout: list[dict[str, Any,]]) -> dict[str, Any,]:
    root = _tree(schema[0]['records'], schema[1]['records'])
    visits = {}
    _walk(root, '', visits)
    visits['_instances'] = len(visits)
    visits['_runs'] = len(visits)
    places = []
    for place, relation, in enumerate(sorted(layout[0]['records'], key=lambda record: visits.get(record[0], len(visits)))):
        places.append([relation[0], '', str(place)])
        for position, column, in enumerate(sorted([record for record in layout[1]['records'] if record[0] == relation[0]], key=lambda record: visits.get(record[1], len(visits)))):
            places.append([relation[0], column[1], str(position)])
    return {'sheet name': 'places', 'header': ['location', 'column', 'place'], 'records': places}

def _at(root: Any, location: str) -> Any:
    found = root
    for token in location.split('/')[1:]:
        found = found[int(token)] if isinstance(found, list) else found[_decoded(token)]
    return found

def _decoded(token: str) -> str:
    return token.replace('~1', '/').replace('~0', '~')

def _escaped(name: str) -> str:
    return name.replace('~', '~0').replace('/', '~1')

def _tree(instances: list[list[Any]], runs: list[list[Any]]) -> Any:
    texts = {}
    places = {}
    for record in runs:
        before = places.get(record[0], [0, 0, 0])
        if int(record[1]) > before[0]:
            texts[record[0]] = texts.get(record[0], '') + '\f' * (int(record[1]) - before[0]) + '\n' * int(record[2]) + '\t' * int(record[3])
        elif int(record[2]) > before[1]:
            texts[record[0]] = texts.get(record[0], '') + '\n' * (int(record[2]) - before[1]) + '\t' * int(record[3])
        else:
            texts[record[0]] = texts.get(record[0], '') + '\t' * (int(record[3]) - before[2])
        texts[record[0]] += record[4]
        places[record[0]] = [int(record[1]), int(record[2]), int(record[3])]
    values = {}
    for record in instances:
        values[record[0]] = _typed(record[3], texts.get(record[0], record[4]))
        if isinstance(values.get(record[1]), dict):
            values[record[1]][_decoded(record[2][1:])] = values[record[0]]
        elif isinstance(values.get(record[1]), list):
            values[record[1]].append(values[record[0]])
    return values[instances[0][0]]

def _typed(kind: str, text: str) -> Any:
    if kind == 'object':
        return {}
    if kind == 'array':
        return []
    if kind == 'null':
        return None
    if kind == 'boolean':
        return text == 'true'
    if kind == 'number':
        return float(text)
    return text

def _walk(root: Any, location: str, visits: dict[str, int,]) -> None:
    if location in visits:
        return
    visits[location] = len(visits)
    at = _at(root, location)
    if not isinstance(at, dict):
        return
    if '$ref' in at:
        _walk(root, urllib.parse.unquote(at['$ref'][1:]), visits)
        return
    for keyword in ['properties', 'patternProperties', 'additionalProperties', 'items', 'additionalItems', 'anyOf', 'oneOf', 'if', 'then', 'else', 'dependencies', 'allOf']:
        held = at.get(keyword)
        if isinstance(held, dict) and keyword in ['properties', 'patternProperties', 'dependencies']:
            for name in held:
                _walk(root, location + '/' + keyword + '/' + _escaped(name), visits)
        elif isinstance(held, list):
            for index in range(len(held)):
                _walk(root, location + '/' + keyword + '/' + str(index), visits)
        elif keyword in at:
            _walk(root, location + '/' + keyword, visits)
