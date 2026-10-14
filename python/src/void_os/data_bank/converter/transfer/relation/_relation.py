"""which relation and column each value is written to"""
__all__ = ['relations']
import re
import urllib.parse
from typing import Any

def relations(schema: list[dict[str, Any,]], input: list[dict[str, Any,]]) -> list[dict[str, Any,]]:
    root = _tree(schema[0]['records'], schema[1]['records'])
    layout = {'relations': [], 'name parts': [], 'columns': [], 'column parts': [], 'rows': {}, 'molten': False, 'runs': 'string' in _types(root, '')}
    top = _sheet(root, '', '', '', 'input values', _part(root, '', []), layout) if _types(root, '') in [['object'], ['array']] else ['molten']
    if top[0] == 'molten' or layout['molten']:
        _relation('_instances', '', 'instances', [], layout)
        _column('_instances', '_type', ['_type'], layout)
        _column('_instances', '_value', ['_value'], layout)
    if layout['runs']:
        _relation('_runs', '', 'runs', [], layout)
        _column('_runs', '_value', ['_value'], layout)
    rows = layout['rows']
    valid = {record[0] + '\n' + record[1] + '\n' + record[2] for record in input[2]['records'] if record[3] == 'true'}
    records = []
    cells = []
    position = ''
    children = {}

    def place(instance: str, target: list[Any], holder: str) -> None:
        if target[0] == 'record':
            records.append([target[1], position, instance, holder])
            fill(instance, rows[target[1]], target[1])
        elif target[0] == 'elements':
            for each in children.get(instance, []):
                place(each[1], target[1], holder)
        elif target[0] == 'molten':
            melt(instance, holder)
        elif target[0] == 'pick':
            chosen = [each[1] for each in target[1] if position + '\n' + instance + '\n' + each[0] in valid]
            if chosen:
                place(instance, chosen[0], holder)

    def melt(instance: str, holder: str) -> None:
        records.append(['_instances', position, instance, holder])
        cells.append(['_instances', position, instance, '_type', instance])
        cells.append(['_instances', position, instance, '_value', instance])
        for each in children.get(instance, []):
            melt(each[1], instance)

    def fill(instance: str, row: dict[str, Any,], relation: str) -> None:
        if row['kind'] == 'value':
            cells.append([relation, position, instance, '_value', instance])
        elif row['kind'] == 'object':
            write(instance, row, relation, instance)
        else:
            for index, each, in enumerate(children.get(instance, [])):
                target = row['items'] or (row['positions'][index] if index < len(row['positions']) else row['rest'])
                if target:
                    place(each[1], target, instance)

    def write(instance: str, row: dict[str, Any,], relation: str, record: str) -> None:
        writers = [[row, relation, record]] + [[rows[each[1]], each[1], instance] for each in row['branches'] if position + '\n' + instance + '\n' + each[0] in valid]
        for writer in writers[1:]:
            records.append([writer[1], position, instance, ''])
        for name, child, in children.get(instance, []):
            covering = [[rule, writer] for writer in writers for rule in ([writer[0]['members'][name]] if name in writer[0]['members'] else []) + [each[1] for each in writer[0]['patterns'] if re.search(each[0], name)]] + [[writer[0]['additional'], writer] for writer in writers if writer[0]['additional']]
            if covering:
                rule, writer, = covering[0]
                if rule[0] == 'column':
                    cells.append([writer[1], position, writer[2], rule[1], child])
                elif rule[0] == 'inline':
                    write(child, rule[1], writer[1], writer[2])
                else:
                    place(child, rule, writer[2])
            else:
                melt(child, record)
    for position in dict.fromkeys((record[0] for record in input[0]['records'])):
        held = [record for record in input[0]['records'] if record[0] == position]
        children = {}
        for record in held:
            if record[2] != '':
                children.setdefault(record[2], []).append([_decoded(record[3][1:]), record[1]])
        place(held[0][1], top, '')
    for key in dict.fromkeys((record[0] + '\n' + record[1] for record in input[1]['records'])):
        records.append(['_runs'] + key.split('\n') + [''])
    return [{'sheet name': 'relations', 'header': ['location', 'parent', 'kind'], 'records': layout['relations']}, {'sheet name': 'name parts', 'header': ['location', 'position', 'part'], 'records': layout['name parts']}, {'sheet name': 'columns', 'header': ['location', 'column'], 'records': layout['columns']}, {'sheet name': 'column parts', 'header': ['location', 'column', 'position', 'part'], 'records': layout['column parts']}, {'sheet name': 'records', 'header': ['location', '_input value', '_instance', 'holder'], 'records': records}, {'sheet name': 'cells', 'header': ['location', '_input value', '_instance', 'column', 'value'], 'records': cells}]

