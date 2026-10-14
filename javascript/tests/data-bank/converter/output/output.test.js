import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('output.1', (t) => {
    t.assert.deepStrictEqual(runner.run('output.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('output.2', (t) => {
    t.assert.deepStrictEqual(runner.run('output.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('output.3', (t) => {
    t.assert.deepStrictEqual(runner.run('output.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
