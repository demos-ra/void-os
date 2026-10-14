export function relations(schema, input) {
    const root = tree(schema[0].records, schema[1].records);
    const layout = { relations: [], 'name parts': [], columns: [], 'column parts': [], rows: new Map(), molten: false, runs: types(root, '').includes('string') };
    const top = ['object', 'array'].includes(types(root, '').join()) ? sheet(root, '', '', '', 'input values', part(root, '', []), layout) : ['molten'];
    if (top[0] === 'molten' || layout.molten) {
        relation('_instances', '', 'instances', [], layout);
        column('_instances', '_type', ['_type'], layout);
        column('_instances', '_value', ['_value'], layout);
    }
    if (layout.runs) {
        relation('_runs', '', 'runs', [], layout);
        column('_runs', '_value', ['_value'], layout);
    }
    const rows = layout.rows;
    const valid = new Set(input[2].records.filter((record) => record[3] === 'true').map((record) => record[0] + '\n' + record[1] + '\n' + record[2]));
    const records = [];
    const cells = [];
    let position = '';
    let children = new Map();
    function place(instance, destination, holder) {
        if (destination[0] === 'record') {
            records.push([destination[1], position, instance, holder]);
            fill(instance, rows.get(destination[1]), destination[1]);
        }
        else {
            if (destination[0] === 'elements') {
                for (const each of children.get(instance) || []) {
                    place(each[1], destination[1], holder);
                }
            }
            else {
                if (destination[0] === 'molten') {
                    melt(instance, holder);
                }
                else {
                    if (destination[0] === 'pick') {
                        const chosen = destination[1].filter((each) => valid.has(position + '\n' + instance + '\n' + each[0])).map((each) => each[1]);
                        if (chosen.length > 0) {
                            place(instance, chosen[0], holder);
                        }
                    }
                }
            }
        }
    }
    function melt(instance, holder) {
        records.push(['_instances', position, instance, holder]);
        cells.push(['_instances', position, instance, '_type', instance]);
        cells.push(['_instances', position, instance, '_value', instance]);
        for (const each of children.get(instance) || []) {
            melt(each[1], instance);
        }
    }
    function fill(instance, entry, owner) {
        if (entry.kind === 'value') {
            cells.push([owner, position, instance, '_value', instance]);
        }
        else {
            if (entry.kind === 'object') {
                write(instance, entry, owner, instance);
            }
            else {
                for (const [index, each] of (children.get(instance) || []).entries()) {
                    const destination = entry.items || (index < entry.positions.length ? entry.positions[index] : entry.rest);
                    if (destination) {
                        place(each[1], destination, instance);
                    }
                }
            }
        }
    }
    function write(instance, entry, owner, record) {
        const writers = [[entry, owner, record]].concat(entry.branches.filter((each) => valid.has(position + '\n' + instance + '\n' + each[0])).map((each) => [rows.get(each[1]), each[1], instance]));
        for (const writer of writers.slice(1)) {
            records.push([writer[1], position, instance, '']);
        }
        for (const [name, child] of children.get(instance) || []) {
            const covering = writers.flatMap((writer) => (writer[0].members.has(name) ? [writer[0].members.get(name)] : []).concat(writer[0].patterns.filter((each) => new RegExp(each[0], 'u').test(name)).map((each) => each[1])).map((rule) => [rule, writer])).concat(writers.filter((writer) => writer[0].additional).map((writer) => [writer[0].additional, writer]));
            if (covering.length > 0) {
                const [rule, writer] = covering[0];
                if (rule[0] === 'column') {
                    cells.push([writer[1], position, writer[2], rule[1], child]);
                }
                else {
                    if (rule[0] === 'inline') {
                        write(child, rule[1], writer[1], writer[2]);
                    }
                    else {
                        place(child, rule, writer[2]);
                    }
                }
            }
            else {
                melt(child, record);
            }
        }
    }
    for (const each of new Set(input[0].records.map((record) => record[0]))) {
        position = each;
        const held = input[0].records.filter((record) => record[0] === position);
        children = new Map();
        for (const record of held) {
            if (record[2] !== '') {
                if (!children.has(record[2])) {
                    children.set(record[2], []);
                }
                children.get(record[2]).push([decoded(record[3].slice(1)), record[1]]);
            }
        }
        place(held[0][1], top, '');
    }
    for (const key of new Set(input[1].records.map((record) => record[0] + '\n' + record[1]))) {
        records.push(['_runs'].concat(key.split('\n'), ['']));
    }
    return [{ 'sheet name': 'relations', header: ['location', 'parent', 'kind'], records: layout.relations }, { 'sheet name': 'name parts', header: ['location', 'position', 'part'], records: layout['name parts'] }, { 'sheet name': 'columns', header: ['location', 'column'], records: layout.columns }, { 'sheet name': 'column parts', header: ['location', 'column', 'position', 'part'], records: layout['column parts'] }, { 'sheet name': 'records', header: ['location', '_input value', '_instance', 'holder'], records: records }, { 'sheet name': 'cells', header: ['location', '_input value', '_instance', 'column', 'value'], records: cells }];
}
function at(root, location) {
    let found = root;
    for (const token of location.split('/').slice(1)) {
        found = Array.isArray(found) ? found[Number(token)] : found.get(decoded(token));
    }
    return found;
}
function branch(root, entry, owner, location, parts, layout) {
    if (types(root, location).join() === 'object') {
        const destination = sheet(root, location, location, owner, 'branch', parts, layout);
        if (destination[0] === 'record') {
            entry.branches.push([location, destination[1]]);
        }
    }
}
function column(owner, name, parts, layout) {
    layout.columns.push([owner, name]);
    layout['column parts'].push(...parts.map((each, index) => [owner, name, String(index), each]));
}
function decoded(token) {
    return token.replaceAll('~1', '/').replaceAll('~0', '~');
}
function escaped(name) {
    return name.replaceAll('~', '~0').replaceAll('/', '~1');
}
function kind(root, location, owner, layout) {
    const pointer = decodeURIComponent(at(root, location).get('$ref').slice(1));
    if (layout.rows.has(pointer)) {
        for (const each of layout.relations) {
            if (each[0] === pointer) {
                each[2] = 'kind';
            }
        }
        return ['record', pointer];
    }
    const found = at(root, pointer);
    const name = found instanceof Map && typeof found.get('title') === 'string' ? found.get('title') : decoded(pointer.split('/').pop());
    return sheet(root, pointer, pointer, owner, 'kind', [name], layout);
}
function member(root, owner, location, required, label, parts, role, layout) {
    const found = at(root, location);
    if (found instanceof Map && found.has('$ref')) {
        return kind(root, location, owner, layout);
    }
    const allowed = types(root, location);
    if (allowed.includes('string')) {
        layout.runs = true;
    }
    const scopes = owns(root, location).filter((own) => at(root, own) instanceof Map);
    const inline = required && allowed.join() === 'object' && scopes.slice(1).every((own) => types(root, own).join() === 'object');
    const branches = found instanceof Map ? ['anyOf', 'oneOf'].flatMap((keyword) => (found.get(keyword) || []).map((each, index) => [keyword, String(index)])) : [];
    if (branches.length > 0 && (allowed.length !== 1 || allowed.join() === 'object' && !inline && !scopes.some((own) => ['properties', 'patternProperties', 'additionalProperties'].some((word) => at(root, own).has(word))))) {
        return ['pick', branches.map((each) => [location + '/' + each[0] + '/' + each[1], member(root, owner, location + '/' + each[0] + '/' + each[1], false, label, parts.concat([each[0]], part(root, location + '/' + each[0] + '/' + each[1], found.get(each[0]).length > 1 ? [each[1]] : [])), 'branch', layout)])];
    }
    if (allowed.length === 1 && ['string', 'number', 'boolean', 'null'].includes(allowed[0])) {
        if (required) {
            column(owner, location, label, layout);
            return ['column', location];
        }
        layout.molten = true;
        return ['molten'];
    }
    if (inline) {
        return ['inline', object(root, owner, location, label, parts, layout)];
    }
    return target(root, owner, location, role, parts, layout);
}
function object(root, owner, location, label, parts, layout) {
    const entry = { kind: 'object', members: new Map(), patterns: [], additional: null, branches: [] };
    const scopes = owns(root, location).filter((own) => at(root, own) instanceof Map);
    const required = scopes.flatMap((own) => at(root, own).get('required') || []);
    for (const own of scopes) {
        const found = at(root, own);
        for (const name of (found.get('properties') || new Map()).keys()) {
            if (!entry.members.has(name)) {
                entry.members.set(name, member(root, owner, own + '/properties/' + escaped(name), required.includes(name), label.concat([name]), parts.concat([name]), 'property', layout));
            }
        }
        for (const pattern of (found.get('patternProperties') || new Map()).keys()) {
            entry.patterns.push([pattern, sheet(root, own + '/patternProperties/' + escaped(pattern), own + '/patternProperties/' + escaped(pattern), owner, 'keyword', parts.concat(['patternProperties'], found.get('patternProperties').size > 1 ? [pattern] : []), layout)]);
        }
        if (found.has('additionalProperties') && entry.additional === null) {
            entry.additional = sheet(root, own + '/additionalProperties', own + '/additionalProperties', owner, 'keyword', parts.concat(['additionalProperties']), layout);
        }
        for (const keyword of ['anyOf', 'oneOf']) {
            for (const index of (found.get(keyword) || []).keys()) {
                branch(root, entry, owner, own + '/' + keyword + '/' + index, parts.concat([keyword], part(root, own + '/' + keyword + '/' + index, found.get(keyword).length > 1 ? [String(index)] : [])), layout);
            }
        }
        for (const keyword of ['if', 'then', 'else']) {
            if (found.has(keyword)) {
                branch(root, entry, owner, own + '/' + keyword, parts.concat([keyword], part(root, own + '/' + keyword, [])), layout);
            }
        }
        for (const [key, value] of found.get('dependencies') || new Map()) {
            if (!Array.isArray(value)) {
                branch(root, entry, owner, own + '/dependencies/' + escaped(key), parts.concat(['dependencies'], part(root, own + '/dependencies/' + escaped(key), [key])), layout);
            }
        }
    }
    if (!scopes.some((own) => at(root, own).has('additionalProperties'))) {
        layout.molten = true;
        layout.runs = true;
    }
    return entry;
}
function owns(root, location) {
    const found = at(root, location);
    if (found instanceof Map && found.has('$ref')) {
        return owns(root, decodeURIComponent(found.get('$ref').slice(1)));
    }
    return [location].concat(found instanceof Map ? (found.get('allOf') || []).flatMap((each, index) => owns(root, location + '/allOf/' + index)) : []);
}
function part(root, location, fallback) {
    const found = at(root, location);
    return found instanceof Map && typeof found.get('title') === 'string' ? [found.get('title')] : fallback;
}
function relation(location, parent, role, parts, layout) {
    layout.relations.push([location, parent, role]);
    layout['name parts'].push(...parts.map((each, index) => [location, String(index), each]));
}
function row(root, owner, location, layout) {
    const allowed = types(root, location);
    const found = at(root, location);
    if (allowed.join() === 'object') {
        return object(root, owner, location, [], [], layout);
    }
    if (allowed.join() === 'array' && Array.isArray(found.get('items'))) {
        return { kind: 'array', items: null, positions: found.get('items').map((each, index) => sheet(root, location + '/items/' + index, location + '/items/' + index, owner, 'keyword', ['items'].concat(found.get('items').length > 1 ? [String(index)] : []), layout)), rest: found.has('additionalItems') ? sheet(root, location + '/additionalItems', location + '/additionalItems', owner, 'keyword', ['additionalItems'], layout) : null };
    }
    if (allowed.join() === 'array' && found.has('items')) {
        return { kind: 'array', items: sheet(root, location + '/items', location + '/items', owner, 'keyword', ['items'], layout), positions: [], rest: null };
    }
    if (allowed.join() === 'array') {
        layout.molten = true;
        layout.runs = true;
        return { kind: 'array', items: ['molten'], positions: [], rest: null };
    }
    column(owner, '_value', ['_value'], layout);
    return { kind: 'value' };
}
function sheet(root, location, schema, owner, role, parts, layout) {
    if (layout.rows.has(location)) {
        return ['record', location];
    }
    const found = at(root, schema);
    if (found instanceof Map && found.has('$ref')) {
        return kind(root, schema, owner, layout);
    }
    const allowed = types(root, schema);
    if (allowed.includes('string')) {
        layout.runs = true;
    }
    if (allowed.length > 1) {
        layout.molten = true;
        return ['molten'];
    }
    if (allowed.length === 0) {
        return ['none'];
    }
    relation(location, owner, role, parts, layout);
    layout.rows.set(location, null);
    layout.rows.set(location, row(root, location, schema, layout));
    return ['record', location];
}
function target(root, owner, location, role, parts, layout) {
    const found = at(root, location);
    if (types(root, location).join() === 'array' && found instanceof Map && !Array.isArray(found.get('items'))) {
        if (found.has('items')) {
            return ['elements', sheet(root, location, location + '/items', owner, role, parts, layout)];
        }
        layout.molten = true;
        layout.runs = true;
        return ['elements', ['molten']];
    }
    return sheet(root, location, location, owner, role, parts, layout);
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
function types(root, location) {
    const found = at(root, location);
    if (typeof found === 'boolean') {
        return found ? ['array', 'boolean', 'null', 'number', 'object', 'string'] : [];
    }
    if (found.has('$ref')) {
        return types(root, decodeURIComponent(found.get('$ref').slice(1)));
    }
    const named = Array.isArray(found.get('type')) ? found.get('type') : found.has('type') ? [found.get('type')] : ['array', 'boolean', 'null', 'number', 'object', 'string'];
    let allowed = ['array', 'boolean', 'null', 'number', 'object', 'string'].filter((each) => named.includes(each) || each === 'number' && named.includes('integer'));
    for (const index of (found.get('allOf') || []).keys()) {
        allowed = allowed.filter((each) => types(root, location + '/allOf/' + index).includes(each));
    }
    for (const keyword of ['anyOf', 'oneOf']) {
        if (found.has(keyword)) {
            allowed = allowed.filter((each) => found.get(keyword).some((option, index) => types(root, location + '/' + keyword + '/' + index).includes(each)));
        }
    }
    return allowed;
}
