import * as fs from 'node:fs';
import * as path from 'node:path';
export function values(folder, relationalModel) {
    let sheets;
    try {
        const values1ReadAFile = fs.readFileSync(path.join(folder, 'values.mtsv'));
        sheets = relationalModel.load(values1ReadAFile);
    }
    catch (error) {
        if (error instanceof relationalModel.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        if (error.syscall !== undefined) {
            throw new NotMTSVError('not MTSV');
        }
        throw error;
    }
    const sheet = sheets.filter((relation) => relation['sheet name'] === 'Values')[0];
    const header = sheet.header;
    return { 'sheet name': 'Values', header: ['Value', 'Given'], records: sheet.records.map((record) => [record[header.indexOf('Value')], record[header.indexOf('Given')]]) };
}
export class NotMTSVError extends Error {}
