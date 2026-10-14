export function load(nodes) {
    const found = new Map();
    for (const [part, node, parent, kind, name, value] of nodes.records) {
        const key = part + '\t' + parent;
        if (!found.has(key)) {
            found.set(key, []);
        }
        found.get(key).push([node, kind, name.slice(name.lastIndexOf('}') + 1), value]);
    }
    const workbook = relations(found, '').find((relation) => relation[0] === 'officeDocument')[2];
    const targets = relations(found, workbook);
    let shared = [];
    for (const relation of targets) {
        if (relation[0] === 'sharedStrings') {
            shared = elements(found, relation[2], elements(found, relation[2], '', 'sst')[0], 'si').map((item) => string(found, relation[2], item));
        }
    }
    const sheets = [];
    const left = [];
    for (const sheet of elements(found, workbook, elements(found, workbook, elements(found, workbook, '', 'workbook')[0], 'sheets')[0], 'sheet')) {
        const held = attributes(found, workbook, sheet);
        const grid = records(found, targets.find((relation) => relation[1] === held.get('id'))[2], shared, left);
        if ([[held.get('name')], ...grid].some((record) => record.some((field) => Array.from('\t\n\f\r').some((character) => field.includes(character))))) {
            throw new CannotBeRepresentedError('cannot be represented');
        }
        sheets.push({ 'sheet name': held.get('name'), header: grid.length > 0 ? grid[0] : [], records: grid.slice(1) });
    }
    return [sheets, left];
}
export class CannotBeRepresentedError extends Error {}
export class FailedError extends Error {}
function attributes(found, part, node) {
    return new Map((found.get(part + '\t' + node) ?? []).filter((child) => child[1] === 'attribute').map((child) => [child[2], child[3]]));
}
function elements(found, part, node, name) {
    return (found.get(part + '\t' + node) ?? []).filter((child) => child[1] === 'element' && child[2] === name).map((child) => child[0]);
}
function position(reference) {
    let column = 0;
    let line = 0;
    for (const character of reference) {
        if ('0123456789'.includes(character)) {
            line = line * 10 + Number(character);
        }
        else {
            column = column * 26 + character.charCodeAt(0) - 64;
        }
    }
    return [column - 1, line - 1];
}
function records(found, part, shared, left) {
    const grid = [];
    for (const data of elements(found, part, elements(found, part, '', 'worksheet')[0], 'sheetData')) {
        for (const row of elements(found, part, data, 'row')) {
            for (const cell of elements(found, part, row, 'c')) {
                const held = attributes(found, part, cell);
                const place = position(held.get('r'));
                let content = elements(found, part, cell, 'v').map((value) => text(found, part, value)).join('');
                if (held.get('t') === 's') {
                    content = shared[Number(content)];
                }
                else {
                    if (held.get('t') === 'inlineStr') {
                        content = elements(found, part, cell, 'is').map((inline) => string(found, part, inline)).join('');
                    }
                }
                while (grid.length <= place[1]) {
                    grid.push([]);
                }
                while (grid[place[1]].length <= place[0]) {
                    grid[place[1]].push('');
                }
                grid[place[1]][place[0]] = content;
                if (held.has('t')) {
                    left.push(held.get('r') + ' t');
                }
                if (elements(found, part, cell, 'f').length > 0) {
                    left.push(held.get('r') + ' f');
                }
                if (held.has('s')) {
                    left.push(held.get('r') + ' s');
                }
            }
        }
    }
    return grid;
}
function relations(found, part) {
    const place = part.slice(0, part.lastIndexOf('/') + 1);
    const pathname = place + '_rels/' + part.slice(part.lastIndexOf('/') + 1) + '.rels';
    const listed = [];
    for (const relationship of elements(found, pathname, elements(found, pathname, '', 'Relationships')[0], 'Relationship')) {
        const held = attributes(found, pathname, relationship);
        const target = held.get('Target').startsWith('/') ? held.get('Target').slice(1) : place + held.get('Target');
        if (!Array.from(found.keys()).some((key) => key.startsWith(target + '\t'))) {
            throw new FailedError('failed');
        }
        listed.push([held.get('Type').slice(held.get('Type').lastIndexOf('/') + 1), held.get('Id'), target]);
    }
    return listed;
}
function string(found, part, node) {
    let content = '';
    for (const child of found.get(part + '\t' + node) ?? []) {
        if (child[1] === 'element' && child[2] === 't') {
            content = content + text(found, part, child[0]);
        }
        else {
            if (child[1] === 'element' && child[2] === 'r') {
                content = content + string(found, part, child[0]);
            }
        }
    }
    return content;
}
function text(found, part, node) {
    return (found.get(part + '\t' + node) ?? []).filter((child) => child[1] === 'text').map((child) => child[3]).join('');
}
