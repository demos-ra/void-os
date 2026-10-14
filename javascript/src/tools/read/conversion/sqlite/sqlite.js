import { DatabaseSync } from 'node:sqlite';
export function load(source) {
    let sqlite1SQLiteURI = source.replaceAll('?', '%3f');
    sqlite1SQLiteURI = sqlite1SQLiteURI.replaceAll('#', '%23');
    while (sqlite1SQLiteURI.includes('//')) {
        sqlite1SQLiteURI = sqlite1SQLiteURI.replaceAll('//', '/');
    }
    sqlite1SQLiteURI = 'file:' + sqlite1SQLiteURI;
    try {
        const sqlite1OpenDatabase = new DatabaseSync(source, { readOnly: true });
        try {
            return loaded(sqlite1OpenDatabase);
        }
        finally {
            sqlite1OpenDatabase.close();
        }
    }
    catch (error) {
        if (error.code === 'ERR_SQLITE_ERROR') {
            throw new FailedError('failed');
        }
        throw error;
    }
}
export class CannotBeRepresentedError extends Error {}
export class FailedError extends Error {}
function loaded(database) {
    const sqlite1Query = database.prepare('SELECT type, name FROM sqlite_schema').all().map((row) => Object.values(row));
    return [sqlite1Query.filter((row) => row[0] === 'table' && !row[1].startsWith('sqlite_')).map((row) => sheet(database, row[1])), sqlite1Query.filter((row) => row[0] !== 'table' || row[1].startsWith('sqlite_')).map((row) => row[0] + ' ' + row[1])];
}
function quoted(name) {
    return '"' + name.replaceAll('"', '""') + '"';
}
function record(row) {
    if (row.filter((value, index) => index % 2 === 0).includes('blob')) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    return row.filter((value, index) => index % 2 === 1).map((value) => text(value ?? ''));
}
function selected(index, column) {
    return 'typeof(' + quoted(column) + ') AS "t' + String(index) + '", CAST(' + quoted(column) + ' AS TEXT) AS "v' + String(index) + '"';
}
function sheet(database, name) {
    const sqlite1Query = database.prepare("SELECT name FROM pragma_table_info('" + name.replaceAll("'", "''") + "')").all().map((row) => Object.values(row));
    const header = sqlite1Query.map((row) => row[0]);
    const query = 'SELECT ' + header.map((column, index) => selected(index, column)).join(', ') + ' FROM ' + quoted(name);
    const sqlite2Query = database.prepare(query).all().map((row) => Object.values(row));
    return { 'sheet name': text(name), header: header.map((column) => text(column)), records: sqlite2Query.map((row) => record(row)) };
}
function text(value) {
    if (Array.from('\t\n\f\r').some((character) => value.includes(character))) {
        throw new CannotBeRepresentedError('cannot be represented');
    }
    return value;
}
