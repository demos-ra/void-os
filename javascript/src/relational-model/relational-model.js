import * as format from './format/format.js';
import * as query from './query/query.js';
export function chosen(sheets, origins, file, lead, sheet, records, fields, filter, join) {
    try {
        return query.chosen(sheets, origins, file, lead, sheet, records, fields, filter, join);
    }
    catch (error) {
        if (error instanceof query.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export function dump(sheets) {
    try {
        return format.dump(sheets);
    }
    catch (error) {
        if (error instanceof format.CannotBeRepresentedError) {
            throw new CannotBeRepresentedError(error.message);
        }
        throw error;
    }
}
export function dumps(sheets) {
    try {
        return format.dumps(sheets);
    }
    catch (error) {
        if (error instanceof format.CannotBeRepresentedError) {
            throw new CannotBeRepresentedError(error.message);
        }
        throw error;
    }
}
export function instances(octets) {
    try {
        return format.instances(octets);
    }
    catch (error) {
        if (error instanceof format.NamesNotUniqueError) {
            throw new NamesNotUniqueError(error.message);
        }
        if (error instanceof format.NotAJSONTextError) {
            throw new NotAJSONTextError(error.message);
        }
        throw error;
    }
}
export function kept(sheets, filter) {
    try {
        return query.kept(sheets, filter);
    }
    catch (error) {
        if (error instanceof query.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export function load(octets) {
    try {
        return format.load(octets);
    }
    catch (error) {
        if (error instanceof format.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        throw error;
    }
}
export function loads(text) {
    try {
        return format.loads(text);
    }
    catch (error) {
        if (error instanceof format.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        throw error;
    }
}
export function named(instances, pointer) {
    return format.named(instances, pointer);
}
export class CannotBeRepresentedError extends Error {}
export class NamesNotUniqueError extends Error {}
export class NotMTSVError extends Error {}
export class NotAJSONTextError extends Error {}
export class RefusedError extends Error {}
