export function order(schema, layout) {
    const root = tree(schema[0].records, schema[1].records);
    const visits = new Map();
    walk(root, '', visits);
    visits.set('_instances', visits.size);
    visits.set('_runs', visits.size);
    const places = [];
    for (const [place, relation] of layout[0].records.slice().sort((one, other) => (visits.get(one[0]) ?? visits.size) - (visits.get(other[0]) ?? visits.size)).entries()) {
        places.push([relation[0], '', String(place)]);
        for (const [position, column] of layout[1].records.filter((record) => record[0] === relation[0]).sort((one, other) => (visits.get(one[1]) ?? visits.size) - (visits.get(other[1]) ?? visits.size)).entries()) {
            places.push([relation[0], column[1], String(position)]);
        }
    }
    return { 'sheet name': 'places', header: ['location', 'column', 'place'], records: places };
}
function at(root, location) {
    let found = root;
    for (const token of location.split('/').slice(1)) {
        found = Array.isArray(found) ? found[Number(token)] : found.get(decoded(token));
    }
    return found;
}
function decoded(token) {
    return token.replaceAll('~1', '/').replaceAll('~0', '~');
}
function escaped(name) {
    return name.replaceAll('~', '~0').replaceAll('/', '~1');
}
function tree(instances, runs) {
    const texts = new Map();
    const places = new Map();
    for (const record of runs) {
        const before = places.get(record[0]) || [0, 0, 0];
        if (Number(record[1]) > before[0]) {
            texts.set(record[0], (texts.get(record[0]) || '') + '\f'.repeat(Number(record[1]) - before[0]) + '\n'.repeat(Number(record[2])) + '\t'.repeat(Number(record[3])));
        }
        else {
            if (Number(record[2]) > before[1]) {
                texts.set(record[0], (texts.get(record[0]) || '') + '\n'.repeat(Number(record[2]) - before[1]) + '\t'.repeat(Number(record[3])));
            }
            else {
                texts.set(record[0], (texts.get(record[0]) || '') + '\t'.repeat(Number(record[3]) - before[2]));
            }
        }
        texts.set(record[0], texts.get(record[0]) + record[4]);
        places.set(record[0], [Number(record[1]), Number(record[2]), Number(record[3])]);
    }
    const values = new Map();
    for (const record of instances) {
        values.set(record[0], typed(record[3], texts.has(record[0]) ? texts.get(record[0]) : record[4]));
        if (values.get(record[1]) instanceof Map) {
            values.get(record[1]).set(decoded(record[2].slice(1)), values.get(record[0]));
        }
        else {
            if (Array.isArray(values.get(record[1]))) {
                values.get(record[1]).push(values.get(record[0]));
            }
        }
    }
    return values.get(instances[0][0]);
}
function typed(type, text) {
    if (type === 'object') {
        return new Map();
    }
    if (type === 'array') {
        return [];
    }
    if (type === 'null') {
        return null;
    }
    if (type === 'boolean') {
        return text === 'true';
    }
    if (type === 'number') {
        return Number(text);
    }
    return text;
}
function walk(root, location, visits) {
    if (visits.has(location)) {
        return;
    }
    visits.set(location, visits.size);
    const found = at(root, location);
    if (!(found instanceof Map)) {
        return;
    }
    if (found.has('$ref')) {
        walk(root, decodeURIComponent(found.get('$ref').slice(1)), visits);
        return;
    }
    for (const keyword of ['properties', 'patternProperties', 'additionalProperties', 'items', 'additionalItems', 'anyOf', 'oneOf', 'if', 'then', 'else', 'dependencies', 'allOf']) {
        const held = found.get(keyword);
        if (held instanceof Map && ['properties', 'patternProperties', 'dependencies'].includes(keyword)) {
            for (const name of held.keys()) {
                walk(root, location + '/' + keyword + '/' + escaped(name), visits);
            }
        }
        else {
            if (Array.isArray(held)) {
                for (const index of held.keys()) {
                    walk(root, location + '/' + keyword + '/' + index, visits);
                }
            }
            else {
                if (found.has(keyword)) {
                    walk(root, location + '/' + keyword, visits);
                }
            }
        }
    }
}
