import * as filterExpression from './filter-expression/filter-expression.js';
import * as operationsOnRelations from './operations-on-relations/operations-on-relations.js';
import * as positions from './positions/positions.js';
import * as setOperations from './set-operations/set-operations.js';
export function chosen(sheets, origins, file, lead, sheet, records, fields, filter, join) {
    try {
        const of = Object.fromEntries(origins.records.map((record) => [record[0], record[1]]));
        const members = [];
        for (const each of new Set(sheets.map((found, index) => of[String(index + 1)]))) {
            let given = sheets.filter((found, index) => of[String(index + 1)] === each);
            given = operationsOnRelations.join(given, originsOf(given.map(() => each)), join, positions, filterExpression);
            const numbers = sheet ? positions.named(sheet, given.length).records.map((found) => Number(found[0])) : given.map((found, index) => index + 1);
            members.push(...numbers.map((number) => [each, number, given[number - 1], operationsOnRelations.restrict([given[number - 1]], '', filter, positions, filterExpression)[0]]));
        }
        const restricted = [];
        const report = [];
        for (const name of new Set(members.map((member) => member[2]['sheet name']))) {
            const group = members.filter((member) => member[2]['sheet name'] === name);
            const outputs = new Set(group.map((member) => member[0])).size === 1 ? group.map((member) => [member[3], [member]]) : setOperations.union(group.map((member) => member[3]), originsOf(group.map((member) => member[0])), file, lead).map((united) => [united, group.filter((member) => JSON.stringify(member[3].header === null ? null : [lead, ...member[3].header]) === JSON.stringify(united.header))]);
            for (const [given, parts] of outputs) {
                const numbers = records ? positions.named(records, given.records.length).records.map((found) => Number(found[0])) : given.records.map((found, index) => index + 1);
                let offset = 0;
                for (const part of parts) {
                    report.push([part[0], String(part[1]), name, String(part[2].records.length), String(part[3].records.length), positions.written({ 'sheet name': 'positions', header: ['position'], records: numbers.filter((number) => offset < number && number <= offset + part[3].records.length).map((number) => [String(number)]) })]);
                    offset += part[3].records.length;
                }
                restricted.push({ 'sheet name': name, header: given.header, records: numbers.map((number) => given.records[number - 1]) });
            }
        }
        return [operationsOnRelations.project(restricted, fields, positions, filterExpression), { 'sheet name': 'sheets', header: ['file', 'sheet', 'sheet name', 'records', 'matches', 'positions'], records: report }];
    }
    catch (error) {
        if (error instanceof operationsOnRelations.RefusedError) {
            throw new RefusedError(error.message);
        }
        if (error instanceof positions.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export function kept(sheets, filter) {
    try {
        return filterExpression.kept(sheets, filter);
    }
    catch (error) {
        if (error instanceof filterExpression.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
}
export class RefusedError extends Error {}
function originsOf(files) {
    return { 'sheet name': 'origins', header: ['sheet', 'file'], records: files.map((each, index) => [String(index + 1), each]) };
}
