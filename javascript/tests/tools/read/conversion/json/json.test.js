import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('json.1', (t) => {
    t.assert.deepStrictEqual(runner.run('json.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('json.2', (t) => {
    t.assert.deepStrictEqual(runner.run('json.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
