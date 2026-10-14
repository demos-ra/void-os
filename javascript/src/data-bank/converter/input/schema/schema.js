export function schema(moduleSpecification, relationalModel) {
    let found;
    try {
        found = relationalModel.instances(moduleSpecification);
    }
    catch (error) {
        if (error instanceof relationalModel.NotAJSONTextError) {
            throw new NonConformingError('module specification: ' + error.message);
        }
        if (error instanceof relationalModel.NamesNotUniqueError) {
            throw new NonConformingError('module specification: ' + error.message);
        }
        throw error;
    }
    const root = tree(found[0].records, found[1].records);
    const meta = relationalModel.instances((new TextEncoder()).encode(metaschema()));
    const outcome = applied(tree(meta[0].records, meta[1].records)[0], root);
    if (!outcome[0]) {
        throw new NonConformingError('module specification: not a draft-07 schema, at "' + outcome[2] + '"');
    }
    rules(root[0]);
    return [found[0], found[1]];
}
export function validate(schema, values, relationalModel) {
    const root = tree(schema[0].records, schema[1].records);
    const annotations = [];
    for (const position of new Set(values[0].records.map((record) => record[0]))) {
        const outcome = applied(root[0], tree(values[0].records.filter((record) => record[0] === position).map((record) => record.slice(1)), values[1].records.filter((record) => record[0] === position).map((record) => record.slice(1))));
        if (!outcome[0]) {
            throw new NonConformingError(position + ' ' + '#' + percentEncoding(outcome[2]));
        }
        annotations.push(...outcome[1].map(([instance, location, valid]) => [position, instance, location, valid ? 'true' : 'false']));
    }
    return { 'sheet name': 'annotations', header: ['_input value', '_instance', 'location', 'valid'], records: annotations };
}
export class NonConformingError extends Error {}
function applied(schema, given) {
    const records = [];
    const failing = [];
    function valid(at, location, instance, path) {
        let result = true;
        if (typeof at === 'boolean') {
            result = at;
        }
        else {
            if ('$ref' in at) {
                const pointer = decodeURIComponent(at.$ref.slice(1));
                result = valid(resolved(schema, pointer), pointer, instance, path);
            }
            else {
                const type = kind(instance);
                const named = Array.isArray(at.type) ? at.type : 'type' in at ? [at.type] : [];
                if (named.length > 0 && !named.includes(type) && !(named.includes('integer') && type === 'number' && Number.isInteger(instance))) {
                    result = false;
                }
                if ('enum' in at && !at.enum.some((each) => equal(instance, each))) {
                    result = false;
                }
                if ('const' in at && !equal(instance, at.const)) {
                    result = false;
                }
                if ('multipleOf' in at && type === 'number' && !Number.isInteger(instance / at.multipleOf)) {
                    result = false;
                }
                if ('maximum' in at && type === 'number' && instance > at.maximum) {
                    result = false;
                }
                if ('exclusiveMaximum' in at && type === 'number' && instance >= at.exclusiveMaximum) {
                    result = false;
                }
                if ('minimum' in at && type === 'number' && instance < at.minimum) {
                    result = false;
                }
                if ('exclusiveMinimum' in at && type === 'number' && instance <= at.exclusiveMinimum) {
                    result = false;
                }
                if ('maxLength' in at && type === 'string' && [...instance].length > at.maxLength) {
                    result = false;
                }
                if ('minLength' in at && type === 'string' && [...instance].length < at.minLength) {
                    result = false;
                }
                if ('pattern' in at && type === 'string' && !new RegExp(at.pattern, 'u').test(instance)) {
                    result = false;
                }
                if (Array.isArray(at.items) && type === 'array' && !at.items.slice(0, instance.length).map((each, index) => valid(each, location + '/items/' + index, instance[index], path + '/' + index)).every((each) => each)) {
                    result = false;
                }
                if ('items' in at && !Array.isArray(at.items) && type === 'array' && !instance.map((each, index) => valid(at.items, location + '/items', each, path + '/' + index)).every((each) => each)) {
                    result = false;
                }
                if ('additionalItems' in at && Array.isArray(at.items) && type === 'array' && !instance.slice(at.items.length).map((each, index) => valid(at.additionalItems, location + '/additionalItems', each, path + '/' + (index + at.items.length))).every((each) => each)) {
                    result = false;
                }
                if ('maxItems' in at && type === 'array' && instance.length > at.maxItems) {
                    result = false;
                }
                if ('minItems' in at && type === 'array' && instance.length < at.minItems) {
                    result = false;
                }
                if (at.uniqueItems === true && type === 'array' && instance.some((each, index) => instance.slice(0, index).some((other) => equal(each, other)))) {
                    result = false;
                }
                if ('contains' in at && type === 'array' && !instance.map((each, index) => valid(at.contains, location + '/contains', each, path + '/' + index)).some((each) => each)) {
                    result = false;
                }
                if ('maxProperties' in at && type === 'object' && Object.keys(instance).length > at.maxProperties) {
                    result = false;
                }
                if ('minProperties' in at && type === 'object' && Object.keys(instance).length < at.minProperties) {
                    result = false;
                }
                if ('required' in at && type === 'object' && !at.required.every((name) => name in instance)) {
                    result = false;
                }
                if ('properties' in at && type === 'object' && !Object.keys(at.properties).filter((name) => name in instance).map((name) => valid(at.properties[name], location + '/properties/' + escaped(name), instance[name], path + '/' + escaped(name))).every((each) => each)) {
                    result = false;
                }
                if ('patternProperties' in at && type === 'object' && !Object.keys(at.patternProperties).flatMap((pattern) => Object.keys(instance).filter((name) => new RegExp(pattern, 'u').test(name)).map((name) => valid(at.patternProperties[pattern], location + '/patternProperties/' + escaped(pattern), instance[name], path + '/' + escaped(name)))).every((each) => each)) {
                    result = false;
                }
                if ('additionalProperties' in at && type === 'object' && !Object.keys(instance).filter((name) => !Object.keys(at.properties || {}).includes(name) && !Object.keys(at.patternProperties || {}).some((pattern) => new RegExp(pattern, 'u').test(name))).map((name) => valid(at.additionalProperties, location + '/additionalProperties', instance[name], path + '/' + escaped(name))).every((each) => each)) {
                    result = false;
                }
                if ('dependencies' in at && type === 'object' && !Object.keys(at.dependencies).filter((name) => name in instance).map((name) => Array.isArray(at.dependencies[name]) ? at.dependencies[name].every((other) => other in instance) : valid(at.dependencies[name], location + '/dependencies/' + escaped(name), instance, path)).every((each) => each)) {
                    result = false;
                }
                if ('propertyNames' in at && type === 'object' && !Object.keys(instance).map((name) => valid(at.propertyNames, location + '/propertyNames', name, path)).every((each) => each)) {
                    result = false;
                }
                const condition = 'if' in at ? valid(at.if, location + '/if', instance, path) : null;
                if ('then' in at && condition === true && !valid(at.then, location + '/then', instance, path)) {
                    result = false;
                }
                if ('else' in at && condition === false && !valid(at.else, location + '/else', instance, path)) {
                    result = false;
                }
                if ('allOf' in at && !at.allOf.map((each, index) => valid(each, location + '/allOf/' + index, instance, path)).every((each) => each)) {
                    result = false;
                }
                if ('anyOf' in at && !at.anyOf.map((each, index) => valid(each, location + '/anyOf/' + index, instance, path)).some((each) => each)) {
                    result = false;
                }
                if ('oneOf' in at && at.oneOf.map((each, index) => valid(each, location + '/oneOf/' + index, instance, path)).filter((each) => each).length !== 1) {
                    result = false;
                }
                if ('not' in at && valid(at.not, location + '/not', instance, path)) {
                    result = false;
                }
            }
        }
        records.push([given[1].get(path), location, result]);
        if (!result) {
            failing.push(path);
        }
        return result;
    }
    const result = valid(schema, '', given[0], '');
    let deepest = '';
    for (const path of failing) {
        if (path.split('/').length > deepest.split('/').length) {
            deepest = path;
        }
    }
    return [result, records, deepest];
}
function decoded(token) {
    return token.replaceAll('~1', '/').replaceAll('~0', '~');
}
function equal(left, right) {
    if (kind(left) !== kind(right)) {
        return false;
    }
    if (Array.isArray(left)) {
        return left.length === right.length && left.every((each, index) => equal(each, right[index]));
    }
    if (kind(left) === 'object') {
        return Object.keys(left).length === Object.keys(right).length && Object.keys(left).every((name) => name in right && equal(left[name], right[name]));
    }
    return left === right;
}
function escaped(name) {
    return name.replaceAll('~', '~0').replaceAll('/', '~1');
}
const fragment = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$&'()*+,;=:@/?";
function kind(instance) {
    if (instance === null) {
        return 'null';
    }
    if (Array.isArray(instance)) {
        return 'array';
    }
    if (typeof instance === 'object') {
        return 'object';
    }
    return typeof instance;
}
function limited(pattern) {
    let depth = 0;
    let index = 0;
    let quantifiable = false;
    while (index < pattern.length) {
        const character = pattern[index];
        if (character === '\\' && !new RegExp('^[^0-9A-Za-z]$', 'u').test(pattern.slice(index + 1, index + 2))) {
            return false;
        }
        if (character === '\\') {
            index += 2;
            quantifiable = true;
        }
        else {
            if (character === '[') {
                const found = new RegExp('^\\[\\^?(\\\\[^0-9A-Za-z]|[^\\\\\\]])+\\]', 'u').exec(pattern.slice(index));
                if (found === null) {
                    return false;
                }
                index += found[0].length;
                quantifiable = true;
            }
            else {
                if (character === '(') {
                    if (pattern.slice(index + 1, index + 2) === '?') {
                        return false;
                    }
                    depth += 1;
                    index += 1;
                    quantifiable = false;
                }
                else {
                    if (character === ')') {
                        depth -= 1;
                        if (depth < 0) {
                            return false;
                        }
                        index += 1;
                        quantifiable = true;
                    }
                    else {
                        if ('+*?{'.includes(character)) {
                            const found = new RegExp('^([+*?]|\\{[0-9]+(,[0-9]*)?\\})\\??', 'u').exec(pattern.slice(index));
                            if (found === null || !quantifiable) {
                                return false;
                            }
                            index += found[0].length;
                            quantifiable = false;
                        }
                        else {
                            if ('|^$'.includes(character)) {
                                index += 1;
                                quantifiable = false;
                            }
                            else {
                                if ('.]}'.includes(character)) {
                                    return false;
                                }
                                else {
                                    index += 1;
                                    quantifiable = true;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    try {
        new RegExp(pattern, 'u');
    }
    catch {
        return false;
    }
    return depth === 0;
}
function loops(root, location, seen) {
    if (seen.includes(location)) {
        return true;
    }
    const at = resolved(root, location);
    if (kind(at) !== 'object') {
        return false;
    }
    if ('$ref' in at) {
        return loops(root, decodeURIComponent(at.$ref.slice(1)), [...seen, location]);
    }
    const places = ['allOf', 'anyOf', 'oneOf'].flatMap((name) => (Array.isArray(at[name]) ? at[name] : []).map((each, index) => location + '/' + name + '/' + index)).concat(['not', 'if', 'then', 'else'].filter((name) => name in at).map((name) => location + '/' + name), Object.keys(at.dependencies || {}).filter((name) => !Array.isArray(at.dependencies[name])).map((name) => location + '/dependencies/' + escaped(name)));
    return places.some((place) => loops(root, place, [...seen, location]));
}
function metaschema() {
    return '{"$schema":"http://json-schema.org/draft-07/schema#","$id":"http://json-schema.org/draft-07/schema#","title":"Core schema meta-schema","definitions":{"schemaArray":{"type":"array","minItems":1,"items":{"$ref":"#"}},"nonNegativeInteger":{"type":"integer","minimum":0},"nonNegativeIntegerDefault0":{"allOf":[{"$ref":"#/definitions/nonNegativeInteger"},{"default":0}]},"simpleTypes":{"enum":["array","boolean","integer","null","number","object","string"]},"stringArray":{"type":"array","items":{"type":"string"},"uniqueItems":true,"default":[]}},"type":["object","boolean"],"properties":{"$id":{"type":"string","format":"uri-reference"},"$schema":{"type":"string","format":"uri"},"$ref":{"type":"string","format":"uri-reference"},"$comment":{"type":"string"},"title":{"type":"string"},"description":{"type":"string"},"default":true,"readOnly":{"type":"boolean","default":false},"writeOnly":{"type":"boolean","default":false},"examples":{"type":"array","items":true},"multipleOf":{"type":"number","exclusiveMinimum":0},"maximum":{"type":"number"},"exclusiveMaximum":{"type":"number"},"minimum":{"type":"number"},"exclusiveMinimum":{"type":"number"},"maxLength":{"$ref":"#/definitions/nonNegativeInteger"},"minLength":{"$ref":"#/definitions/nonNegativeIntegerDefault0"},"pattern":{"type":"string","format":"regex"},"additionalItems":{"$ref":"#"},"items":{"anyOf":[{"$ref":"#"},{"$ref":"#/definitions/schemaArray"}],"default":true},"maxItems":{"$ref":"#/definitions/nonNegativeInteger"},"minItems":{"$ref":"#/definitions/nonNegativeIntegerDefault0"},"uniqueItems":{"type":"boolean","default":false},"contains":{"$ref":"#"},"maxProperties":{"$ref":"#/definitions/nonNegativeInteger"},"minProperties":{"$ref":"#/definitions/nonNegativeIntegerDefault0"},"required":{"$ref":"#/definitions/stringArray"},"additionalProperties":{"$ref":"#"},"definitions":{"type":"object","additionalProperties":{"$ref":"#"},"default":{}},"properties":{"type":"object","additionalProperties":{"$ref":"#"},"default":{}},"patternProperties":{"type":"object","additionalProperties":{"$ref":"#"},"propertyNames":{"format":"regex"},"default":{}},"dependencies":{"type":"object","additionalProperties":{"anyOf":[{"$ref":"#"},{"$ref":"#/definitions/stringArray"}]}},"propertyNames":{"$ref":"#"},"const":true,"enum":{"type":"array","items":true,"minItems":1,"uniqueItems":true},"type":{"anyOf":[{"$ref":"#/definitions/simpleTypes"},{"type":"array","items":{"$ref":"#/definitions/simpleTypes"},"minItems":1,"uniqueItems":true}]},"format":{"type":"string"},"contentMediaType":{"type":"string"},"contentEncoding":{"type":"string"},"if":{"$ref":"#"},"then":{"$ref":"#"},"else":{"$ref":"#"},"allOf":{"$ref":"#/definitions/schemaArray"},"anyOf":{"$ref":"#/definitions/schemaArray"},"oneOf":{"$ref":"#/definitions/schemaArray"},"not":{"$ref":"#"}},"default":true}';
}
function percentEncoding(text) {
    return [...text].map((character) => fragment.includes(character) ? character : [...new TextEncoder().encode(character)].map((octet) => '%' + octet.toString(16).toUpperCase().padStart(2, '0')).join('')).join('');
}
function resolved(root, pointer) {
    let found = root;
    for (const token of pointer.split('/').slice(1)) {
        found = Array.isArray(found) ? found[Number(token)] : found[decoded(token)];
    }
    return found;
}
function rules(root) {
    if (kind(root) !== 'object' || typeof root.title !== 'string') {
        throw new NonConformingError('module specification: the root schema holds no title');
    }
    const found = schemas(root, '');
    const places = found.map(([place]) => place);
    for (const [location, at] of found) {
        if ('$ref' in at && !at.$ref.startsWith('#')) {
            throw new NonConformingError('module specification: a $ref outside it, at "' + location + '"');
        }
        if ('$ref' in at && !new RegExp("^#(/([A-Za-z0-9\\-._~!$&'()*+,;=:@/?]|%[0-9A-Fa-f]{2})*)?$", 'u').test(at.$ref)) {
            throw new NonConformingError('module specification: a $ref fragment not a JSON Pointer, at "' + location + '"');
        }
        if ('$ref' in at && !places.includes(decodeURIComponent(at.$ref.slice(1)))) {
            throw new NonConformingError('module specification: a $ref to no schema of it, at "' + location + '"');
        }
        const names = [at.title || '', ...Object.keys(at.properties || {}), ...Object.keys(at.patternProperties || {}), ...Object.keys(at.dependencies || {}), decoded(decodeURIComponent(at.$ref || '').split('/').pop())];
        if (names.some((name) => new RegExp('[\t\n\f\r]', 'u').test(name))) {
            throw new NonConformingError('module specification: a name holds HT, LF, FF or CR, at "' + location + '"');
        }
        if (![...Object.keys(at.patternProperties || {}), at.pattern || ''].every((pattern) => limited(pattern))) {
            throw new NonConformingError('module specification: a pattern outside the limited syntax, at "' + location + '"');
        }
    }
    for (const [location] of found) {
        if (loops(root, location, [])) {
            throw new NonConformingError('module specification: a $ref reaches again a schema it is applied from, at "' + location + '"');
        }
    }
}
function schemas(at, location) {
    if (kind(at) !== 'object') {
        return [];
    }
    const found = [[location, at]];
    for (const name of ['additionalItems', 'additionalProperties', 'contains', 'else', 'if', 'items', 'not', 'propertyNames', 'then']) {
        found.push(...schemas(at[name], location + '/' + name));
    }
    for (const name of ['allOf', 'anyOf', 'items', 'oneOf']) {
        found.push(...(Array.isArray(at[name]) ? at[name] : []).flatMap((each, index) => schemas(each, location + '/' + name + '/' + index)));
    }
    for (const name of ['definitions', 'dependencies', 'patternProperties', 'properties']) {
        found.push(...Object.keys(kind(at[name]) === 'object' ? at[name] : {}).flatMap((key) => schemas(at[name][key], location + '/' + name + '/' + escaped(key))));
    }
    return found;
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
    const paths = new Map();
    const ids = new Map();
    for (const record of instances) {
        values.set(record[0], typed(record[3], texts.has(record[0]) ? texts.get(record[0]) : record[4]));
        paths.set(record[0], (paths.get(record[1]) || '') + record[2]);
        ids.set(paths.get(record[0]), record[0]);
        if (kind(values.get(record[1])) === 'object') {
            values.get(record[1])[decoded(record[2].slice(1))] = values.get(record[0]);
        }
        else {
            if (Array.isArray(values.get(record[1]))) {
                values.get(record[1]).push(values.get(record[0]));
            }
        }
    }
    return [values.get(instances[0][0]), ids];
}
function typed(type, text) {
    if (type === 'object') {
        return Object.create(null);
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
