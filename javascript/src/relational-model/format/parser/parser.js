export function load(octets) {
    try {
        const parser4UTF8Decode = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(octets);
        return loads(parser4UTF8Decode);
    }
    catch (error) {
        if (error instanceof TypeError) {
            const prefix = validPrefix(octets);
            throw new NotMTSVError(where(prefix, prefix.length));
        }
        throw error;
    }
}
export function loads(text) {
    return parse(text);
}
export class NotMTSVError extends Error {}
function parse(text) {
    let position = 0;
    if (text.startsWith('\ufeff')) {
        position = 1;
    }
    function mtsvFile() {
        const sheets = [];
        if (position < text.length && !ff()) {
            sheets.push(firstSheet());
        }
        while (ff()) {
            sheets.push(namedSheet());
        }
        return sheets;
    }
    function firstSheet() {
        return sheetBody('');
    }
    function namedSheet() {
        position = position + 1;
        const name = sheetName();
        eol();
        return sheetBody(name);
    }
    function sheetBody(name) {
        if (position === text.length || ff()) {
            return { 'sheet name': name, header: null, records: [] };
        }
        const fields = header();
        const records = [];
        while (position < text.length && !ff()) {
            const start = position;
            const values = record();
            if (values.length !== fields.length) {
                throw new NotMTSVError(where(text, start));
            }
            records.push(values);
        }
        return { 'sheet name': name, header: fields, records: records };
    }
    function header() {
        return record();
    }
    function record() {
        const fields = [field()];
        while (text.startsWith('\t', position)) {
            position = position + 1;
            fields.push(field());
        }
        eol();
        return fields;
    }
    function field() {
        const start = position;
        while (position < text.length && fieldChar(text[position])) {
            position = position + 1;
        }
        return text.slice(start, position);
    }
    function sheetName() {
        return field();
    }
    function fieldChar(character) {
        return !'\t\n\f\r'.includes(character);
    }
    function ff() {
        return text.startsWith('\f', position);
    }
    function eol() {
        if (text.startsWith('\n', position)) {
            position = position + 1;
        }
        else {
            if (text.startsWith('\r\n', position)) {
                position = position + 2;
            }
            else {
                throw new NotMTSVError(where(text, position));
            }
        }
    }
    return mtsvFile();
}
function validPrefix(octets) {
    const decoder = new TextDecoder('utf-8', { fatal: true });
    let prefix = '';
    for (const index of octets.keys()) {
        try {
            prefix = prefix + decoder.decode(octets.subarray(index, index + 1), { stream: true });
        }
        catch {
            return prefix;
        }
    }
    return prefix;
}
function where(text, position) {
    const before = text.slice(0, position);
    const line = before.split('\n').length;
    return String(line);
}
