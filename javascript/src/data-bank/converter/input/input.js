import * as schema from './schema/schema.js';
import * as value from './value/value.js';
export function read(moduleSpecification, inputValues, start, relationalModel) {
    try {
        const relations = schema.schema(moduleSpecification, relationalModel);
        const [values, notCarried] = value.values(inputValues, start, relationalModel);
        return [relations, values.concat([schema.validate(relations, values, relationalModel)]), notCarried];
    }
    catch (error) {
        if (error instanceof schema.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        if (error instanceof value.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        throw error;
    }
}
export class NonConformingError extends Error {}
