export function insert(values, inputName, event, hookInput, relationalModel, dataBank) {
    try {
        return dataBank.insert(values, inputName, [hookInput], new TextEncoder().encode(new Map(values.records).get('hook input schema')), event, relationalModel);
    }
    catch (error) {
        if (error instanceof dataBank.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof dataBank.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        throw error;
    }
}
export class KeepingFailedError extends Error {}
export class NonConformingError extends Error {}
