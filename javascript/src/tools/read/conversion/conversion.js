import * as fs from 'node:fs';
import * as csv from './csv/csv.js';
import * as json from './json/json.js';
import * as ods from './ods/ods.js';
import * as package_ from './package/package.js';
import * as sqlite from './sqlite/sqlite.js';
import * as xlsx from './xlsx/xlsx.js';
export function sheets(source, relationalModel) {
    const name = source.slice(source.lastIndexOf('/') + 1);
    const extension = name.includes('.') ? name.slice(name.lastIndexOf('.') + 1) : '';
    if (!['mtsv', 'csv', 'json', 'xlsx', 'ods', 'sqlite'].includes(extension)) {
        throw new NoFormatError('no format');
    }
    try {
        if (extension === 'sqlite') {
            return sqlite.load(source);
        }
        if (extension === 'xlsx') {
            return xlsx.load(package_.nodes(source));
        }
        if (extension === 'ods') {
            return ods.load(package_.nodes(source));
        }
        let octets;
        try {
            const conversion1ReadAFile = fs.readFileSync(source);
            octets = conversion1ReadAFile;
        }
        catch (error) {
            throw new FailedError('cannot be read');
        }
        if (extension === 'mtsv') {
            return [relationalModel.load(octets), []];
        }
        if (extension === 'csv') {
            return csv.load(octets);
        }
        return json.load(octets, relationalModel);
    }
    catch (error) {
        if (error instanceof sqlite.CannotBeRepresentedError) {
            throw new FailedError('cannot be represented');
        }
        if (error instanceof sqlite.FailedError) {
            throw new FailedError('failed');
        }
        if (error instanceof package_.FailedError) {
            throw new FailedError('failed');
        }
        if (error instanceof package_.CompressionMethodNotAllowedError) {
            throw new FailedError('compression method not allowed');
        }
        if (error instanceof xlsx.CannotBeRepresentedError) {
            throw new FailedError('cannot be represented');
        }
        if (error instanceof xlsx.FailedError) {
            throw new FailedError('failed');
        }
        if (error instanceof ods.CannotBeRepresentedError) {
            throw new FailedError('cannot be represented');
        }
        if (error instanceof ods.FailedError) {
            throw new FailedError('failed');
        }
        if (error instanceof relationalModel.NotMTSVError) {
            throw new FailedError('not MTSV');
        }
        if (error instanceof csv.CannotBeRepresentedError) {
            throw new FailedError('cannot be represented');
        }
        if (error instanceof json.CannotBeRepresentedError) {
            throw new FailedError('cannot be represented');
        }
        if (error instanceof json.NotAJSONTextError) {
            throw new FailedError('not a JSON text');
        }
        if (error instanceof json.NamesNotUniqueError) {
            throw new FailedError('names not unique');
        }
        throw error;
    }
}
export class FailedError extends Error {}
export class NoFormatError extends Error {}
