export function load(nodes) {
    const found = new Map();
    for (const [part, node, parent, kind, name, value] of nodes.records) {
        if (part === 'content.xml') {
            if (!found.has(parent)) {
                found.set(parent, []);
            }
            found.get(parent).push([node, kind, name.slice(name.lastIndexOf('}') + 1), value]);
        }
    }
    if (found.size === 0) {
        throw new FailedError('failed');
    }
    const sheets = [];
    const left = [];
    for (const body of elements(found, elements(found, '', 'document-content')[0], 'body')) {
        if (elements(found, body, 'spreadsheet').length === 0) {
            throw new FailedError('failed');
        }
        for (const spreadsheet of elements(found, body, 'spreadsheet')) {
            for (const table of elements(found, spreadsheet, 'table')) {
                const title = attributes(found, table).get('name');
                const grid = records(found, table, left);
                if ([[title], ...grid].some((record) => record.some((field) => Array.from('\t\n\f\r').some((character) => field.includes(character))))) {
                    throw new CannotBeRepresentedError('cannot be represented');
                }
                sheets.push({ 'sheet name': title, header: grid.length > 0 ? grid[0] : [], records: grid.slice(1) });
            }
        }
    }
    return [sheets, left];
}
export class CannotBeRepresentedError extends Error {}
export class FailedError extends Error {}
function attributes(found, node) {
    return new Map((found.get(node) ?? []).filter((child) => child[1] === 'attribute').map((child) => [child[2], child[3]]));
}
function elements(found, node, name) {
    return (found.get(node) ?? []).filter((child) => child[1] === 'element' && child[2] === name).map((child) => child[0]);
}
function paragraph(found, node) {
    let content = '';
    for (const child of found.get(node) ?? []) {
        if (child[1] === 'text') {
            content = content + child[3];
        }
        else {
            if (child[1] === 'element' && child[2] === 's') {
                content = content + ' '.repeat(Number(attributes(found, child[0]).get('c') ?? '1'));
            }
            else {
                if (child[1] === 'element' && child[2] === 'tab') {
                    content = content + '\t';
                }
                else {
                    if (child[1] === 'element' && child[2] === 'line-break') {
                        content = content + '\n';
                    }
                    else {
                        if (child[1] === 'element') {
                            content = content + paragraph(found, child[0]);
                        }
                    }
                }
            }
        }
    }
    return content;
}
function records(found, table, left) {
    const grid = [];
    let line = 0;
    for (const row of rows(found, table)) {
        const cells = [];
        for (const cell of found.get(row) ?? []) {
            if (cell[1] === 'element' && ['table-cell', 'covered-table-cell'].includes(cell[2])) {
                const held = attributes(found, cell[0]);
                cells.push([Number(held.get('number-columns-repeated') ?? '1'), elements(found, cell[0], 'p').map((item) => paragraph(found, item)).join('\n'), ['office:value-type', 'office:value', 'office:date-value', 'office:time-value', 'office:boolean-value', 'office:string-value', 'table:formula', 'table:style-name'].filter((label) => held.has(label.slice(label.indexOf(':') + 1)))]);
            }
        }
        const repeated = Number(attributes(found, row).get('number-rows-repeated') ?? '1');
        if (cells.every((entry) => entry[1] === '' && entry[2].length === 0)) {
            line = line + repeated;
        }
        else {
            const last = line + repeated;
            while (line < last) {
                const record = [];
                let column = 0;
                for (const [count, text, labels] of cells) {
                    if (text === '' && labels.length === 0) {
                        column = column + count;
                    }
                    else {
                        const stop = column + count;
                        while (column < stop) {
                            while (record.length < column) {
                                record.push('');
                            }
                            record.push(text);
                            left.push(...labels.map((label) => reference(column, line) + ' ' + label));
                            column = column + 1;
                        }
                    }
                }
                while (grid.length < line) {
                    grid.push([]);
                }
                grid.push(record);
                line = line + 1;
            }
        }
    }
    return grid;
}
function reference(column, line) {
    let letters = '';
    let number = column + 1;
    while (number > 0) {
        letters = String.fromCharCode(65 + (number - 1) % 26) + letters;
        number = Math.floor((number - 1) / 26);
    }
    return letters + String(line + 1);
}
function rows(found, node) {
    const listed = [];
    for (const child of found.get(node) ?? []) {
        if (child[1] === 'element' && child[2] === 'table-row') {
            listed.push(child[0]);
        }
        else {
            if (child[1] === 'element' && ['table-header-rows', 'table-rows', 'table-row-group'].includes(child[2])) {
                listed.push(...rows(found, child[0]));
            }
        }
    }
    return listed;
}
