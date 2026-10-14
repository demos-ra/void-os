import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('read-input.1', (t) => {
    t.assert.deepStrictEqual(runner.run('read-input.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('read-input.2', (t) => {
    t.assert.deepStrictEqual(runner.run('read-input.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('read-input.3', (t) => {
    t.assert.deepStrictEqual(runner.run('read-input.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('read-input.4', (t) => {
    t.assert.deepStrictEqual(runner.run('read-input.4', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('read-input.5', (t) => {
    t.assert.deepStrictEqual(runner.run('read-input.5', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
