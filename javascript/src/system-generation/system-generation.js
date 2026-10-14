import * as path from 'node:path';
import * as values_ from './values/values.js';
export function values(relationalModel) {
    const systemGeneration1ModuleFolder = import.meta.dirname;
    try {
        return values_.values(path.join(systemGeneration1ModuleFolder, 'values'), relationalModel);
    }
    catch (error) {
        if (error instanceof values_.NotMTSVError) {
            throw new NotMTSVError(error.message);
        }
        throw error;
    }
}
export class NotMTSVError extends Error {}
