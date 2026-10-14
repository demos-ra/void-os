import * as child_process from 'node:child_process';
import * as fs from 'node:fs';
import { createRequire } from 'node:module';
import * as os from 'node:os';
import * as path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import * as zlib from 'node:zlib';
export function run(values, requirement, case_, folder, root, relationalModel) {
    try {
        const key = [requirement, String(case_)];
        const repository = path.dirname(folder);
        const found_ = found(folder, relationalModel);
        const held = found_.filter((entry) => sheet(entry[1], 'cases').some((record) => record[0] === key[0] && record[1] === key[1]));
        if (held.length === 0) {
            throw new NoCaseError('no case');
        }
        const sheets = held[0][1];
        const place = path.dirname(held[0][0]) + path.sep;
        const above = found_.filter((entry) => place.startsWith(path.dirname(entry[0]) + path.sep)).sort((left, right) => path.dirname(left[0]).length - path.dirname(right[0]).length);
        const record = rows(sheets, 'cases', key)[0];
        const made = path.join(os.tmpdir(), 'void-os-' + requirement + '-' + String(case_) + '-' + String(process.hrtime.bigint()));
        fs.mkdirSync(path.join(made, 'home'), { recursive: true });
        const runner2ResolvePathname = fs.realpathSync(made);
        const runner2EnvironmentVariableNames = Object.keys(process.env);
        for (const name of runner2EnvironmentVariableNames) {
            if (!['PATH', 'SYSTEMROOT'].includes(name)) {
                delete process.env[name];
            }
        }
        const runner6Platform = process.platform;
        process.env['TZ'] = 'UTC0';
        process.env[runner6Platform === 'win32' ? 'USERPROFILE' : 'HOME'] = path.join(runner2ResolvePathname, 'home');
        for (const row of rows(sheets, 'environment', key)) {
            process.env[row[0]] = value(row[1], runner2ResolvePathname, repository);
        }
        const given = placed(sheets, key, above, runner2ResolvePathname, repository, relationalModel);
        const books_ = books(relationalModel);
        const starts = sheet(books_, 'Access programs').some((row) => row[0] === record[0] && row[1] === record[1] && row[2] !== '');
        let outcome = [undefined, undefined, new Uint8Array(0), new Uint8Array(0)];
        if (record[0] !== '' && starts) {
            outcome = command(sheets, key, record, books_, runner2ResolvePathname, repository);
        }
        if (record[0] !== '' && !starts) {
            outcome = call(values, sheets, key, record, given, books_, root, runner2ResolvePathname, repository);
        }
        return compared(sheets, key, record, outcome, above, runner2ResolvePathname, repository, books_, relationalModel);
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        throw error;
    }
}
export class NoCaseError extends Error {}
export class NotMTSVError extends Error {}
function after(pathname, results, outcome, pwd, repository, relationalModel) {
    if (pathname.startsWith('result ')) {
        const held = results[Number(pathname.slice(7)) - 1];
        return Array.isArray(held) ? held : [held];
    }
    if (pathname === '-') {
        return relationalModel.load(outcome[2]);
    }
    return relationalModel.load(bytes(path_(pathname, pwd, repository)));
}
function beside(name, above) {
    return above.filter((entry) => sheet(entry[1], 'octets').concat(sheet(entry[1], 'expected files')).some((row) => row[3] === name)).map((entry) => path.join(path.dirname(entry[0]), name)).at(-1);
}
function books(relationalModel) {
    const folder = path.join(import.meta.dirname, '..', '..', '..', '..', 'spec');
    return fs.readdirSync(folder).filter((name) => name.endsWith('.mtsv')).sort().flatMap((name) => relationalModel.load(bytes(path.join(folder, name))));
}
function bytes(pathname) {
    const runner1ReadAFile = fs.readFileSync(pathname);
    return runner1ReadAFile;
}
function call(values, sheets, key, record, given, books_, root, pwd, repository) {
    const arguments_ = [];
    for (const row of rows(books_, 'Parameters', record.slice(0, 2))) {
        const items = rows(sheets, 'arguments', key).filter((argument) => argument[0] === row[0]).map((argument) => argument.slice(1));
        if (row[0] in given) {
            arguments_.push(row[2] === 'relations' ? given[row[0]] : given[row[0]][0]);
        }
        if (!(row[0] in given) && row[3] === 'Values') {
            arguments_.push(values);
        }
        if (!(row[0] in given) && row[3] !== 'Values') {
            arguments_.push(read(items, row[2], books_, root, pwd, repository));
        }
    }
    for (const row of sheet(books_, 'Compositions')) {
        if (row[1] === record[0]) {
            arguments_.push(reached(row[2], books_, root));
        }
    }
    try {
        return [reached(record[0], books_, root)[camel(record[1])](...arguments_), undefined, new Uint8Array(0), new Uint8Array(0)];
    }
    catch (error) {
        return [undefined, error, new Uint8Array(0), new Uint8Array(0)];
    }
}
function camel(name) {
    return name.replaceAll('-', ' ').split(' ').map((word, index) => index === 0 ? word : word.slice(0, 1).toUpperCase() + word.slice(1)).join('');
}
function command(sheets, key, record, books_, pwd, repository) {
    const file = sheet(books_, 'Files').find((row) => row[1] === record[0] && row[0].startsWith('javascript/'))[0];
    const runner11Interpreter = process.execPath;
    const runner11UTF8Encode = new TextEncoder().encode(rows(sheets, 'stdin', key).map((row) => value(row[1], pwd, repository) + '\n').join(''));
    const operands = [runner11Interpreter, path.join(repository, file)].concat(rows(sheets, 'arguments', key).map((row) => value(row[2], pwd, repository)));
    const runner11RunACommand = ((child) => [child.status, child.stdout, child.stderr])(child_process.spawnSync(operands[0], operands.slice(1), { input: runner11UTF8Encode, cwd: pwd, env: process.env }));
    return [runner11RunACommand[0], undefined, runner11RunACommand[1], runner11RunACommand[2]];
}
function compared(sheets, key, record, outcome, above, pwd, repository, books_, relationalModel) {
    const failed = [];
    const expected = record[2] === '' ? '' : record[2].split(' ').map((word) => word.slice(0, 1).toUpperCase() + word.slice(1)).join('') + 'Error';
    const actual = outcome[1] === undefined ? '' : outcome[1].constructor.name;
    if (actual !== expected) {
        failed.push('error ' + actual);
    }
    const said = outcome[1] === undefined ? new TextDecoder().decode(outcome[3]) : outcome[1].message;
    if (record[3] !== '' && said !== value(record[3], pwd, repository)) {
        failed.push('reason ' + said);
    }
    if (record[4] === 'true' && outcome[2].length === 0) {
        failed.push('output');
    }
    if (record[4] === 'false' && outcome[2].length !== 0) {
        failed.push('output');
    }
    if (record[5] === 'true' && outcome[3].length === 0) {
        failed.push('diagnostic');
    }
    if (record[5] === 'false' && outcome[3].length !== 0) {
        failed.push('diagnostic');
    }
    const kinds = rows(books_, 'Results', record.slice(0, 2)).map((row) => row[1]);
    const results = kinds.length < 2 || outcome[0] === undefined ? [outcome[0]] : outcome[0];
    for (const position of new Set(rows(sheets, 'results', key).map((row) => row[0]))) {
        const held = written(results[Number(position) - 1], kinds[Number(position) - 1], books_);
        if (JSON.stringify(held) !== JSON.stringify(rows(sheets, 'results', key).filter((row) => row[0] === position).map((row) => [row[1], value(row[2], pwd, repository)]))) {
            failed.push('result ' + position + ' ' + JSON.stringify(held));
        }
    }
    for (const position of new Set(rows(sheets, 'result instances', key).map((row) => row[0]))) {
        failed.push(...matched('result ' + position, new TextEncoder().encode(results[Number(position) - 1]), rows(sheets, 'result instances', key).filter((row) => row[0] === position).map((row) => row.slice(1)), true, pwd, repository, relationalModel));
    }
    const lines = new TextDecoder().decode(outcome[2]).split('\n');
    for (const line of new Set(rows(sheets, 'stdout lines', key).map((row) => row[0]))) {
        failed.push(...matched('line ' + line, new TextEncoder().encode(lines[Number(line) - 1] ?? ''), rows(sheets, 'stdout lines', key).filter((row) => row[0] === line).map((row) => row.slice(1)), false, pwd, repository, relationalModel));
    }
    for (const row of rows(sheets, 'placed', key)) {
        if (row[0] === 'after' && !same(after(row[1], results, outcome, pwd, repository, relationalModel), fixture(row[2], above, pwd, repository))) {
            failed.push('placed ' + row[1]);
        }
    }
    for (const row of rows(sheets, 'expected files', key)) {
        const held = row[0] === '-' ? outcome[2] : bytes(path_(row[0], pwd, repository));
        if (Buffer.compare(held, bytes(beside(row[1], above))) !== 0) {
            failed.push('file ' + row[0]);
        }
    }
    for (const row of rows(sheets, 'file texts', key)) {
        if (!new TextDecoder().decode(bytes(path_(row[0], pwd, repository))).split('\n').some((line) => line.includes(value(row[2], pwd, repository)))) {
            failed.push('text ' + row[2]);
        }
    }
    for (const pathname of new Set(rows(sheets, 'file instances', key).map((row) => row[0]))) {
        failed.push(...matched(pathname, bytes(path_(pathname, pwd, repository)), rows(sheets, 'file instances', key).filter((row) => row[0] === pathname).map((row) => row.slice(1)), false, pwd, repository, relationalModel));
    }
    for (const row of rows(sheets, 'absent', key)) {
        let runner5Exists;
        try {
            fs.lstatSync(path_(row[0], pwd, repository));
            runner5Exists = true;
        }
        catch {
            runner5Exists = false;
        }
        if (runner5Exists) {
            failed.push('absent ' + row[0]);
        }
    }
    return failed;
}
function content(record, runs) {
    let text_ = record[4];
    let last = [];
    for (const run_ of runs.filter((held) => held[0] === record[0])) {
        if (last.length !== 0 && run_[1] !== last[1]) {
            text_ = text_ + '\f';
        }
        if (last.length !== 0 && run_[1] === last[1] && run_[2] !== last[2]) {
            text_ = text_ + '\n';
        }
        if (last.length !== 0 && run_[1] === last[1] && run_[2] === last[2]) {
            text_ = text_ + '\t';
        }
        text_ = text_ + run_[4];
        last = run_;
    }
    return text_;
}
const controls = ['NUL', 'SOH', 'STX', 'ETX', 'EOT', 'ENQ', 'ACK', 'BEL', 'BS', 'TAB', 'LF', 'VT', 'FF', 'CR', 'SO', 'SI', 'DLE', 'DC1', 'DC2', 'DC3', 'DC4', 'NAK', 'SYN', 'ETB', 'CAN', 'EM', 'SUB', 'ESC', 'FS', 'GS', 'RS', 'US', 'DEL'];
const dateTime = /^[0-9]{4}-[0-9]{2}-[0-9]{2}[Tt][0-9]{2}:[0-9]{2}:[0-9]{2}([.][0-9]+)?[Zz]$/;
function documents(home) {
    return process.platform === 'android' ? '/storage/emulated/0/Documents' : path.join(home, 'Documents');
}
function encoded(segment) {
    const named = Array.from(new TextEncoder().encode(segment), (octet) => 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'.includes(String.fromCharCode(octet)) ? String.fromCharCode(octet) : '%' + octet.toString(16).toUpperCase().padStart(2, '0')).join('');
    return named.startsWith('_') ? '_' + named : named;
}
function fixture(name, above, pwd, repository) {
    const sheets = [];
    for (const row of above.flatMap((entry) => rows(entry[1], 'fixtures', [name]))) {
        if (row[1] === '0') {
            sheets.push({ 'sheet name': value(row[3], pwd, repository), header: [], records: [] });
        }
        if (row[1] === '1') {
            sheets.at(-1).header.push(value(row[3], pwd, repository));
        }
        if (!['0', '1'].includes(row[1]) && row[2] === '1') {
            sheets.at(-1).records.push([]);
        }
        if (!['0', '1'].includes(row[1])) {
            sheets.at(-1).records.at(-1).push(value(row[3], pwd, repository));
        }
    }
    return sheets;
}
function found(folder, relationalModel) {
    return fs.readdirSync(folder, { recursive: true }).filter((name) => name.endsWith('.mtsv')).sort().map((name) => [path.join(folder, name), relationalModel.load(bytes(path.join(folder, name)))]);
}
function instances(octets, relationalModel) {
    const held = relationalModel.instances(octets);
    const pointers = new Map([['', '']]);
    const found_ = [];
    for (const record of held[0].records) {
        pointers.set(record[0], pointers.get(record[1]) + record[2]);
        found_.push([pointers.get(record[0]), record[3], content(record, held[1].records)]);
    }
    return found_;
}
function little(number, size) {
    const held = Buffer.alloc(size);
    held.writeUIntLE(number, 0, size);
    return held;
}
function matched(name, octets, given, whole, pwd, repository, relationalModel) {
    const expected = given.map((row) => JSON.stringify([row[0], row[1], value(row[2], pwd, repository)]));
    let held;
    try {
        held = instances(octets, relationalModel).map((instance) => JSON.stringify(instance));
    }
    catch (error) {
        if (error instanceof relationalModel.NotAJSONTextError) {
            return [name + ' not a JSON text'];
        }
        if (error instanceof relationalModel.NamesNotUniqueError) {
            return [name + ' names not unique'];
        }
        throw error;
    }
    if (whole && JSON.stringify(held.toSorted()) !== JSON.stringify(expected.toSorted())) {
        return [name + ' ' + JSON.stringify(held)];
    }
    return expected.filter((instance) => !held.includes(instance)).map((instance) => name + ' ' + instance);
}
function path_(text_, pwd, repository) {
    return path.resolve(repository, value(text_, pwd, repository).replaceAll('/', path.sep));
}
function placed(sheets, key, above, pwd, repository, relationalModel) {
    const given = {};
    for (const row of rows(sheets, 'placed', key)) {
        if (row[0] === 'before' && row[1].startsWith('argument ')) {
            given[row[1].slice(9)] = fixture(row[2], above, pwd, repository);
        }
        if (row[0] === 'before' && !row[1].startsWith('argument ')) {
            write(path_(row[1], pwd, repository), relationalModel.dump(fixture(row[2], above, pwd, repository)));
        }
    }
    for (const row of rows(sheets, 'octets', key)) {
        write(path_(row[0], pwd, repository), bytes(beside(row[1], above)));
        if (row[2] !== '') {
            fs.utimesSync(path_(row[0], pwd, repository), Date.now() / 1000 - Number(row[2]), Date.now() / 1000 - Number(row[2]));
        }
    }
    for (const pathname of new Set(rows(sheets, 'zip entries', key).map((row) => row[0]))) {
        write(path_(pathname, pwd, repository), zip(rows(sheets, 'zip entries', key).filter((row) => row[0] === pathname).map((row) => row.slice(2)), pwd, repository));
    }
    for (const pathname of new Set(rows(sheets, 'database statements', key).map((row) => row[0]))) {
        fs.mkdirSync(path.dirname(path_(pathname, pwd, repository)), { recursive: true });
        {
            const connection = new DatabaseSync(path_(pathname, pwd, repository));
            connection.exec(rows(sheets, 'database statements', key).filter((row) => row[0] === pathname).map((row) => value(row[2], pwd, repository) + ';\n').join(''));
            connection.close();
        }
    }
    return given;
}
function reached(name, books_, root) {
    if (sheet(books_, 'Modules').some((row) => row[0] === name && row[1] === '')) {
        return root;
    }
    return createRequire(import.meta.url)(path.join(import.meta.dirname, '..', '..', '..', '..', sheet(books_, 'Files').find((row) => row[1] === name && row[0].startsWith('javascript/'))[0]));
}
function read(items, kind, books_, root, pwd, repository) {
    const held = sheet(books_, 'Types').filter((row) => row[0] === kind);
    if (held.length !== 0 && held[0][2] === 'array') {
        return items.filter((item) => item[0] !== '0').map((item) => read([['0', item[1]]], held[0][1], books_, root, pwd, repository));
    }
    const value_ = items.length === 0 ? '' : items[0][1];
    if (kind === 'number') {
        return Number(value_);
    }
    if (kind === 'boolean') {
        return value_ === 'true';
    }
    if (kind === 'bytes') {
        return new TextEncoder().encode(value(value_, pwd, repository));
    }
    if (kind === 'module') {
        return reached(value_, books_, root);
    }
    if (kind === 'absolute path') {
        return path_(value_, pwd, repository);
    }
    return value(value_, pwd, repository);
}
function rows(sheets, name, key) {
    return sheet(sheets, name).filter((record) => key.every((field, index) => record[index] === field)).map((record) => record.slice(key.length));
}
function same(held, given) {
    return JSON.stringify(held.map((sheet_) => timeless(sheet_))) === JSON.stringify(given.map((sheet_) => timeless(sheet_)));
}
function sheet(sheets, name) {
    return sheets.filter((sheet_) => sheet_['sheet name'] === name).flatMap((sheet_) => sheet_.records);
}
function text(written_) {
    let text_ = written_;
    for (const name of controls) {
        text_ = text_.replaceAll('<' + name + '>', String.fromCharCode(controls.indexOf(name) < 32 ? controls.indexOf(name) : 127));
    }
    return text_;
}
function timeless(sheet_) {
    return [sheet_['sheet name'], sheet_.header, sheet_.records.map((record) => record.map((field, index) => sheet_.header[index] === '_time' && dateTime.test(field) ? '' : field))];
}
function value(text_, pwd, repository) {
    const runner6HomeFolder = os.homedir();
    const named = pwd.replaceAll(path.sep, '/').split('/').filter((segment) => segment !== '').map((segment) => encoded(segment)).join(path.sep);
    return text(text_.replaceAll('$HOME/Documents', documents(runner6HomeFolder)).replaceAll('$INPUT', named).replaceAll('$PWD', pwd).replaceAll('$HOME', runner6HomeFolder).replaceAll('$REPOSITORY', repository));
}
function write(pathname, data) {
    fs.mkdirSync(path.dirname(pathname), { recursive: true });
    fs.writeFileSync(pathname, data);
}
function written(value_, kind, books_) {
    const held = sheet(books_, 'Types').filter((row) => row[0] === kind);
    if (held.length !== 0 && held[0][2] === 'array') {
        return value_.length === 0 ? [['0', '']] : value_.map((item, index) => [String(index + 1), written(item, held[0][1], books_)[0][1]]);
    }
    if (kind === 'boolean') {
        return [['0', value_ ? 'true' : 'false']];
    }
    if (kind === 'bytes') {
        return [['0', new TextDecoder().decode(value_)]];
    }
    if (kind === 'nothing') {
        return [['0', '']];
    }
    return [['0', String(value_)]];
}
function zip(entries, pwd, repository) {
    let local = Buffer.alloc(0);
    let central = Buffer.alloc(0);
    for (const entry of entries) {
        const runner3UTF8Encode = new TextEncoder().encode(value(entry[2], pwd, repository));
        const runner3CRC32 = zlib.crc32(runner3UTF8Encode);
        let data = runner3UTF8Encode;
        if (entry[1] === '8') {
            const runner3DEFLATEWrite = zlib.deflateRawSync(runner3UTF8Encode);
            data = runner3DEFLATEWrite;
        }
        const name = new TextEncoder().encode(entry[0]);
        const fields = Buffer.concat([little(Number(entry[1]), 2), Buffer.alloc(4), little(runner3CRC32, 4), little(data.length, 4), little(runner3UTF8Encode.length, 4), little(name.length, 2), Buffer.alloc(2)]);
        central = Buffer.concat([central, little(33639248, 4), Buffer.from([20, 0, 20, 0, 0, 0]), fields, Buffer.alloc(10), little(local.length, 4), name]);
        local = Buffer.concat([local, little(67324752, 4), Buffer.from([20, 0, 0, 0]), fields, name, data]);
    }
    return Buffer.concat([local, central, little(101010256, 4), Buffer.alloc(4), little(entries.length, 2), little(entries.length, 2), little(central.length, 4), little(local.length, 4), Buffer.alloc(2)]);
}
