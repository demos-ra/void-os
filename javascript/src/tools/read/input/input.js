import * as fs from 'node:fs';
export function members(pathname) {
    if (!pathname.startsWith('/')) {
        throw new RefusedError('not absolute');
    }
    let readInput3IsADirectory;
    try {
        readInput3IsADirectory = fs.statSync(pathname).isDirectory();
    }
    catch {
        readInput3IsADirectory = false;
    }
    let readInput3IsARegularFile;
    try {
        readInput3IsARegularFile = fs.statSync(pathname).isFile();
    }
    catch {
        readInput3IsARegularFile = false;
    }
    if (readInput3IsARegularFile) {
        try {
            const readInput3ReadAFile = fs.readFileSync(pathname);
        }
        catch (error) {
            throw new RefusedError('cannot be read');
        }
        const readInput4ResolvePathname = fs.realpathSync(pathname);
        return [{ 'sheet name': 'file', header: ['file', 'source'], records: [['1', readInput4ResolvePathname]] }, { 'sheet name': 'not read', header: ['file', 'status', 'reason'], records: [] }];
    }
    if (!readInput3IsADirectory) {
        throw new RefusedError('names neither a directory nor a regular file');
    }
    let listed;
    try {
        const readInput2ListDirectory = fs.readdirSync(pathname, { encoding: 'buffer' });
        listed = readInput2ListDirectory;
    }
    catch (error) {
        throw new RefusedError('cannot be listed');
    }
    const place = pathname.endsWith('/') ? pathname : pathname + '/';
    const found = [];
    const left = [];
    for (const name of listed.sort(Buffer.compare)) {
        const input1UTF8Decode = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(name);
        if (!input1UTF8Decode.startsWith('.')) {
            let readInput2IsARegularFile;
            try {
                readInput2IsARegularFile = fs.statSync(place + input1UTF8Decode).isFile();
            }
            catch {
                readInput2IsARegularFile = false;
            }
            let readInput2IsADirectory;
            try {
                readInput2IsADirectory = fs.statSync(place + input1UTF8Decode).isDirectory();
            }
            catch {
                readInput2IsADirectory = false;
            }
            if (readInput2IsARegularFile) {
                const readInput4ResolvePathname = fs.realpathSync(place + input1UTF8Decode);
                if (!found.map((record) => record[1]).includes(readInput4ResolvePathname)) {
                    found.push([String(found.length + 1), readInput4ResolvePathname]);
                }
            }
            else {
                if (!readInput2IsADirectory) {
                    found.push([String(found.length + 1), place + input1UTF8Decode]);
                    left.push([String(found.length), 'skipped', '']);
                }
            }
        }
    }
    return [{ 'sheet name': 'file', header: ['file', 'source'], records: found }, { 'sheet name': 'not read', header: ['file', 'status', 'reason'], records: left }];
}
export class RefusedError extends Error {}
