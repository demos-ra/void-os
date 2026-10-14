export function load(octets) {
    let text = '';
    try {
        const csv1UTF8Decode = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(octets);
        text = csv1UTF8Decode;
    }
    catch (error) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    const found = records(text);
    if (found.some((record) => record.some((field) => Array.from('\t\n\f\r').some((character) => field.includes(character))))) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    return [[{ 'sheet name': '', header: found.length > 0 ? found[0] : [], records: found.slice(1) }], []];
}
export class CannotBeRepresentedError extends Error {}
function records(text) {
    const found = [];
    let record = [];
    let field = '';
    let quoted = false;
    let previous = '';
    for (const character of text.replaceAll('\r\n', '\n')) {
        if (character === '"') {
            if (previous === '"' && !quoted) {
                field = field + '"';
            }
            quoted = !quoted;
        }
        else {
            if (character === ',' && !quoted) {
                record.push(field);
                field = '';
            }
            else {
                if (character === '\n' && !quoted) {
                    record.push(field);
                    found.push(record);
                    record = [];
                    field = '';
                }
                else {
                    field = field + character;
                }
            }
        }
        previous = character;
    }
    if (field !== '' || record.length > 0) {
        record.push(field);
        found.push(record);
    }
    return found;
}
