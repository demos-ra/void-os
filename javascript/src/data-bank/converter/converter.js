import * as input from './input/input.js';
import * as output from './output/output.js';
import * as transfer from './transfer/transfer.js';
export function convert(inputValues, moduleSpecification, start, relationalModel) {
    try {
        const [relations, values, notCarried] = input.read(moduleSpecification, inputValues, start, relationalModel);
        return [output.write(transfer.transfer(relations, values), values, relationalModel), notCarried];
    }
    catch (error) {
        if (error instanceof input.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        throw error;
    }
}
export function sheets(moduleSpecification, inputName, relationalModel) {
    try {
        const [relations, values] = input.read(moduleSpecification, [], 0, relationalModel);
        const transferred = transfer.transfer(relations, values);
        const named = output.sheets([transferred[0], transferred[1], transferred[2], transferred[3], transferred[7]], relationalModel);
        return [{ 'sheet name': '_sheets', header: ['_input', '_place', '_sheet name'], records: named.map((relation, place) => [inputName, String(place), relation['sheet name']]) }, { 'sheet name': '_fields', header: ['_input', '_place', '_position', '_field name'], records: named.flatMap((relation, place) => relation.header.map((name, position) => [inputName, String(place), String(position), name])) }];
    }
    catch (error) {
        if (error instanceof input.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        throw error;
    }
}
export class NonConformingError extends Error {}
