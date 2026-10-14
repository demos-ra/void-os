import * as communication from './communication/communication.js';
import * as converter from './converter/converter.js';
import * as storage from './storage/storage.js';
export function folder(values, relationalModel) {
    return storage.folder(values, relationalModel, converter);
}
export function insert(values, inputName, inputValues, moduleSpecification, event, relationalModel) {
    try {
        return storage.insert(values, inputName, inputValues, moduleSpecification, event, relationalModel, converter);
    }
    catch (error) {
        if (error instanceof storage.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof storage.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        throw error;
    }
}
export function names(values, relationalModel) {
    try {
        return communication.names(values, relationalModel, converter, storage);
    }
    catch (error) {
        if (error instanceof communication.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
function new_(values, inputName, session, agent, places, relationalModel) {
    try {
        return communication.new(values, inputName, session, agent, places, relationalModel, converter, storage);
    }
    catch (error) {
        if (error instanceof communication.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
export { new_ as new };
export function records(values, inputName, first, last, places, relationalModel) {
    try {
        return communication.records(values, inputName, first, last, places, relationalModel, converter, storage);
    }
    catch (error) {
        if (error instanceof communication.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
export function stored(values, inputName, first, last, relationalModel) {
    try {
        return storage.stored(values, inputName, first, last, relationalModel, converter);
    }
    catch (error) {
        if (error instanceof storage.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
export class KeepingFailedError extends Error {}
export class NonConformingError extends Error {}
