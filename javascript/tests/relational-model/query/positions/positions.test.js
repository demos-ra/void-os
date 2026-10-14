import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('positions.1', (t) => {
    t.assert.deepStrictEqual(runner.run('positions.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('positions.2', (t) => {
    t.assert.deepStrictEqual(runner.run('positions.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('positions.3', (t) => {
    t.assert.deepStrictEqual(runner.run('positions.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('positions.4', (t) => {
    t.assert.deepStrictEqual(runner.run('positions.4', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
