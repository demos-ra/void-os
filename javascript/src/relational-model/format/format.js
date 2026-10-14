import * as generator from './generator/generator.js';
import * as jsonText from './json-text/json-text.js';
import * as parser from './parser/parser.js';
export function dump(sheets) {
    try {
        return generator.dump(sheets);
    }
    catch (error) {
        if (error instanceof generator.CannotBeRepresentedError) {
            throw new CannotBeRepresentedError(error.message);
        }
        throw error;
    }
}
export function dumps(sheets) {
    try {
        return generator.dumps(sheets);
    }
    catch (error) {
        if (error instanceof generator.CannotBeRepresentedError) {
            throw new CannotBeRepresentedError(error.message);
        }
        throw error;
    }
}
export function instances(octets) {
    try {
        return jsonText.instances(octets);
    }
    catch (error) {
        if (error instanceof jsonText.NamesNotUniqueError) {
            throw new NamesNotUniqueError(error.message);
        }
        if (error instanceof jsonText.NotAJSONTextError) {
            throw new NotAJSONTextError(error.message);
        }
        throw error;
    }
}
export function load(octets) {
    try {
        return parser.load(octets);
    }
    catch (error) {
        if (error instanceof parser.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        throw error;
    }
}
export function loads(text) {
    try {
        return parser.loads(text);
    }
    catch (error) {
        if (error instanceof parser.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        throw error;
    }
}
export function named(instances, pointer) {
    return jsonText.named(instances, pointer);
}
export class CannotBeRepresentedError extends Error {}
export class NamesNotUniqueError extends Error {}
export class NotMTSVError extends Error {}
export class NotAJSONTextError extends Error {}
