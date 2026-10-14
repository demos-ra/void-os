import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('field.1', (t) => {
    t.assert.deepStrictEqual(runner.run('field.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('field.2', (t) => {
    t.assert.deepStrictEqual(runner.run('field.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('field.3', (t) => {
    t.assert.deepStrictEqual(runner.run('field.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