def _at(root: Any, location: str) -> Any:
    found = root
    for token in location.split('/')[1:]:
        found = found[int(token)] if isinstance(found, list) else found[_decoded(token)]
    return found

def _branch(root: Any, row: dict[str, Any,], relation: str, location: str, parts: list[str], layout: dict[str, Any,]) -> None:
    if _types(root, location) == ['object']:
        target = _sheet(root, location, location, relation, 'branch', parts, layout)
        if target[0] == 'record':
            row['branches'].append([location, target[1]])

def _column(relation: str, column: str, parts: list[str], layout: dict[str, Any,]) -> None:
    layout['columns'].append([relation, column])
    layout['column parts'].extend(([relation, column, str(index), part] for index, part, in enumerate(parts)))

def _decoded(token: str) -> str:
    return token.replace('~1', '/').replace('~0', '~')

def _escaped(name: str) -> str:
    return name.replace('~', '~0').replace('/', '~1')

def _kind(root: Any, location: str, relation: str, layout: dict[str, Any,]) -> list[Any]:
    target = urllib.parse.unquote(_at(root, location)['$ref'][1:])
    if target in layout['rows']:
        for each in layout['relations']:
            if each[0] == target:
                each[2] = 'kind'
        return ['record', target]
    at = _at(root, target)
    name = at['title'] if isinstance(at, dict) and isinstance(at.get('title'), str) else _decoded(target.split('/')[-1])
    return _sheet(root, target, target, relation, 'kind', [name], layout)

def _member(root: Any, relation: str, location: str, required: bool, label: list[str], parts: list[str], kind: str, layout: dict[str, Any,]) -> list[Any]:
    at = _at(root, location)
    if isinstance(at, dict) and '$ref' in at:
        return _kind(root, location, relation, layout)
    types = _types(root, location)
    if 'string' in types:
        layout['runs'] = True
    owns = [own for own in _owns(root, location) if isinstance(_at(root, own), dict)]
    inline = required and types == ['object'] and all((_types(root, own) == ['object'] for own in owns[1:]))
    branches = [[keyword, str(index)] for keyword in ['anyOf', 'oneOf'] if isinstance(at, dict) for index in range(len(at.get(keyword, [])))]
    if branches and (len(types) != 1 or types == ['object'] and not inline and not any((word in _at(root, own) for own in owns for word in ['properties', 'patternProperties', 'additionalProperties']))):
        return ['pick', [[location + '/' + each[0] + '/' + each[1], _member(root, relation, location + '/' + each[0] + '/' + each[1], False, label, parts + [each[0]] + _part(root, location + '/' + each[0] + '/' + each[1], [each[1]] if len(at[each[0]]) > 1 else []), 'branch', layout)] for each in branches]]
    if len(types) == 1 and types[0] in ['string', 'number', 'boolean', 'null']:
        if required:
            _column(relation, location, label, layout)
            return ['column', location]
        layout['molten'] = True
        return ['molten']
    if inline:
        return ['inline', _object(root, relation, location, label, parts, layout)]
    return _target(root, relation, location, kind, parts, layout)

def _object(root: Any, relation: str, location: str, label: list[str], parts: list[str], layout: dict[str, Any,]) -> dict[str, Any,]:
    row = {'kind': 'object', 'members': {}, 'patterns': [], 'additional': None, 'branches': []}
    owns = [own for own in _owns(root, location) if isinstance(_at(root, own), dict)]
    required = [name for own in owns for name in _at(root, own).get('required', [])]
    for own in owns:
        at = _at(root, own)
        for name in at.get('properties', {}):
            if name not in row['members']:
                row['members'][name] = _member(root, relation, own + '/properties/' + _escaped(name), name in required, label + [name], parts + [name], 'property', layout)
        for pattern in at.get('patternProperties', {}):
            row['patterns'].append([pattern, _sheet(root, own + '/patternProperties/' + _escaped(pattern), own + '/patternProperties/' + _escaped(pattern), relation, 'keyword', parts + ['patternProperties'] + ([pattern] if len(at['patternProperties']) > 1 else []), layout)])
        if 'additionalProperties' in at and row['additional'] is None:
            row['additional'] = _sheet(root, own + '/additionalProperties', own + '/additionalProperties', relation, 'keyword', parts + ['additionalProperties'], layout)
        for keyword in ['anyOf', 'oneOf']:
            for index in range(len(at.get(keyword, []))):
                _branch(root, row, relation, own + '/' + keyword + '/' + str(index), parts + [keyword] + _part(root, own + '/' + keyword + '/' + str(index), [str(index)] if len(at[keyword]) > 1 else []), layout)
        for keyword in ['if', 'then', 'else']:
            if keyword in at:
                _branch(root, row, relation, own + '/' + keyword, parts + [keyword] + _part(root, own + '/' + keyword, []), layout)
        for key in at.get('dependencies', {}):
            if not isinstance(at['dependencies'][key], list):
                _branch(root, row, relation, own + '/dependencies/' + _escaped(key), parts + ['dependencies'] + _part(root, own + '/dependencies/' + _escaped(key), [key]), layout)
    if not any(('additionalProperties' in _at(root, own) for own in owns)):
        layout['molten'] = True
        layout['runs'] = True
    return row

