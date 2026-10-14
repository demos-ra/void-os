export function days(values, inputName, offset, relationalModel, dataBank) {
    const counts = new Map();
    for (const entry of stored(values, inputName, relationalModel, dataBank)) {
        const key = date(entry[1], offset) + '\t' + entry[2];
        counts.set(key, (counts.get(key) ?? 0) + 1);
    }
    return { 'sheet name': 'days', header: ['input', 'day', 'event', 'values'], records: [...counts].map((pair) => [inputName, ...pair[0].split('\t'), String(pair[1])]) };
}
export function turns(values, inputName, day, offset, relationalModel, dataBank) {
    const chosen = stored(values, inputName, relationalModel, dataBank).filter((entry) => date(entry[1], offset) === day);
    const found = [];
    if (chosen.length > 0) {
        let sheets;
        try {
            sheets = dataBank.records(values, inputName, Number(chosen[0][0]), Number(chosen[chosen.length - 1][0]), [], relationalModel);
        }
        catch (error) {
            if (error instanceof dataBank.KeepingFailedError) {
                throw new KeepingFailedError(error.message);
            }
            throw error;
        }
        const runs = sheet(sheets, '_runs');
        for (const entry of chosen) {
            const instances = { 'sheet name': 'instances', header: ['_instance', '_parent', '_pointer', '_type', '_value'], records: [['0', '', '', 'object', ''], ...sheet(sheets, '_instances').filter((record) => record[0] === entry[0]).map((record) => record.slice(1))] };
            const held = runs.filter((run) => run[0] === entry[0]);
            found.push([inputName, entry[0], entry[1], entry[2], ...['agent', 'session', 'turn', 'model'].map((column) => member(instances, held, column, relationalModel)), firstLine(instances, held)]);
        }
    }
    return { 'sheet name': 'turns', header: ['input', 'value', 'time', 'event', 'agent', 'session', 'turn', 'model', 'first line'], records: found };
}
export class KeepingFailedError extends Error {}
function date(time, offset) {
    const zoom3FullDateAtOffset = new Date(Date.parse(time) + offset * 60000).toISOString().slice(0, 10);
    return zoom3FullDateAtOffset;
}
function firstLine(instances, runs) {
    for (const instance of instances.records) {
        if (instance[3] === 'string' && text(instance, runs) !== '') {
            return text(instance, runs).split('\n')[0];
        }
    }
    return '';
}
const harnessMembers = [{ 'column': 'place', 'pointer': '/cwd', 'harness': 'Codex' }, { 'column': 'place', 'pointer': '/workspace_roots/0', 'harness': 'Cursor' }, { 'column': 'agent', 'pointer': '/agent_id', 'harness': 'Claude Code' }, { 'column': 'agent', 'pointer': '/agent_id', 'harness': 'Codex' }, { 'column': 'agent', 'pointer': '/subagent_id', 'harness': 'Cursor' }, { 'column': 'session', 'pointer': '/session_id', 'harness': 'Claude Code' }, { 'column': 'session', 'pointer': '/session_id', 'harness': 'Codex' }, { 'column': 'session', 'pointer': '/conversation_id', 'harness': 'Cursor' }, { 'column': 'turn', 'pointer': '/prompt_id', 'harness': 'Claude Code' }, { 'column': 'turn', 'pointer': '/turn_id', 'harness': 'Codex' }, { 'column': 'turn', 'pointer': '/generation_id', 'harness': 'Cursor' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Claude Code' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Codex' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Cursor' }];
function member(instances, runs, column, relationalModel) {
    for (const entry of harnessMembers) {
        if (entry.column === column) {
            const named = relationalModel.named(instances, entry.pointer);
            if (named.records.length > 0) {
                return text(named.records[0], runs);
            }
        }
    }
    return '';
}
function sheet(sheets, name) {
    return sheets.filter((relation) => relation['sheet name'] === name).flatMap((relation) => relation.records);
}
function stored(values, inputName, relationalModel, dataBank) {
    let kept;
    try {
        const count = sheet(dataBank.names(values, relationalModel), '_inputs').filter((record) => record[0] === inputName).reduce((total, record) => total + Number(record[1]), 0);
        kept = dataBank.stored(values, inputName, 0, count - 1, relationalModel);
    }
    catch (error) {
        if (error instanceof dataBank.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        throw error;
    }
    const header = kept.header;
    return kept.records.map((record) => [record[header.indexOf('_input value')], record[header.indexOf('_time')], record[header.indexOf('_event')]]);
}
function text(instance, runs) {
    let content = instance[4];
    let page = 0;
    let line = 0;
    let position = 0;
    for (const run of runs) {
        if (run[1] === instance[0]) {
            while (page < Number(run[2])) {
                content = content + '\f';
                page = page + 1;
                line = 0;
                position = 0;
            }
            while (line < Number(run[3])) {
                content = content + '\n';
                line = line + 1;
                position = 0;
            }
            while (position < Number(run[4])) {
                content = content + '\t';
                position = position + 1;
            }
            content = content + run[5];
        }
    }
    return content;
}
