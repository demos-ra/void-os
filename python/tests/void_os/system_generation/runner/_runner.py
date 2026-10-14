"""how a conformance case is run: found by its key, its fixtures placed, its access program called, and what it asserts compared"""
__all__ = ['run', 'NoCaseError', 'NotMTSVError']
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import types
import zlib
from typing import Any

def run(values: dict[str, Any,], requirement: str, case: int | float, folder: str, root: types.ModuleType, relational_model: types.ModuleType) -> list[str]:
    try:
        key = [requirement, str(case)]
        repository = os.path.dirname(folder)
        found = _found(folder, relational_model)
        held = [entry for entry in found if key in [record[:2] for record in _sheet(entry[1], 'cases')]]
        if not held:
            raise NoCaseError('no case')
        sheets = held[0][1]
        place = os.path.dirname(held[0][0]) + os.sep
        above = [entry for entry in found if place.startswith(os.path.dirname(entry[0]) + os.sep)]
        record = _rows(sheets, 'cases', key)[0]
        made = os.path.join(tempfile.gettempdir(), 'void-os-' + requirement + '-' + str(case) + '-' + str(time.time_ns()))
        os.makedirs(os.path.join(made, 'home'), exist_ok=True)
        runner_2_resolve_pathname = os.path.realpath(made, strict=True)
        runner_2_environment_variable_names = list(os.environ)
        for name in runner_2_environment_variable_names:
            if name not in ['PATH', 'SYSTEMROOT']:
                os.environ.pop(name, None)
        runner_6_platform = sys.platform
        os.environ['TZ'] = 'UTC0'
        os.environ['USERPROFILE' if runner_6_platform == 'win32' else 'HOME'] = os.path.join(runner_2_resolve_pathname, 'home')
        for row in _rows(sheets, 'environment', key):
            os.environ[row[0]] = _value(row[1], runner_2_resolve_pathname, repository)
        given = _placed(sheets, key, above, runner_2_resolve_pathname, repository, relational_model)
        books = _books(relational_model)
        starts = [record[0], record[1]] in [row[:2] for row in _sheet(books, 'Access programs') if row[2] != '']
        outcome = [None, None, b'', b'']
        if record[0] != '' and starts:
            outcome = _command(sheets, key, record, books, runner_2_resolve_pathname, repository)
        if record[0] != '' and not starts:
            outcome = _call(values, sheets, key, record, given, books, root, runner_2_resolve_pathname, repository)
        return _compared(sheets, key, record, outcome, above, runner_2_resolve_pathname, repository, books, relational_model)
    except relational_model.NotMTSVError as error:
        raise NotMTSVError(str(error))

class NoCaseError(Exception):
    """A requirement and case that name no case MUST end run as no case."""

class NotMTSVError(Exception):
    """A file of conformance the parser rejects MUST end run as not MTSV."""

