#!/usr/bin/env node
import * as tty from 'node:tty';
import * as dataBank from './data-bank/data-bank.js';
import * as hooks from './hooks/hooks.js';
import * as relationalModel from './relational-model/relational-model.js';
import * as systemGeneration from './system-generation/system-generation.js';
import * as tools from './tools/tools.js';
import * as view from './view/view.js';
export function voidOs() {
    const voidOs5Arguments = process.argv.slice(2);
    let values;
    try {
        values = systemGeneration.values(relationalModel);
    }
    catch (error) {
        if (error instanceof systemGeneration.NotMTSVError) {
            const voidOs11UTF8Encode = new TextEncoder().encode(error.message + '\n');
            process.stderr.write(voidOs11UTF8Encode);
            process.exitCode = 1;
            return 1;
        }
        throw error;
    }
    const given = new Map(values.records);
    if (voidOs5Arguments.length === 0) {
        tools.serve(values, relationalModel, dataBank);
        return 0;
    }
    if (voidOs5Arguments[0] === given.get('view operand')) {
        const voidOs10IsATerminal = tty.isatty(1);
        const voidOs10LocalOffset = -new Date().getTimezoneOffset();
        try {
            view.view(values, voidOs5Arguments.slice(1), voidOs10IsATerminal, voidOs10LocalOffset, relationalModel, dataBank);
        }
        catch (error) {
            if (error instanceof view.RefusedError) {
                const voidOs11UTF8Encode = new TextEncoder().encode(error.message + '\n');
                process.stderr.write(voidOs11UTF8Encode);
                process.exitCode = 1;
                return 1;
            }
            if (error instanceof view.KeepingFailedError) {
                const voidOs11UTF8Encode = new TextEncoder().encode(error.message + '\n');
                process.stderr.write(voidOs11UTF8Encode);
                process.exitCode = 1;
                return 1;
            }
            throw error;
        }
        return 0;
    }
    if (voidOs5Arguments.length === 1 && ['SessionStart', 'SubagentStart', 'UserPromptSubmit', 'PostToolUse', 'SubagentStop', 'Stop', 'sessionStart', 'subagentStart', 'beforeSubmitPrompt', 'postToolUse', 'subagentStop', 'stop'].includes(voidOs5Arguments[0])) {
        const voidOs7WorkingDirectory = process.cwd();
        try {
            hooks.hook(values, voidOs5Arguments[0], voidOs7WorkingDirectory, relationalModel, dataBank);
        }
        catch (error) {
            if (error instanceof hooks.KeepingFailedError) {
                const voidOs11UTF8Encode = new TextEncoder().encode(error.message + '\n');
                process.stderr.write(voidOs11UTF8Encode);
                process.exitCode = 1;
                return 1;
            }
            if (error instanceof hooks.NonConformingError) {
                const voidOs11UTF8Encode = new TextEncoder().encode(error.message + '\n');
                process.stderr.write(voidOs11UTF8Encode);
                process.exitCode = 1;
                return 1;
            }
            throw error;
        }
        process.exitCode = 0;
        return 0;
    }
    const voidOs8UTF8Encode = new TextEncoder().encode(given.get('usage message') + '\n');
    process.stderr.write(voidOs8UTF8Encode);
    process.exitCode = 1;
    return 1;
}
process.exitCode = voidOs();
