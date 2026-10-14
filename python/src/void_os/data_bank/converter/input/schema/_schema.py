"""what a module specification supplies, and how its schema is read and applied"""
__all__ = ['schema', 'validate', 'NonConformingError']
import re
import types
import urllib.parse
from typing import Any

def schema(module_specification: bytes, relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        found = relational_model.instances(module_specification)
    except relational_model.NotAJSONTextError as error:
        raise NonConformingError('module specification: ' + str(error))
    except relational_model.NamesNotUniqueError as error:
        raise NonConformingError('module specification: ' + str(error))
    root = _tree(found[0]['records'], found[1]['records'])
    meta = relational_model.instances(bytes(_metaschema(), 'utf-8'))
    applied = _applied(_tree(meta[0]['records'], meta[1]['records'])[0], root)
    if not applied[0]:
        raise NonConformingError('module specification: not a draft-07 schema, at "' + applied[2] + '"')
    _rules(root[0])
    return [found[0], found[1]]

def validate(schema: list[dict[str, Any,]], values: list[dict[str, Any,]], relational_model: types.ModuleType) -> dict[str, Any,]:
    root = _tree(schema[0]['records'], schema[1]['records'])
    annotations = []
    for position in dict.fromkeys((record[0] for record in values[0]['records'])):
        applied = _applied(root[0], _tree([record[1:] for record in values[0]['records'] if record[0] == position], [record[1:] for record in values[1]['records'] if record[0] == position]))
        if not applied[0]:
            raise NonConformingError(position + ' ' + '#' + _percent_encoding(applied[2]))
        annotations.extend(([position, instance, location, 'true' if valid else 'false'] for instance, location, valid, in applied[1]))
    return {'sheet name': 'annotations', 'header': ['_input value', '_instance', 'location', 'valid'], 'records': annotations}

class NonConformingError(Exception):
    """The access program validate MUST give, for each instance of each input value, each subschema applied to it and whether the instance is valid against it, and reject an input value that fails an assertion as non-conforming, its reason the value's position, a space, and the JSON Pointer to the deepest instance location where it fails, in its URI fragment representation.

A module specification that breaks schema.1 or schema.3-8 MUST be rejected as non-conforming."""

def _applied(schema: Any, tree: tuple[Any, dict[str, Any,],]) -> tuple[bool, list[list[Any]], str,]:
    applied = []
    failing = []

    def valid(at: Any, location: str, instance: Any, path: str) -> bool:
        if isinstance(at, bool):
            result = at
        elif '$ref' in at:
            pointer = urllib.parse.unquote(at['$ref'][1:])
            result = valid(_resolved(schema, pointer), pointer, instance, path)
        else:
            kind = _kind(instance)
            result = True
            named = at['type'] if isinstance(at.get('type'), list) else [at['type']] if 'type' in at else []
            if named and kind not in named and not ('integer' in named and kind == 'number' and instance == int(instance)):
                result = False
            if 'enum' in at and not any((_equal(instance, each) for each in at['enum'])):
                result = False
            if 'const' in at and not _equal(instance, at['const']):
                result = False
            if 'multipleOf' in at and kind == 'number' and instance / at['multipleOf'] != int(instance / at['multipleOf']):
                result = False
            if 'maximum' in at and kind == 'number' and instance > at['maximum']:
                result = False
            if 'exclusiveMaximum' in at and kind == 'number' and instance >= at['exclusiveMaximum']:
                result = False
            if 'minimum' in at and kind == 'number' and instance < at['minimum']:
                result = False
            if 'exclusiveMinimum' in at and kind == 'number' and instance <= at['exclusiveMinimum']:
                result = False
            if 'maxLength' in at and kind == 'string' and len(instance) > at['maxLength']:
                result = False
            if 'minLength' in at and kind == 'string' and len(instance) < at['minLength']:
                result = False
            if 'pattern' in at and kind == 'string' and not re.search(at['pattern'], instance):
                result = False
            if isinstance(at.get('items'), list) and kind == 'array' and not all([valid(each, location + '/items/' + str(index), instance[index], path + '/' + str(index)) for index, each, in enumerate(at['items']) if index < len(instance)]):
                result = False
            if 'items' in at and not isinstance(at['items'], list) and kind == 'array' and not all([valid(at['items'], location + '/items', each, path + '/' + str(index)) for index, each, in enumerate(instance)]):
                result = False
            if 'additionalItems' in at and isinstance(at.get('items'), list) and kind == 'array' and not all([valid(at['additionalItems'], location + '/additionalItems', each, path + '/' + str(index)) for index, each, in enumerate(instance) if index >= len(at['items'])]):
                result = False
            if 'maxItems' in at and kind == 'array' and len(instance) > at['maxItems']:
                result = False
            if 'minItems' in at and kind == 'array' and len(instance) < at['minItems']:
                result = False
            if at.get('uniqueItems') is True and kind == 'array' and any((_equal(instance[index], instance[other]) for index in range(len(instance)) for other in range(index))):
                result = False
            if 'contains' in at and kind == 'array' and not any([valid(at['contains'], location + '/contains', each, path + '/' + str(index)) for index, each, in enumerate(instance)]):
                result = False
            if 'maxProperties' in at and kind == 'object' and len(instance) > at['maxProperties']:
                result = False
            if 'minProperties' in at and kind == 'object' and len(instance) < at['minProperties']:
                result = False
            if 'required' in at and kind == 'object' and not all((name in instance for name in at['required'])):
                result = False
            if 'properties' in at and kind == 'object' and not all([valid(at['properties'][name], location + '/properties/' + _escaped(name), instance[name], path + '/' + _escaped(name)) for name in at['properties'] if name in instance]):
                result = False
            if 'patternProperties' in at and kind == 'object' and not all([valid(at['patternProperties'][pattern], location + '/patternProperties/' + _escaped(pattern), instance[name], path + '/' + _escaped(name)) for pattern in at['patternProperties'] for name in instance if re.search(pattern, name)]):
                result = False
            if 'additionalProperties' in at and kind == 'object' and not all([valid(at['additionalProperties'], location + '/additionalProperties', instance[name], path + '/' + _escaped(name)) for name in instance if name not in at.get('properties', {}) and not any((re.search(pattern, name) for pattern in at.get('patternProperties', {})))]):
                result = False
            if 'dependencies' in at and kind == 'object' and not all([all((other in instance for other in at['dependencies'][name])) if isinstance(at['dependencies'][name], list) else valid(at['dependencies'][name], location + '/dependencies/' + _escaped(name), instance, path) for name in at['dependencies'] if name in instance]):
                result = False
            if 'propertyNames' in at and kind == 'object' and not all([valid(at['propertyNames'], location + '/propertyNames', name, path) for name in instance]):
                result = False
            condition = valid(at['if'], location + '/if', instance, path) if 'if' in at else None
            if 'then' in at and condition is True and not valid(at['then'], location + '/then', instance, path):
                result = False
            if 'else' in at and condition is False and not valid(at['else'], location + '/else', instance, path):
                result = False
            if 'allOf' in at and not all([valid(each, location + '/allOf/' + str(index), instance, path) for index, each, in enumerate(at['allOf'])]):
                result = False
            if 'anyOf' in at and not any([valid(each, location + '/anyOf/' + str(index), instance, path) for index, each, in enumerate(at['anyOf'])]):
                result = False
            if 'oneOf' in at and [valid(each, location + '/oneOf/' + str(index), instance, path) for index, each, in enumerate(at['oneOf'])].count(True) != 1:
                result = False
            if 'not' in at and valid(at['not'], location + '/not', instance, path):
                result = False
        applied.append([tree[1][path], location, result])
        if not result:
            failing.append(path)
        return result
    result = valid(schema, '', tree[0], '')
    deepest = ''
    for path in failing:
        if path.count('/') > deepest.count('/'):
            deepest = path
    return result, applied, deepest,

def _decoded(token: str) -> str:
    return token.replace('~1', '/').replace('~0', '~')

def _equal(left: Any, right: Any) -> bool:
    if _kind(left) != _kind(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all((_equal(each, right[index]) for index, each, in enumerate(left)))
    if isinstance(left, dict):
        return sorted(left) == sorted(right) and all((_equal(left[name], right[name]) for name in left))
    return left == right

def _escaped(name: str) -> str:
    return name.replace('~', '~0').replace('/', '~1')
_fragment = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$&'()*+,;=:@/?"

def _kind(instance: Any) -> str:
    if instance is None:
        return 'null'
    if isinstance(instance, bool):
        return 'boolean'
    if isinstance(instance, dict):
        return 'object'
    if isinstance(instance, list):
        return 'array'
    if isinstance(instance, str):
        return 'string'
    return 'number'

def _limited(pattern: str) -> bool:
    depth = 0
    index = 0
    quantifiable = False
    while index < len(pattern):
        character = pattern[index]
        if character == '\\' and not re.fullmatch('[^0-9A-Za-z]', pattern[index + 1:index + 2]):
            return False
        if character == '\\':
            index += 2
            quantifiable = True
        elif character == '[':
            found = re.match('\\[\\^?(\\\\[^0-9A-Za-z]|[^\\\\\\]])+\\]', pattern[index:])
            if not found:
                return False
            index += len(found.group(0))
            quantifiable = True
        elif character == '(':
            if pattern[index + 1:index + 2] == '?':
                return False
            depth += 1
            index += 1
            quantifiable = False
        elif character == ')':
            depth -= 1
            if depth < 0:
                return False
            index += 1
            quantifiable = True
        elif character in '+*?{':
            found = re.match('([+*?]|\\{[0-9]+(,[0-9]*)?\\})\\??', pattern[index:])
            if not found or not quantifiable:
                return False
            index += len(found.group(0))
            quantifiable = False
        elif character in '|^$':
            index += 1
            quantifiable = False
        elif character in '.]}':
            return False
        else:
            index += 1
            quantifiable = True
    try:
        re.compile(pattern)
    except re.error:
        return False
    return depth == 0

def _loops(root: Any, location: str, seen: list[str]) -> bool:
    if location in seen:
        return True
    at = _resolved(root, location)
    if not isinstance(at, dict):
        return False
    if '$ref' in at:
        return _loops(root, urllib.parse.unquote(at['$ref'][1:]), seen + [location])
    places = [location + '/' + name + '/' + str(index) for name in ['allOf', 'anyOf', 'oneOf'] for index in range(len(at.get(name, [])))] + [location + '/' + name for name in ['not', 'if', 'then', 'else'] if name in at] + [location + '/dependencies/' + _escaped(name) for name in at.get('dependencies', {}) if not isinstance(at['dependencies'][name], list)]
    return any((_loops(root, place, seen + [location]) for place in places))

def _metaschema() -> str:
    return '{"$schema":"http://json-schema.org/draft-07/schema#","$id":"http://json-schema.org/draft-07/schema#","title":"Core schema meta-schema","definitions":{"schemaArray":{"type":"array","minItems":1,"items":{"$ref":"#"}},"nonNegativeInteger":{"type":"integer","minimum":0},"nonNegativeIntegerDefault0":{"allOf":[{"$ref":"#/definitions/nonNegativeInteger"},{"default":0}]},"simpleTypes":{"enum":["array","boolean","integer","null","number","object","string"]},"stringArray":{"type":"array","items":{"type":"string"},"uniqueItems":true,"default":[]}},"type":["object","boolean"],"properties":{"$id":{"type":"string","format":"uri-reference"},"$schema":{"type":"string","format":"uri"},"$ref":{"type":"string","format":"uri-reference"},"$comment":{"type":"string"},"title":{"type":"string"},"description":{"type":"string"},"default":true,"readOnly":{"type":"boolean","default":false},"writeOnly":{"type":"boolean","default":false},"examples":{"type":"array","items":true},"multipleOf":{"type":"number","exclusiveMinimum":0},"maximum":{"type":"number"},"exclusiveMaximum":{"type":"number"},"minimum":{"type":"number"},"exclusiveMinimum":{"type":"number"},"maxLength":{"$ref":"#/definitions/nonNegativeInteger"},"minLength":{"$ref":"#/definitions/nonNegativeIntegerDefault0"},"pattern":{"type":"string","format":"regex"},"additionalItems":{"$ref":"#"},"items":{"anyOf":[{"$ref":"#"},{"$ref":"#/definitions/schemaArray"}],"default":true},"maxItems":{"$ref":"#/definitions/nonNegativeInteger"},"minItems":{"$ref":"#/definitions/nonNegativeIntegerDefault0"},"uniqueItems":{"type":"boolean","default":false},"contains":{"$ref":"#"},"maxProperties":{"$ref":"#/definitions/nonNegativeInteger"},"minProperties":{"$ref":"#/definitions/nonNegativeIntegerDefault0"},"required":{"$ref":"#/definitions/stringArray"},"additionalProperties":{"$ref":"#"},"definitions":{"type":"object","additionalProperties":{"$ref":"#"},"default":{}},"properties":{"type":"object","additionalProperties":{"$ref":"#"},"default":{}},"patternProperties":{"type":"object","additionalProperties":{"$ref":"#"},"propertyNames":{"format":"regex"},"default":{}},"dependencies":{"type":"object","additionalProperties":{"anyOf":[{"$ref":"#"},{"$ref":"#/definitions/stringArray"}]}},"propertyNames":{"$ref":"#"},"const":true,"enum":{"type":"array","items":true,"minItems":1,"uniqueItems":true},"type":{"anyOf":[{"$ref":"#/definitions/simpleTypes"},{"type":"array","items":{"$ref":"#/definitions/simpleTypes"},"minItems":1,"uniqueItems":true}]},"format":{"type":"string"},"contentMediaType":{"type":"string"},"contentEncoding":{"type":"string"},"if":{"$ref":"#"},"then":{"$ref":"#"},"else":{"$ref":"#"},"allOf":{"$ref":"#/definitions/schemaArray"},"anyOf":{"$ref":"#/definitions/schemaArray"},"oneOf":{"$ref":"#/definitions/schemaArray"},"not":{"$ref":"#"}},"default":true}'

def _percent_encoding(text):
    return ''.join([character if character in _fragment else ''.join(['%' + format(octet, '02X') for octet in bytes(character, 'utf-8')]) for character in text])

def _resolved(root: Any, pointer: str) -> Any:
    found = root
    for token in pointer.split('/')[1:]:
        found = found[int(token)] if isinstance(found, list) else found[_decoded(token)]
    return found

def _rules(root: Any) -> None:
    if not isinstance(root, dict) or not isinstance(root.get('title'), str):
        raise NonConformingError('module specification: the root schema holds no title')
    schemas = _schemas(root, '')
    places = [place for place, at, in schemas]
    for location, at, in schemas:
        if '$ref' in at and not at['$ref'].startswith('#'):
            raise NonConformingError('module specification: a $ref outside it, at "' + location + '"')
        if '$ref' in at and not re.fullmatch("#(/([A-Za-z0-9\\-._~!$&'()*+,;=:@/?]|%[0-9A-Fa-f]{2})*)?", at['$ref']):
            raise NonConformingError('module specification: a $ref fragment not a JSON Pointer, at "' + location + '"')
        if '$ref' in at and urllib.parse.unquote(at['$ref'][1:]) not in places:
            raise NonConformingError('module specification: a $ref to no schema of it, at "' + location + '"')
        names = [at.get('title', '')] + list(at.get('properties', {})) + list(at.get('patternProperties', {})) + list(at.get('dependencies', {})) + [_decoded(urllib.parse.unquote(at.get('$ref', '')).split('/')[-1])]
        if any((re.search('[\t\n\f\r]', name) for name in names)):
            raise NonConformingError('module specification: a name holds HT, LF, FF or CR, at "' + location + '"')
        if not all((_limited(pattern) for pattern in list(at.get('patternProperties', {})) + [at.get('pattern', '')])):
            raise NonConformingError('module specification: a pattern outside the limited syntax, at "' + location + '"')
    for location, at, in schemas:
        if _loops(root, location, []):
            raise NonConformingError('module specification: a $ref reaches again a schema it is applied from, at "' + location + '"')

def _schemas(at: Any, location: str) -> list[tuple[str, Any,]]:
    if not isinstance(at, dict):
        return []
    found = [(location, at,)]
    for name in ['additionalItems', 'additionalProperties', 'contains', 'else', 'if', 'items', 'not', 'propertyNames', 'then']:
        found += _schemas(at.get(name), location + '/' + name)
    for name in ['allOf', 'anyOf', 'items', 'oneOf']:
        found += [place for index, each, in enumerate(at.get(name) if isinstance(at.get(name), list) else []) for place in _schemas(each, location + '/' + name + '/' + str(index))]
    for name in ['definitions', 'dependencies', 'patternProperties', 'properties']:
        found += [place for key in at.get(name, {}) for place in _schemas(at[name][key], location + '/' + name + '/' + _escaped(key))]
    return found

def _tree(instances: list[list[Any]], runs: list[list[Any]]) -> tuple[Any, dict[str, Any,],]:
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
    paths = {}
    ids = {}
    for record in instances:
        values[record[0]] = _typed(record[3], texts.get(record[0], record[4]))
        paths[record[0]] = paths.get(record[1], '') + record[2]
        ids[paths[record[0]]] = record[0]
        if isinstance(values.get(record[1]), dict):
            values[record[1]][_decoded(record[2][1:])] = values[record[0]]
        elif isinstance(values.get(record[1]), list):
            values[record[1]].append(values[record[0]])
    return values[instances[0][0]], ids,

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
