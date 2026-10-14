import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('converter-input.1', (t) => {
    t.assert.deepStrictEqual(runner.run('converter-input.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('converter-input.2', (t) => {
    t.assert.deepStrictEqual(runner.run('converter-input.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