def _owns(root: Any, location: str) -> list[str]:
    at = _at(root, location)
    if isinstance(at, dict) and '$ref' in at:
        return _owns(root, urllib.parse.unquote(at['$ref'][1:]))
    return [location] + [own for index in range(len(at.get('allOf', []) if isinstance(at, dict) else [])) for own in _owns(root, location + '/allOf/' + str(index))]

def _part(root: Any, location: str, fallback: list[str]) -> list[str]:
    at = _at(root, location)
    return [at['title']] if isinstance(at, dict) and isinstance(at.get('title'), str) else fallback

def _relation(location: str, parent: str, kind: str, parts: list[str], layout: dict[str, Any,]) -> None:
    layout['relations'].append([location, parent, kind])
    layout['name parts'].extend(([location, str(index), part] for index, part, in enumerate(parts)))

def _row(root: Any, relation: str, location: str, layout: dict[str, Any,]) -> dict[str, Any,]:
    types = _types(root, location)
    at = _at(root, location)
    if types == ['object']:
        return _object(root, relation, location, [], [], layout)
    if types == ['array'] and isinstance(at.get('items'), list):
        return {'kind': 'array', 'items': None, 'positions': [_sheet(root, location + '/items/' + str(index), location + '/items/' + str(index), relation, 'keyword', ['items'] + ([str(index)] if len(at['items']) > 1 else []), layout) for index in range(len(at['items']))], 'rest': _sheet(root, location + '/additionalItems', location + '/additionalItems', relation, 'keyword', ['additionalItems'], layout) if 'additionalItems' in at else None}
    if types == ['array'] and 'items' in at:
        return {'kind': 'array', 'items': _sheet(root, location + '/items', location + '/items', relation, 'keyword', ['items'], layout), 'positions': [], 'rest': None}
    if types == ['array']:
        layout['molten'] = True
        layout['runs'] = True
        return {'kind': 'array', 'items': ['molten'], 'positions': [], 'rest': None}
    _column(relation, '_value', ['_value'], layout)
    return {'kind': 'value'}

def _sheet(root: Any, location: str, schema: str, relation: str, kind: str, parts: list[str], layout: dict[str, Any,]) -> list[Any]:
    if location in layout['rows']:
        return ['record', location]
    at = _at(root, schema)
    if isinstance(at, dict) and '$ref' in at:
        return _kind(root, schema, relation, layout)
    types = _types(root, schema)
    if 'string' in types:
        layout['runs'] = True
    if len(types) > 1:
        layout['molten'] = True
        return ['molten']
    if not types:
        return ['none']
    _relation(location, relation, kind, parts, layout)
    layout['rows'][location] = None
    layout['rows'][location] = _row(root, location, schema, layout)
    return ['record', location]

def _target(root: Any, relation: str, location: str, kind: str, parts: list[str], layout: dict[str, Any,]) -> list[Any]:
    at = _at(root, location)
    if _types(root, location) == ['array'] and isinstance(at, dict) and not isinstance(at.get('items'), list):
        if 'items' in at:
            return ['elements', _sheet(root, location, location + '/items', relation, kind, parts, layout)]
        layout['molten'] = True
        layout['runs'] = True
        return ['elements', ['molten']]
    return _sheet(root, location, location, relation, kind, parts, layout)

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
    if kind == 'number' and re.fullmatch('-?[0-9]+', text):
        return int(text)
    if kind == 'number':
        return float(text)
    return text

def _types(root: Any, location: str) -> list[str]:
    at = _at(root, location)
    if isinstance(at, bool):
        return ['array', 'boolean', 'null', 'number', 'object', 'string'] if at else []
    if '$ref' in at:
        return _types(root, urllib.parse.unquote(at['$ref'][1:]))
    named = at['type'] if isinstance(at.get('type'), list) else [at['type']] if 'type' in at else ['array', 'boolean', 'null', 'number', 'object', 'string']
    types = [each for each in ['array', 'boolean', 'null', 'number', 'object', 'string'] if each in named or each == 'number' and 'integer' in named]
    for index in range(len(at.get('allOf', []))):
        types = [each for each in types if each in _types(root, location + '/allOf/' + str(index))]
    for keyword in ['anyOf', 'oneOf']:
        if keyword in at:
            types = [each for each in types if any((each in _types(root, location + '/' + keyword + '/' + str(index)) for index in range(len(at[keyword]))))]
    return types
