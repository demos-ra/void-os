export function join(sheets, origins, join, positions, filterExpression) {
    if (!join) {
        return sheets;
    }
    const of = Object.fromEntries(origins.records.map((record) => [record[0], record[1]]));
    const grouped = new Map();
    for (const [index, sheet] of sheets.entries()) {
        if (!grouped.has(of[String(index + 1)])) {
            grouped.set(of[String(index + 1)], []);
        }
        grouped.get(of[String(index + 1)]).push(sheet);
    }
    const given = [];
    try {
        for (const each of grouped.values()) {
            const named = positions.named(join, each.length).records.map((found) => each[Number(found[0]) - 1]);
            if (named.length > 0) {
                given.push(named.reduce(joined));
            }
            given.push(...each.filter((sheet) => !named.includes(sheet)));
        }
    }
    catch (error) {
        if (error instanceof positions.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
    return given;
}
export function project(sheets, fields, positions, filterExpression) {
    try {
        return sheets.map((sheet) => !fields || sheet.header === null ? sheet : projected(sheet, positions.named(fields, sheet.header.length).records.map((found) => Number(found[0]) - 1)));
    }
    catch (error) {
        if (error instanceof positions.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export function restrict(sheets, records, filter, positions, filterExpression) {
    try {
        const kept = filter ? filterExpression.kept(sheets, filter) : sheets;
        return kept.map((sheet) => ({ 'sheet name': sheet['sheet name'], header: sheet.header, records: records ? positions.named(records, sheet.records.length).records.map((found) => sheet.records[Number(found[0]) - 1]) : sheet.records }));
    }
    catch (error) {
        if (error instanceof filterExpression.RefusedError) {
            throw new RefusedError(error.message);
        }
        if (error instanceof positions.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export class RefusedError extends Error {}
function joined(left, right) {
    const shared = left.header === null || right.header === null ? [] : left.header.filter((name) => right.header.includes(name));
    if (shared.length === 0) {
        throw new RefusedError('the sheets ' + left['sheet name'] + ' and ' + right['sheet name'] + ' share no column');
    }
    const others = right.header.flatMap((name, index) => shared.includes(name) ? [] : [index]);
    return { 'sheet name': left['sheet name'] + '*' + right['sheet name'], header: [...left.header, ...others.map((index) => right.header[index])], records: left.records.flatMap((first) => right.records.filter((second) => shared.every((name) => first[left.header.indexOf(name)] === second[right.header.indexOf(name)])).map((second) => [...first, ...others.map((index) => second[index])])) };
}
function projected(sheet, kept) {
    if (kept.length === 0) {
        return { 'sheet name': sheet['sheet name'], header: null, records: [] };
    }
    return { 'sheet name': sheet['sheet name'], header: kept.map((index) => sheet.header[index]), records: sheet.records.map((record) => kept.map((index) => record[index])) };
}
