import * as fs from 'node:fs';
import * as conversion from './conversion/conversion.js';
import * as input from './input/input.js';
import * as reply from './reply/reply.js';
export function read(values, pathname, sheet, records, fields, filter, join, relationalModel, dataBank) {
    const bank = resolved(dataBank.folder(values, relationalModel));
    const place = pathname.startsWith('/') ? resolved(pathname) : pathname;
    const alone = sheet + records + fields + filter + join === '';
    let given;
    let file;
    let chosen;
    try {
        given = place === bank || place.startsWith(bank + '/') ? banked(values, place, bank, alone, dataBank, relationalModel) : files(pathname, place, relationalModel);
        file = { 'sheet name': 'file', header: ['file', 'source'], records: given[2] };
        chosen = relationalModel.chosen(given[0], { 'sheet name': 'origins', header: ['sheet', 'file'], records: given[1] }, file, given[3], sheet, records, fields, filter, join);
    }
    catch (error) {
        if (error instanceof dataBank.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof input.RefusedError) {
            throw new RefusedError(error.message);
        }
        if (error instanceof relationalModel.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
    return reply.reply([file, { 'sheet name': 'not read', header: ['file', 'status', 'reason'], records: given[4] }, { 'sheet name': 'left behind', header: ['file', 'what'], records: given[5] }, chosen[1]], alone ? [{ 'sheet name': 'fields', header: ['file', 'sheet', 'field', 'field name'], records: map(chosen) }] : chosen[0], relationalModel);
}
export class KeepingFailedError extends Error {}
export class RefusedError extends Error {}
function banked(values, place, bank, alone, dataBank, relationalModel) {
    const names = dataBank.names(values, relationalModel);
    const inputs = names.filter((relation) => relation['sheet name'] === '_inputs')[0].records;
    if (place === bank && alone) {
        return [names, names.map((relation, index) => [String(index + 1), '1']), [['1', bank]], 'file', [], []];
    }
    if (place === bank) {
        const sheets = [];
        const origins = [];
        for (const [index, given] of inputs.entries()) {
            for (const relation of dataBank.records(values, given[0], 0, Number(given[1]) - 1, [], relationalModel)) {
                sheets.push(relation);
                origins.push([String(sheets.length), String(index + 1)]);
            }
        }
        return [sheets, origins, inputs.map((given, index) => [String(index + 1), given[0]]), '_input', [], []];
    }
    for (const given of inputs) {
        if (place === resolved(given[2])) {
            const sheets = [...dataBank.records(values, given[0], 0, Number(given[1]) - 1, [], relationalModel), dataBank.stored(values, given[0], 0, Number(given[1]) - 1, relationalModel)];
            return [sheets, sheets.map((relation, index) => [String(index + 1), '1']), [['1', given[0]]], 'file', [], []];
        }
    }
    throw new RefusedError('names no input of the data bank');
}
function files(pathname, place, relationalModel) {
    const members = input.members(pathname);
    const sheets = [];
    const origins = [];
    const left = [...members[1].records];
    const behind = [];
    for (const [number, source] of members[0].records) {
        if (!members[1].records.map((record) => record[0]).includes(number)) {
            let converted = [[], []];
            try {
                converted = conversion.sheets(source, relationalModel);
            }
            catch (error) {
                if (error instanceof conversion.NoFormatError) {
                    if (source === place) {
                        throw new RefusedError('no format');
                    }
                    left.push([number, 'no format', '']);
                    continue;
                }
                if (error instanceof conversion.FailedError) {
                    if (source === place) {
                        throw new RefusedError('failed: ' + error.message);
                    }
                    left.push([number, 'failed', error.message]);
                    continue;
                }
                throw error;
            }
            for (const relation of converted[0]) {
                sheets.push(relation);
                origins.push([String(sheets.length), number]);
            }
            for (const what of converted[1]) {
                behind.push([number, what]);
            }
        }
    }
    return [sheets, origins, members[0].records, 'file', left, behind];
}
function map(chosen) {
    const found = [];
    for (const [index, relation] of chosen[0].entries()) {
        for (const [position, name] of (relation.header ?? []).entries()) {
            found.push([chosen[1].records[index][0], chosen[1].records[index][1], String(position + 1), name]);
        }
    }
    return found;
}
function resolved(pathname) {
    try {
        return fs.realpathSync(pathname);
    }
    catch (error) {
        return pathname;
    }
}
