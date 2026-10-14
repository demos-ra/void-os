export function fields(cells, input) {
    const instances = new Map(input[0].records.map((record) => [record[0] + '\n' + record[1], record]));
    const texts = cells.records.map((record) => record.slice(0, 4).concat([instances.get(record[1] + '\n' + record[4])[record[3] === '_type' ? 4 : 5]]));
    return [{ 'sheet name': 'cells', header: ['location', '_input value', '_instance', 'column', 'value'], records: texts }, input[1]];
}
