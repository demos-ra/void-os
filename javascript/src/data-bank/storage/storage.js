import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
export function communicated(values, inputName, session, agent, relationalModel, converter) {
    try {
        const found = records(values, '_communicated.mtsv', relationalModel).find((record) => record[0] === inputName && record[1] === session && record[2] === agent);
        return found === undefined ? 0 : Number(found[3]);
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export function folder(values, relationalModel, converter) {
    return bank(values);
}
export function insert(values, inputName, inputValues, moduleSpecification, event, relationalModel, converter) {
    try {
        fs.mkdirSync(bank(values), { recursive: true });
        lock(values);
        try {
            return inserted(values, inputName, inputValues, moduleSpecification, event, relationalModel, converter);
        }
        finally {
            fs.unlinkSync(at(values, '_lock'));
        }
    }
    catch (error) {
        if (error instanceof converter.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export function inputs(values, relationalModel, converter) {
    try {
        const found = records(values, '_stored.mtsv', relationalModel);
        const listed = [];
        for (const inputName of new Set(found.map((record) => record[0]))) {
            const storage11Count = found.filter((record) => record[0] === inputName).length;
            listed.push([inputName, String(storage11Count), pathname(values, inputName)]);
        }
        return { 'sheet name': '_inputs', header: ['_input', '_values', '_file'], records: listed };
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export function markCommunicated(values, inputName, session, agent, count, relationalModel, converter) {
    if (Array.from('\t\n\f\r').some((character) => session.includes(character) || agent.includes(character))) {
        return;
    }
    try {
        fs.mkdirSync(bank(values), { recursive: true });
        lock(values);
        try {
            const found = records(values, '_communicated.mtsv', relationalModel).filter((record) => record[0] !== inputName || record[1] !== session || record[2] !== agent);
            replace(values, at(values, '_communicated.mtsv'), [{ 'sheet name': '_communicated', header: ['_input', '_session', '_agent', '_values'], records: found.concat([[inputName, session, agent, String(count)]]) }], relationalModel);
        }
        finally {
            fs.unlinkSync(at(values, '_lock'));
        }
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export function names(values, relationalModel, converter) {
    try {
        return [{ 'sheet name': '_sheets', header: ['_input', '_place', '_sheet name'], records: records(values, '_sheets.mtsv', relationalModel) }, { 'sheet name': '_fields', header: ['_input', '_place', '_position', '_field name'], records: records(values, '_fields.mtsv', relationalModel) }];
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export function relations(values, inputName, relationalModel, converter) {
    try {
        return whole(sheets(pathname(values, inputName), relationalModel), records(values, '_stored.mtsv', relationalModel).filter((record) => record[0] === inputName).length);
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export function stored(values, inputName, first, last, relationalModel, converter) {
    try {
        return { 'sheet name': '_stored', header: ['_input', '_input value', '_time', '_event'], records: records(values, '_stored.mtsv', relationalModel).filter((record) => record[0] === inputName && first <= Number(record[1]) && Number(record[1]) <= last) };
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new KeepingFailedError('keeping failed');
        }
        if (error.syscall !== undefined) {
            throw new KeepingFailedError('keeping failed');
        }
        throw error;
    }
}
export class KeepingFailedError extends Error {}
export class NonConformingError extends Error {}
function at(values, name) {
    return path.join(bank(values), name);
}
function bank(values) {
    return process.env[value(values, 'data bank variable')] || path.join(documents(), value(values, 'data bank folder'));
}
function cut(values, inputName, start, relationalModel) {
    const held = sheets(pathname(values, inputName), relationalModel);
    if (held.some((sheet) => sheet.records.some((record) => Number(record[0]) >= start))) {
        replace(values, pathname(values, inputName), whole(held, start), relationalModel);
    }
    const found = records(values, '_stored.mtsv', relationalModel);
    if (found.some((record) => record[0] === inputName && Number(record[1]) >= start)) {
        replace(values, at(values, '_stored.mtsv'), [{ 'sheet name': '_stored', header: ['_input', '_input value', '_time', '_event'], records: found.filter((record) => record[0] !== inputName || Number(record[1]) < start) }], relationalModel);
    }
}
function documents() {
    if (process.platform === 'android') {
        return '/storage/emulated/0/Documents';
    }
    return path.join(os.homedir(), 'Documents');
}
function encoded(segment) {
    const named = Array.from(new TextEncoder().encode(segment), (octet) => 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'.includes(String.fromCharCode(octet)) ? String.fromCharCode(octet) : '%' + octet.toString(16).toUpperCase().padStart(2, '0')).join('');
    return named.startsWith('_') ? '_' + named : named;
}
function inserted(values, inputName, inputValues, moduleSpecification, event, relationalModel, converter) {
    const start = records(values, '_stored.mtsv', relationalModel).filter((record) => record[0] === inputName).length;
    const text = converter.convert(inputValues, moduleSpecification, start, relationalModel)[0];
    const named = converter.sheets(moduleSpecification, inputName, relationalModel);
    fs.mkdirSync(path.dirname(pathname(values, inputName)), { recursive: true });
    cut(values, inputName, start, relationalModel);
    fs.appendFileSync(pathname(values, inputName), new TextEncoder().encode(text));
    const storage8TimeNow = new Date().toISOString();
    fs.appendFileSync(at(values, '_stored.mtsv'), relationalModel.dump([{ 'sheet name': '_stored', header: ['_input', '_input value', '_time', '_event'], records: inputValues.map((octets, index) => [inputName, String(start + index), storage8TimeNow, event]) }]));
    replace(values, at(values, '_sheets.mtsv'), [{ 'sheet name': '_sheets', header: named[0].header, records: replaced(records(values, '_sheets.mtsv', relationalModel), inputName, named[0].records) }], relationalModel);
    replace(values, at(values, '_fields.mtsv'), [{ 'sheet name': '_fields', header: named[1].header, records: replaced(records(values, '_fields.mtsv', relationalModel), inputName, named[1].records) }], relationalModel);
    return inputValues.length;
}
function lock(values) {
    const pathname = at(values, '_lock');
    while (true) {
        try {
            fs.closeSync(fs.openSync(pathname, 'wx'));
            return;
        }
        catch (error) {
            if (error.code !== 'EEXIST') {
                throw error;
            }
        }
        try {
            if (Date.now() - fs.statSync(pathname).mtimeMs > Number(value(values, 'lock timeout')) * 1000) {
                fs.unlinkSync(pathname);
            }
            else {
                Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, Number(value(values, 'lock wait')) * 1000);
            }
        }
        catch (error) {
            if (error.code !== 'ENOENT') {
                throw error;
            }
        }
    }
}
function pathname(values, inputName) {
    const segments = inputName.replaceAll(path.sep, '/').split('/').filter((segment) => segment !== '').map((segment) => encoded(segment));
    return path.join(bank(values), segments.join(path.sep) + '.mtsv');
}
function records(values, name, relationalModel) {
    return sheets(at(values, name), relationalModel).flatMap((sheet) => sheet.records);
}
function replace(values, pathname, held, relationalModel) {
    fs.writeFileSync(pathname + value(values, 'replace suffix'), relationalModel.dump(held));
    fs.renameSync(pathname + value(values, 'replace suffix'), pathname);
}
function replaced(found, inputName, given) {
    const held = found.map((record) => record[0]);
    const place = held.includes(inputName) ? held.indexOf(inputName) : found.length;
    const kept = found.filter((record) => record[0] !== inputName);
    return kept.slice(0, place).concat(given, kept.slice(place));
}
function sheets(pathname, relationalModel) {
    try {
        return relationalModel.load(fs.readFileSync(pathname));
    }
    catch (error) {
        if (error.code === 'ENOENT') {
            return [];
        }
        throw error;
    }
}
function value(values, name) {
    return new Map(values.records).get(name);
}
function whole(held, count) {
    const kept = held.map((sheet) => ({ 'sheet name': sheet['sheet name'], header: sheet.header, records: sheet.records.filter((record) => Number(record[0]) < count) }));
    return kept.filter((sheet) => sheet.records.length > 0);
}
