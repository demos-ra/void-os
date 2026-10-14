export function names(values, relationalModel, converter, storage) {
    try {
        return [storage.inputs(values, relationalModel, converter)].concat(storage.names(values, relationalModel, converter));
    }
    catch (error) {
        if (error instanceof storage.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
function new_(values, inputName, session, agent, places, relationalModel, converter, storage) {
    try {
        const first = storage.communicated(values, inputName, session, agent, relationalModel, converter);
        const last = count(values, inputName, relationalModel, converter, storage) - 1;
        const found = given(values, inputName, first, last, places, relationalModel, converter, storage);
        storage.markCommunicated(values, inputName, session, agent, last + 1, relationalModel, converter);
        return found.concat([storage.stored(values, inputName, first, last, relationalModel, converter)]);
    }
    catch (error) {
        if (error instanceof storage.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
export { new_ as new };
export function records(values, inputName, first, last, places, relationalModel, converter, storage) {
    try {
        return given(values, inputName, first, last, places, relationalModel, converter, storage);
    }
    catch (error) {
        if (error instanceof storage.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
export class KeepingFailedError extends Error {}
function count(values, inputName, relationalModel, converter, storage) {
    const found = storage.inputs(values, relationalModel, converter).records.find((record) => record[0] === inputName);
    return found === undefined ? 0 : Number(found[1]);
}
function given(values, inputName, first, last, places, relationalModel, converter, storage) {
    const named = storage.names(values, relationalModel, converter);
    const held = storage.relations(values, inputName, relationalModel, converter);
    const listed = named[0].records.filter((place) => place[0] === inputName);
    const chosen = places.length > 0 ? listed.filter((place) => places.includes(place[1])) : listed;
    const found = [];
    for (const place of chosen) {
        const rows = held.filter((sheet) => sheet['sheet name'] === place[2]).flatMap((sheet) => sheet.records).filter((record) => first <= Number(record[0]) && Number(record[0]) <= last);
        if (rows.length > 0) {
            found.push({ 'sheet name': place[2], header: named[1].records.filter((field) => field[0] === inputName && field[1] === place[1]).map((field) => field[3]), records: rows });
        }
    }
    return found;
}
