import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('hook-output.1', (t) => {
    t.assert.deepStrictEqual(runner.run('hook-output.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('hook-output.4', (t) => {
    t.assert.deepStrictEqual(runner.run('hook-output.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('hook-output.5', (t) => {
    t.assert.deepStrictEqual(runner.run('hook-output.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('hook-output.6', (t) => {
    t.assert.deepStrictEqual(runner.run('hook-output.6', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('hook-output.7', (t) => {
    t.assert.deepStrictEqual(runner.run('hook-output.7', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('hook-output.8', (t) => {
    t.assert.deepStrictEqual(runner.run('hook-output.8', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
