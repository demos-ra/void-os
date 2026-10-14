import * as details from './details/details.js';
import * as filter from './filter/filter.js';
import * as overview from './overview/overview.js';
import * as terminal from './terminal/terminal.js';
import * as zoom from './zoom/zoom.js';
export function view(values, operands, isATerminal, offset, relationalModel, dataBank) {
    let chosen = operands;
    let filters = [];
    if (chosen.length >= 2 && chosen[0] === '--filter') {
        filters = [chosen[1]];
        chosen = chosen.slice(2);
    }
    if (chosen.length > 3) {
        throw new RefusedError('too many operands');
    }
    let level;
    try {
        const inputs = dataBank.names(values, relationalModel).filter((relation) => relation['sheet name'] === '_inputs')[0];
        if (chosen.length === 0) {
            const every = inputs.records.map((record) => zoom.days(values, record[0], offset, relationalModel, dataBank));
            level = [overview.overview(inputs, { 'sheet name': 'days', header: ['input', 'day', 'event', 'values'], records: every.flatMap((relation) => relation.records) })];
        }
        if (chosen.length >= 1) {
            if (!inputs.records.some((record) => record[0] === chosen[0])) {
                throw new RefusedError('no input ' + chosen[0]);
            }
            level = [zoom.days(values, chosen[0], offset, relationalModel, dataBank)];
        }
        if (chosen.length >= 2) {
            if (!level[0].records.some((record) => record[1] === chosen[1])) {
                throw new RefusedError('no day ' + chosen[1]);
            }
            level = [zoom.turns(values, chosen[0], chosen[1], offset, relationalModel, dataBank)];
        }
        if (chosen.length === 3) {
            if (!level[0].records.some((record) => record[1] === chosen[2])) {
                throw new RefusedError('no position ' + chosen[2]);
            }
            level = details.details(values, chosen[0], Number(chosen[2]), relationalModel, dataBank);
        }
        for (const query of filters) {
            level = filter.kept(level, query, relationalModel);
        }
    }
    catch (error) {
        if (error instanceof dataBank.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof zoom.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof details.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof filter.RefusedError) {
            throw new RefusedError(error.message);
        }
        throw error;
    }
    const text = terminal.layOut(values, level, isATerminal, relationalModel);
    if (isATerminal) {
        terminal.page(values, text, relationalModel);
    }
    if (!isATerminal) {
        terminal.write(text, relationalModel);
    }
}
export class KeepingFailedError extends Error {}
export class RefusedError extends Error {}
