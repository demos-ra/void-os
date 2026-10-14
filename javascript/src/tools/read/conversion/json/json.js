export function load(octets, relationalModel) {
    let given;
    try {
        given = relationalModel.instances(octets);
    }
    catch (error) {
        if (error instanceof relationalModel.NotAJSONTextError) {
            throw new NotAJSONTextError(error.message);
        }
        if (error instanceof relationalModel.NamesNotUniqueError) {
            throw new NamesNotUniqueError(error.message);
        }
        throw error;
    }
    const [instances, runs, notCarried] = given;
    if (runs.records.length > 0) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    const held = instances.records;
    return [elements(held, '0').map((element) => ({ 'sheet name': string(held, member(held, element, '/sheet name')), header: strings(held, member(held, element, '/header')), records: elements(held, member(held, element, '/records')).map((record) => strings(held, record)) })), notCarried];
}
export class CannotBeRepresentedError extends Error {}
export class NamesNotUniqueError extends Error {}
export class NotAJSONTextError extends Error {}
function elements(held, instance) {
    typed(held, instance, 'array');
    return held.filter((record) => record[1] === instance).map((record) => record[0]);
}
function member(held, instance, pointer) {
    typed(held, instance, 'object');
    const found = held.filter((record) => record[1] === instance && record[2] === pointer).map((record) => record[0]);
    if (found.length === 0) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    return found[0];
}
function string(held, instance) {
    const record = typed(held, instance, 'string');
    if (Array.from('\t\n\f\r').some((character) => record[4].includes(character))) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    return record[4];
}
function strings(held, instance) {
    return elements(held, instance).map((element) => string(held, element));
}
function typed(held, instance, kind) {
    const found = held.filter((record) => record[0] === instance && record[3] === kind);
    if (found.length === 0) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    return found[0];
}
