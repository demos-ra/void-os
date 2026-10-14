import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('value.1', (t) => {
    t.assert.deepStrictEqual(runner.run('value.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('value.2', (t) => {
    t.assert.deepStrictEqual(runner.run('value.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('value.3', (t) => {
    t.assert.deepStrictEqual(runner.run('value.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('value.4', (t) => {
    t.assert.deepStrictEqual(runner.run('value.4', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('value.5', (t) => {
    t.assert.deepStrictEqual(runner.run('value.5', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
