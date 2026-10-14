import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('key.1', (t) => {
    t.assert.deepStrictEqual(runner.run('key.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('key.2', (t) => {
    t.assert.deepStrictEqual(runner.run('key.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('key.3', (t) => {
    t.assert.deepStrictEqual(runner.run('key.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('key.4', (t) => {
    t.assert.deepStrictEqual(runner.run('key.4', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
