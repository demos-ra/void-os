import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('converter.1', (t) => {
    t.assert.deepStrictEqual(runner.run('converter.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('converter.5', (t) => {
    t.assert.deepStrictEqual(runner.run('converter.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
