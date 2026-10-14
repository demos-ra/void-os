export function values(inputValues, start, relationalModel) {
    const instances = { 'sheet name': '_instances', header: ['_input value', '_instance', '_parent', '_pointer', '_type', '_value'], records: [] };
    const runs = { 'sheet name': '_runs', header: ['_input value', '_instance', '_page', '_line', '_position', '_value'], records: [] };
    const notCarried = [];
    for (const [index, octets] of inputValues.entries()) {
        const position = String(start + index);
        let found;
        try {
            found = relationalModel.instances(octets);
        }
        catch (error) {
            if (error instanceof relationalModel.NotAJSONTextError) {
                throw new NonConformingError(position + ' ' + '#');
            }
            if (error instanceof relationalModel.NamesNotUniqueError) {
                throw new NonConformingError(position + ' ' + error.message);
            }
            throw error;
        }
        instances.records.push(...found[0].records.map((record) => [position, ...record]));
        runs.records.push(...found[1].records.map((record) => [position, ...record]));
        notCarried.push(...found[2].map((pointer) => '/' + position + pointer));
    }
    return [[instances, runs], notCarried];
}
export class NonConformingError extends Error {}