def _after(pathname: str, results: list[Any], outcome: list[Any], pwd: str, repository: str, relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    if pathname.startswith('result '):
        held = results[int(pathname[7:]) - 1]
        return [held] if isinstance(held, dict) else held
    if pathname == '-':
        return relational_model.load(outcome[2])
    return relational_model.load(_bytes(_path(pathname, pwd, repository)))

def _beside(name: str, above: list[list[Any]]) -> str:
    return [os.path.join(os.path.dirname(entry[0]), name) for entry in above if name in [row[3] for row in _sheet(entry[1], 'octets') + _sheet(entry[1], 'expected files')]][-1]

def _books(relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    folder = os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..', 'spec')
    return [sheet for name in sorted(os.listdir(folder)) if name.endswith('.mtsv') for sheet in relational_model.load(_bytes(os.path.join(folder, name)))]

def _bytes(pathname: str) -> bytes:
    with open(pathname, 'rb') as file:
        runner_1_read_a_file = file.read()
    return runner_1_read_a_file

def _call(values: dict[str, Any,], sheets: list[dict[str, Any,]], key: list[str], record: list[str], given: dict[str, Any,], books: list[dict[str, Any,]], root: types.ModuleType, pwd: str, repository: str) -> list[Any]:
    arguments = []
    for row in _rows(books, 'Parameters', record[:2]):
        items = [argument[1:] for argument in _rows(sheets, 'arguments', key) if argument[0] == row[0]]
        if row[0] in given:
            arguments.append(given[row[0]] if row[2] == 'relations' else given[row[0]][0])
        if row[0] not in given and row[3] == 'Values':
            arguments.append(values)
        if row[0] not in given and row[3] != 'Values':
            arguments.append(_read(items, row[2], books, root, pwd, repository))
    for row in _sheet(books, 'Compositions'):
        if row[1] == record[0]:
            arguments.append(_reached(row[2], books, root))
    try:
        return [getattr(_reached(record[0], books, root), _snake(record[1]))(*arguments), None, b'', b'']
    except Exception as error:
        return [None, error, b'', b'']

def _command(sheets: list[dict[str, Any,]], key: list[str], record: list[str], books: list[dict[str, Any,]], pwd: str, repository: str) -> list[Any]:
    parts = [row[0] for row in _sheet(books, 'Files') if row[1] == record[0] and row[0].startswith('python/')][0][:-3].split('/')
    code = 'import sys\nsys.path.insert(0, ' + repr(os.path.join(repository, parts[0], parts[1])) + ')\nfrom ' + '.'.join(parts[2:]) + ' import ' + _snake(record[1]) + '\nsys.exit(' + _snake(record[1]) + '())\n'
    runner_11_interpreter = sys.executable
    runner_11_utf_8_encode = bytes(''.join([_value(row[1], pwd, repository) + '\n' for row in _rows(sheets, 'stdin', key)]), 'utf-8')
    runner_11_run_a_command = (lambda child: [child.returncode, child.stdout, child.stderr])(subprocess.run([runner_11_interpreter, '-c', code] + [_value(row[2], pwd, repository) for row in _rows(sheets, 'arguments', key)], input=runner_11_utf_8_encode, cwd=pwd, env=dict(os.environ), capture_output=True))
    return [runner_11_run_a_command[0], None, runner_11_run_a_command[1], runner_11_run_a_command[2]]

def _compared(sheets: list[dict[str, Any,]], key: list[str], record: list[str], outcome: list[Any], above: list[list[Any]], pwd: str, repository: str, books: list[dict[str, Any,]], relational_model: types.ModuleType) -> list[str]:
    failed = []
    expected = ''.join([word[:1].upper() + word[1:] for word in record[2].split(' ')]) + 'Error' if record[2] != '' else ''
    actual = type(outcome[1]).__name__ if outcome[1] is not None else ''
    if actual != expected:
        failed.append('error ' + actual)
    said = str(outcome[1]) if outcome[1] is not None else str(outcome[3], 'utf-8')
    if record[3] != '' and said != _value(record[3], pwd, repository):
        failed.append('reason ' + said)
    if record[4] == 'true' and outcome[2] == b'':
        failed.append('output')
    if record[4] == 'false' and outcome[2] != b'':
        failed.append('output')
    if record[5] == 'true' and outcome[3] == b'':
        failed.append('diagnostic')
    if record[5] == 'false' and outcome[3] != b'':
        failed.append('diagnostic')
    kinds = [row[1] for row in _rows(books, 'Results', record[:2])]
    results = [outcome[0]] if len(kinds) < 2 or outcome[0] is None else list(outcome[0])
    for position in dict.fromkeys([row[0] for row in _rows(sheets, 'results', key)]):
        held = _written(results[int(position) - 1], kinds[int(position) - 1], books)
        if held != [[row[1], _value(row[2], pwd, repository)] for row in _rows(sheets, 'results', key) if row[0] == position]:
            failed.append('result ' + position + ' ' + repr(held))
    for position in dict.fromkeys([row[0] for row in _rows(sheets, 'result instances', key)]):
        failed.extend(_matched('result ' + position, bytes(results[int(position) - 1], 'utf-8'), [row[1:] for row in _rows(sheets, 'result instances', key) if row[0] == position], True, pwd, repository, relational_model))
    lines = outcome[2].split(b'\n')
    for line in dict.fromkeys([row[0] for row in _rows(sheets, 'stdout lines', key)]):
        failed.extend(_matched('line ' + line, lines[int(line) - 1] if int(line) <= len(lines) else b'', [row[1:] for row in _rows(sheets, 'stdout lines', key) if row[0] == line], False, pwd, repository, relational_model))
    for row in _rows(sheets, 'placed', key):
        if row[0] == 'after' and not _same(_after(row[1], results, outcome, pwd, repository, relational_model), _fixture(row[2], above, pwd, repository)):
            failed.append('placed ' + row[1])
    for row in _rows(sheets, 'expected files', key):
        held = outcome[2] if row[0] == '-' else _bytes(_path(row[0], pwd, repository))
        if held != _bytes(_beside(row[1], above)):
            failed.append('file ' + row[0])
    for row in _rows(sheets, 'file texts', key):
        if not [line for line in str(_bytes(_path(row[0], pwd, repository)), 'utf-8').split('\n') if _value(row[2], pwd, repository) in line]:
            failed.append('text ' + row[2])
    for pathname in dict.fromkeys([row[0] for row in _rows(sheets, 'file instances', key)]):
        failed.extend(_matched(pathname, _bytes(_path(pathname, pwd, repository)), [row[1:] for row in _rows(sheets, 'file instances', key) if row[0] == pathname], False, pwd, repository, relational_model))
    for row in _rows(sheets, 'absent', key):
        runner_5_exists = os.path.lexists(_path(row[0], pwd, repository))
        if runner_5_exists:
            failed.append('absent ' + row[0])
    return failed

def _content(record: list[str], runs: list[list[str]]) -> str:
    text = record[4]
    last = []
    for run in [run for run in runs if run[0] == record[0]]:
        if last and run[1] != last[1]:
            text = text + '\f'
        if last and run[1] == last[1] and run[2] != last[2]:
            text = text + '\n'
        if last and run[1:3] == last[1:3]:
            text = text + '\t'
        text = text + run[4]
        last = run
    return text
_controls = ['NUL', 'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'TAB', 'LF', 'VT', 'FF', 'CR', 'SO', 'SI', 'DLE', 'DC1', 'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB', 'ESC', 'FS', 'GS', 'RS', 'US', 'DEL']
_date_time = '[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-9]{2}([.][0-9]+)?[Zz]'

def _documents(home: str) -> str:
    return '/storage/emulated/0/Documents' if sys.platform == 'android' else os.path.join(home, 'Documents')

def _encoded(segment: str) -> str:
    named = ''.join([chr(octet) if chr(octet) in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~' else '%' + format(octet, '02X') for octet in bytes(segment, 'utf-8')])
    return '_' + named if named.startswith('_') else named

def _fixture(name: str, above: list[list[Any]], pwd: str, repository: str) -> list[dict[str, Any,]]:
    sheets = []
    for row in [row for entry in above for row in _rows(entry[1], 'fixtures', [name])]:
        if row[1] == '0':
            sheets.append({'sheet name': _value(row[3], pwd, repository), 'header': [], 'records': []})
        if row[1] == '1':
            sheets[-1]['header'].append(_value(row[3], pwd, repository))
        if row[1] not in ['0', '1'] and row[2] == '1':
            sheets[-1]['records'].append([])
        if row[1] not in ['0', '1']:
            sheets[-1]['records'][-1].append(_value(row[3], pwd, repository))
    return sheets

def _found(folder: str, relational_model: types.ModuleType) -> list[list[Any]]:
    found = []
    for walked in sorted(os.walk(folder)):
        for name in sorted(walked[2]):
            if name.endswith('.mtsv'):
                found.append([os.path.join(walked[0], name), relational_model.load(_bytes(os.path.join(walked[0], name)))])
    return found

def _instances(octets: bytes, relational_model: types.ModuleType) -> list[list[str]]:
    held = relational_model.instances(octets)
    pointers = {'': ''}
    found = []
    for record in held[0]['records']:
        pointers[record[0]] = pointers[record[1]] + record[2]
        found.append([pointers[record[0]], record[3], _content(record, held[1]['records'])])
    return found

def _matched(name: str, octets: bytes, given: list[list[str]], whole: bool, pwd: str, repository: str, relational_model: types.ModuleType) -> list[str]:
    expected = [[row[0], row[1], _value(row[2], pwd, repository)] for row in given]
    try:
        held = _instances(octets, relational_model)
    except relational_model.NotAJSONTextError:
        return [name + ' not a JSON text']
    except relational_model.NamesNotUniqueError:
        return [name + ' names not unique']
    if whole and sorted(held) != sorted(expected):
        return [name + ' ' + repr(held)]
    return [name + ' ' + repr(instance) for instance in expected if instance not in held]

def _path(text: str, pwd: str, repository: str) -> str:
    return os.path.join(repository, _value(text, pwd, repository).replace('/', os.sep))

def _placed(sheets: list[dict[str, Any,]], key: list[str], above: list[list[Any]], pwd: str, repository: str, relational_model: types.ModuleType) -> dict[str, Any,]:
    given = {}
    for row in _rows(sheets, 'placed', key):
        if row[0] == 'before' and row[1].startswith('argument '):
            given[row[1][9:]] = _fixture(row[2], above, pwd, repository)
        if row[0] == 'before' and not row[1].startswith('argument '):
            _write(_path(row[1], pwd, repository), relational_model.dump(_fixture(row[2], above, pwd, repository)))
    for row in _rows(sheets, 'octets', key):
        _write(_path(row[0], pwd, repository), _bytes(_beside(row[1], above)))
        if row[2] != '':
            os.utime(_path(row[0], pwd, repository), (time.time() - float(row[2]), time.time() - float(row[2]),))
    for pathname in dict.fromkeys([row[0] for row in _rows(sheets, 'zip entries', key)]):
        _write(_path(pathname, pwd, repository), _zip([row[2:] for row in _rows(sheets, 'zip entries', key) if row[0] == pathname], pwd, repository))
    for pathname in dict.fromkeys([row[0] for row in _rows(sheets, 'database statements', key)]):
        os.makedirs(os.path.dirname(_path(pathname, pwd, repository)), exist_ok=True)
        (lambda connection: (connection.executescript(''.join([_value(row[2], pwd, repository) + ';\n' for row in _rows(sheets, 'database statements', key) if row[0] == pathname])), connection.close(),))(sqlite3.connect(_path(pathname, pwd, repository)))
    return given

def _reached(name: str, books: list[dict[str, Any,]], root: types.ModuleType) -> types.ModuleType:
    parents = dict([row[:2] for row in _sheet(books, 'Modules')])
    chain = [name]
    while parents[chain[0]] != '':
        chain.insert(0, parents[chain[0]])
    module = root
    for step in chain[1:]:
        module = getattr(module, [row[0] for row in _sheet(books, 'Files') if row[1] == step and row[0].startswith('python/')][0].split('/')[-1][:-3])
    return module

def _read(items: list[list[str]], kind: str, books: list[dict[str, Any,]], root: types.ModuleType, pwd: str, repository: str) -> Any:
    held = [row for row in _sheet(books, 'Types') if row[0] == kind]
    if held and held[0][2] == 'array':
        return [_read([['0', item[1]]], held[0][1], books, root, pwd, repository) for item in items if item[0] != '0']
    value = items[0][1] if items else ''
    if kind == 'number':
        return int(value) if value.lstrip('-').isdigit() else float(value)
    if kind == 'boolean':
        return value == 'true'
    if kind == 'bytes':
        return bytes(_value(value, pwd, repository), 'utf-8')
    if kind == 'module':
        return _reached(value, books, root)
    if kind == 'absolute path':
        return _path(value, pwd, repository)
    return _value(value, pwd, repository)

def _rows(sheets: list[dict[str, Any,]], name: str, key: list[str]) -> list[list[str]]:
    return [record[len(key):] for record in _sheet(sheets, name) if record[:len(key)] == key]

def _same(held: list[dict[str, Any,]], given: list[dict[str, Any,]]) -> bool:
    return [_timeless(sheet) for sheet in held] == [_timeless(sheet) for sheet in given]

def _sheet(sheets: list[dict[str, Any,]], name: str) -> list[list[str]]:
    return [record for sheet in sheets if sheet['sheet name'] == name for record in sheet['records']]

def _snake(name: str) -> str:
    return name.lower().replace(' ', '_').replace('-', '_')

def _text(written: str) -> str:
    text = written
    for code, name, in enumerate(_controls):
        text = text.replace('<' + name + '>', chr(code if code < 32 else 127))
    return text

def _timeless(sheet: dict[str, Any,]) -> list[Any]:
    return [sheet['sheet name'], sheet['header'], [['' if sheet['header'][index] == '_time' and re.fullmatch(_date_time, field) else field for index, field, in enumerate(record)] for record in sheet['records']]]

def _value(text: str, pwd: str, repository: str) -> str:
    runner_6_home_folder = os.path.expanduser('~')
    named = os.sep.join([_encoded(segment) for segment in pwd.replace(os.sep, '/').split('/') if segment])
    return _text(text.replace('$HOME/Documents', _documents(runner_6_home_folder)).replace('$INPUT', named).replace('$PWD', pwd).replace('$HOME', runner_6_home_folder).replace('$REPOSITORY', repository))

def _write(pathname: str, data: bytes) -> None:
    os.makedirs(os.path.dirname(pathname), exist_ok=True)
    with open(pathname, 'wb') as file:
        file.write(data)

def _written(value: Any, kind: str, books: list[dict[str, Any,]]) -> list[list[str]]:
    held = [row for row in _sheet(books, 'Types') if row[0] == kind]
    if held and held[0][2] == 'array':
        return [[str(index + 1), _written(item, held[0][1], books)[0][1]] for index, item, in enumerate(value)] or [['0', '']]
    if kind == 'boolean':
        return [['0', 'true' if value else 'false']]
    if kind == 'bytes':
        return [['0', str(value, 'utf-8')]]
    if kind == 'nothing':
        return [['0', '']]
    return [['0', str(value)]]

def _zip(entries: list[list[str]], pwd: str, repository: str) -> bytes:
    local = b''
    central = b''
    for entry in entries:
        runner_3_utf_8_encode = bytes(_value(entry[2], pwd, repository), 'utf-8')
        runner_3_crc_32 = zlib.crc32(runner_3_utf_8_encode)
        data = runner_3_utf_8_encode
        if entry[1] == '8':
            runner_3_deflate_write = (lambda compressor: compressor.compress(runner_3_utf_8_encode) + compressor.flush())(zlib.compressobj(wbits=-15))
            data = runner_3_deflate_write
        name = bytes(entry[0], 'utf-8')
        fields = int.to_bytes(int(entry[1]), 2, 'little') + bytes(4) + int.to_bytes(runner_3_crc_32, 4, 'little') + int.to_bytes(len(data), 4, 'little') + int.to_bytes(len(runner_3_utf_8_encode), 4, 'little') + int.to_bytes(len(name), 2, 'little') + bytes(2)
        central = central + int.to_bytes(33639248, 4, 'little') + bytes([20, 0, 20, 0, 0, 0]) + fields + bytes(10) + int.to_bytes(len(local), 4, 'little') + name
        local = local + int.to_bytes(67324752, 4, 'little') + bytes([20, 0, 0, 0]) + fields + name + data
    return local + central + int.to_bytes(101010256, 4, 'little') + bytes(4) + int.to_bytes(len(entries), 2, 'little') + int.to_bytes(len(entries), 2, 'little') + int.to_bytes(len(central), 4, 'little') + int.to_bytes(len(local), 4, 'little') + bytes(2)
