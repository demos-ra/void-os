export function dump(sheets) {
    const generator3UTF8Encode = new TextEncoder().encode(dumps(sheets));
    return generator3UTF8Encode;
}
export function dumps(sheets) {
    return generate(sheets);
}
export class CannotBeRepresentedError extends Error {}
function generate(sheets) {
    function mtsvFile() {
        const texts = [];
        for (const [number, sheet] of sheets.entries()) {
            texts.push(namedSheet(sheet, String(number + 1)));
        }
        return texts.join('');
    }
    function namedSheet(sheet, place) {
        return ff() + sheetName(sheet['sheet name'], place + ' 0 1') + eol() + sheetBody(sheet, place);
    }
    function sheetBody(sheet, place) {
        if (sheet.header === null) {
            if (sheet.records.length > 0) {
                throw new CannotBeRepresentedError('records without a header cannot be represented: ' + place);
            }
            return '';
        }
        const texts = [header(sheet.header, place + ' 1')];
        for (const [number, fields] of sheet.records.entries()) {
            if (fields.length !== sheet.header.length) {
                throw new CannotBeRepresentedError('a record must have as many fields as its header: ' + place + ' ' + String(number + 2));
            }
            texts.push(record(fields, place + ' ' + String(number + 2)));
        }
        return texts.join('');
    }
    function header(fields, place) {
        return record(fields, place);
    }
    function record(fields, place) {
        if (fields.length === 0) {
            throw new CannotBeRepresentedError('a record must have a field: ' + place);
        }
        const texts = [];
        for (const [number, value] of fields.entries()) {
            texts.push(field(value, place + ' ' + String(number + 1)));
        }
        return texts.join('\t') + eol();
    }
    function field(value, place) {
        for (const character of value) {
            if (!fieldChar(character)) {
                throw new CannotBeRepresentedError(place);
            }
        }
        return value;
    }
    function sheetName(value, place) {
        return field(value, place);
    }
    function fieldChar(character) {
        return !'\t\n\f\r'.includes(character);
    }
    function ff() {
        return '\f';
    }
    function eol() {
        return '\n';
    }
    return mtsvFile();
}
