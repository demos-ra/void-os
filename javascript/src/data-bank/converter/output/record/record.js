export function records(transferred) {
    const cells = new Map(transferred[1].records.map((record) => [record[0] + '\n' + record[1] + '\n' + record[2] + '\n' + record[3], record[4]]));
    const keys = new Map(transferred[2].records.map((record) => [record[0] + '\n' + record[1] + '\n' + record[2], record]));
    const places = transferred[3].records;
    const relations = [];
    for (const place of places.filter((record) => record[1] === '' && record[0] !== '_runs').sort((one, other) => Number(one[2]) - Number(other[2]))) {
        const columns = places.filter((record) => record[0] === place[0] && record[1] !== '').sort((one, other) => Number(one[2]) - Number(other[2])).map((record) => record[1]);
        const held = transferred[0].records.filter((record) => record[0] === place[0]);
        const alone = place[0] === '' && held.every((record) => record[3] === '');
        const rows = [];
        for (const record of held) {
            const key = keys.get(record[0] + '\n' + record[1] + '\n' + record[2]);
            rows.push((alone ? [record[1]] : [record[1], record[2], key[3], key[4]]).concat(columns.map((column) => cells.get(record[0] + '\n' + record[1] + '\n' + record[2] + '\n' + column) ?? '')));
        }
        relations.push({ 'sheet name': place[0], header: (alone ? ['_input value'] : ['_input value', '_instance', '_parent', '_pointer']).concat(columns), records: rows });
    }
    return relations;
}
