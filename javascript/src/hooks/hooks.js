import * as fs from 'node:fs';
import * as hookInput from './hook-input/hook-input.js';
import * as hookOutput from './hook-output/hook-output.js';
export function hook(values, event, workingDirectory, relationalModel, dataBank) {
    const hooks7ReadStandardInput = fs.readFileSync(0);
    let given;
    try {
        given = relationalModel.instances(hooks7ReadStandardInput);
    }
    catch (error) {
        if (error instanceof relationalModel.NotAJSONTextError) {
            throw new NonConformingError('non-conforming');
        }
        if (error instanceof relationalModel.NamesNotUniqueError) {
            throw new NonConformingError('non-conforming');
        }
        throw error;
    }
    let place = '';
    for (const entry of harnessVariables) {
        if (place === '' && entry.column === 'place') {
            const hooks2EnvironmentVariable = process.env[entry.variable];
            if (hooks2EnvironmentVariable !== undefined) {
                place = hooks2EnvironmentVariable;
            }
        }
    }
    for (const entry of harnessMembers) {
        if (place === '' && entry.column === 'place') {
            const named = relationalModel.named(given[0], entry.pointer);
            if (named.records.length > 0) {
                place = named.records[0][4];
            }
        }
    }
    if (place === '') {
        place = workingDirectory;
    }
    const hooks2ResolvePathname = fs.realpathSync(place);
    let answer;
    try {
        answer = hookOutput.context(values, event, hooks2ResolvePathname, given[0], relationalModel, dataBank);
        hookInput.insert(values, hooks2ResolvePathname, event, hooks7ReadStandardInput, relationalModel, dataBank);
    }
    catch (error) {
        if (error instanceof hookOutput.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof hookInput.KeepingFailedError) {
            throw new KeepingFailedError(error.message);
        }
        if (error instanceof hookInput.NonConformingError) {
            throw new NonConformingError(error.message);
        }
        throw error;
    }
    if (answer !== '') {
        const hooks8UTF8Encode = new TextEncoder().encode(answer);
        process.stdout.write(hooks8UTF8Encode);
    }
}
export class KeepingFailedError extends Error {}
export class NonConformingError extends Error {}
const harnessMembers = [{ 'column': 'place', 'pointer': '/cwd', 'harness': 'Codex' }, { 'column': 'place', 'pointer': '/workspace_roots/0', 'harness': 'Cursor' }, { 'column': 'agent', 'pointer': '/agent_id', 'harness': 'Claude Code' }, { 'column': 'agent', 'pointer': '/agent_id', 'harness': 'Codex' }, { 'column': 'agent', 'pointer': '/subagent_id', 'harness': 'Cursor' }, { 'column': 'session', 'pointer': '/session_id', 'harness': 'Claude Code' }, { 'column': 'session', 'pointer': '/session_id', 'harness': 'Codex' }, { 'column': 'session', 'pointer': '/conversation_id', 'harness': 'Cursor' }, { 'column': 'turn', 'pointer': '/prompt_id', 'harness': 'Claude Code' }, { 'column': 'turn', 'pointer': '/turn_id', 'harness': 'Codex' }, { 'column': 'turn', 'pointer': '/generation_id', 'harness': 'Cursor' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Claude Code' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Codex' }, { 'column': 'model', 'pointer': '/model', 'harness': 'Cursor' }];
const harnessVariables = [{ 'column': 'place', 'variable': 'CLAUDE_PROJECT_DIR', 'harness': 'Claude Code' }];
