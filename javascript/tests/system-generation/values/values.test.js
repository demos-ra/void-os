import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../runner/runner.js';
test('values.1', (t) => {
    t.assert.deepStrictEqual(runner.run('values.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('values.2', (t) => {
    t.assert.deepStrictEqual(runner.run('values.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('values.3', (t) => {
    t.assert.deepStrictEqual(runner.run('values.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
