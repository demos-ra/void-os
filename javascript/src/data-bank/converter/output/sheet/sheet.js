export function sheets(layout) {
    const kinds = new Map(layout[0].records.map((record) => [record[0], record]));
    const places = layout[4].records;
    const names = new Map();
    const relations = [];
    for (const place of places.filter((record) => record[1] === '').sort((one, other) => Number(one[2]) - Number(other[2]))) {
        const relation = kinds.get(place[0]);
        const parts = layout[1].records.filter((record) => record[0] === place[0]).map((record) => doubled(record[2]));
        if (['instances', 'runs'].includes(relation[2])) {
            names.set(place[0], place[0]);
        }
        else {
            if (['input values', 'kind'].includes(relation[2])) {
                names.set(place[0], parts.join('.'));
            }
            else {
                names.set(place[0], [names.get(relation[1])].concat(parts).join('.'));
            }
        }
        const keys = relation[2] === 'runs' ? ['_input value', '_instance', '_page', '_line', '_position'] : relation[2] === 'input values' ? ['_input value'] : ['_input value', '_instance', '_parent', '_pointer'];
        const columns = places.filter((record) => record[0] === place[0] && record[1] !== '').sort((one, other) => Number(one[2]) - Number(other[2]));
        const labels = columns.map((record) => ['_type', '_value'].includes(record[1]) ? record[1] : layout[3].records.filter((part) => part[0] === place[0] && part[1] === record[1]).map((part) => doubled(part[3])).join('.'));
        relations.push({ 'sheet name': names.get(place[0]), header: keys.concat(labels), records: [] });
    }
    return relations;
}
function doubled(name) {
    return name.startsWith('_') ? '_' + name : name;
}
