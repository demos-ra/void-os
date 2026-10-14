export function context(values, event, inputName, hookInput, relationalModel, dataBank) {
    const taken = answerMembers.filter((entry) => entry.event === event);
    const placed = contextMembers.filter((entry) => entry.event === event);
    if (taken.length === 0 && placed.length === 0) {
        return '';
    }
    const answer = {};
    for (const entry of taken) {
        place(answer, entry.pointer, JSON.parse(entry.value));
    }
    if (placed.length > 0) {
        let text;
        try {
            text = composed(values, placed[0].begins, inputName, hookInput, relationalModel, dataBank);
        }
        catch (error) {
            if (error instanceof dataBank.KeepingFailedError) {
                throw new KeepingFailedError(error.message);
            }
            throw error;
        }
        for (const entry of placed) {
            place(answer, entry.pointer, text);
        }
    }
    const hookOutput7JSONTextWrite = JSON.stringify(answer);
    return hookOutput7JSONTextWrite;
}
export class KeepingFailedError extends Error {}
const answerMembers = [{ 'event': 'SessionStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SessionStart"' }, { 'event': 'SessionStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SessionStart"' }, { 'event': 'SubagentStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SubagentStart"' }, { 'event': 'SubagentStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"SubagentStart"' }, { 'event': 'UserPromptSubmit', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"UserPromptSubmit"' }, { 'event': 'UserPromptSubmit', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/hookEventName', 'value': '"UserPromptSubmit"' }, { 'event': 'subagentStart', 'harness': 'Cursor', 'pointer': '/permission', 'value': '"allow"' }, { 'event': 'beforeSubmitPrompt', 'harness': 'Cursor', 'pointer': '/continue', 'value': 'true' }];
function composed(values, begins, inputName, hookInput, relationalModel, dataBank) {
    const names = begins ? dataBank.names(values, relationalModel) : [];
    const session = member(hookInput, 'session', relationalModel);
    const agent = member(hookInput, 'agent', relationalModel);
    const fresh = dataBank.new(values, inputName, session, agent, [], relationalModel);
    const owned = own(fresh, session, agent, relationalModel);
    const positions = fresh.at(-1).records.filter((record) => !owned.includes(record[1])).map((record) => record[1]);
    for (const index of positions.keys()) {
        const text = relationalModel.dumps([...names, ...positions.slice(index).flatMap((position) => [...fresh.slice(0, -1).map((relation) => kept(relation, 0, [position])), kept(fresh.at(-1), 1, [position])]).filter((relation) => relation.records.length > 0)]);
        if (Array.from(text).length <= Number(new Map(values.records).get('context limit'))) {
            return text;
        }
    }
    return relationalModel.dumps(names);
}
const contextMembers = [{ 'event': 'SessionStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': true }, { 'event': 'SessionStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': true }, { 'event': 'SubagentStart', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': true }, { 'event': 'SubagentStart', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': true }, { 'event': 'UserPromptSubmit', 'harness': 'Claude Code', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': false }, { 'event': 'UserPromptSubmit', 'harness': 'Codex', 'pointer': '/hookSpecificOutput/additionalContext', 'begins': false }, { 'event': 'sessionStart', 'harness': 'Cursor', 'pointer': '/additional_context', 'begins': true }, { 'event': 'postToolUse', 'harness': 'Cursor', 'pointer': '/additional_context', 'begins': false }];
const harnessMembers = [{ 'column': 'place', 'pointer': '/cwd', 'harness': 'Codex' }, { 'column': 'place', 'pointer': '/workspace_roots/0', 'harness': 'Cursor' }, { 'column': 'agent', 'pointer': '/agent_id', 'harness': 'Claude Code' }, { 'column': 'agent', 'pointer': '/agent_id', 'harness': 'Codex' }, { 'column': 'agent', 'pointer': '/subagent_id', 'harness': 'Cursor' }, { 'column': 'session', 'pointer': '/session_id', 'harness': 'Claude Code' }, { 'column': 'session', 'pointer': '/session_id', 'harness': 'Codex' }, { 'column': 'session', 'pointer': '/conversation_id', 'harness': 'Cursor' }, { 'column': 'turn', 'pointer': '/prompt_id', 'harness': 'Claude Code' }, { 'column': 'turn', 'pointer': '/turn_id', 'harness': 'Codex' }, { 'column': 'turn', 'pointer': '/generation_id', 'harness': 'Cursor' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Claude Code' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Codex' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Cursor' }];
function kept(relation, column, chosen) {
    return { 'sheet name': relation['sheet name'], header: relation.header, records: relation.records.filter((record) => chosen.includes(record[column])) };
}
function member(instances, column, relationalModel) {
    for (const entry of harnessMembers) {
        if (entry.column === column) {
            const named = relationalModel.named(instances, entry.pointer);
            if (named.records.length > 0) {
                return named.records[0][4];
            }
        }
    }
    return '';
}
function own(fresh, session, agent, relationalModel) {
    const owned = [];
    for (const record of fresh.at(-1).records) {
        const instances = { 'sheet name': 'instances', header: ['_instance', '_parent', '_pointer', '_type', '_value'], records: fresh.filter((relation) => relation['sheet name'] === '_instances').flatMap((relation) => relation.records).filter((entry) => entry[0] === record[1]).map((entry) => entry.slice(1)) };
        if (member(instances, 'session', relationalModel) === session && member(instances, 'agent', relationalModel) === agent) {
            owned.push(record[1]);
        }
    }
    return owned;
}
function place(answer, pointer, value) {
    const tokens = pointer.split('/').slice(1).map((token) => token.replaceAll('~1', '/').replaceAll('~0', '~'));
    let held = answer;
    for (const token of tokens.slice(0, -1)) {
        held[token] = held[token] ?? {};
        held = held[token];
    }
    held[tokens.at(-1)] = value;
}
