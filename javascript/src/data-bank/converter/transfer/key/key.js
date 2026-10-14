export function keys(records, instances) {
    const held = new Map(instances.records.map((record) => [record[0] + '\n' + record[1], record]));
    const keyed = [];
    for (const record of records.records) {
        let pointer = '';
        let instance = record[2];
        if (record[3] !== '') {
            while (instance !== record[3]) {
                pointer = held.get(record[1] + '\n' + instance)[3] + pointer;
                instance = held.get(record[1] + '\n' + instance)[2];
            }
        }
        keyed.push([record[0], record[1], record[2], record[3], pointer]);
    }
    return { 'sheet name': 'keys', header: ['location', '_input value', '_instance', '_parent', '_pointer'], records: keyed };
}
