export function details(values, inputName, position, relationalModel, dataBank) {
    try {
        return [...dataBank.records(values, inputName, position, position, [], relationalModel), dataBank.stored(values, inputName, position, position, relationalModel)];
    }
    catch (error) {
        if (error instanceof dataBank.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
}
export class KeepingFailedError extends Error {}
