import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('ods.1', (t) => {
    t.assert.deepStrictEqual(runner.run('ods.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('ods.2', (t) => {
    t.assert.deepStrictEqual(runner.run('ods.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('ods.3', (t) => {
    t.assert.deepStrictEqual(runner.run('ods.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
