import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('query.1', (t) => {
    t.assert.deepStrictEqual(runner.run('query.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('query.2', (t) => {
    t.assert.deepStrictEqual(runner.run('query.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('query.3', (t) => {
    t.assert.deepStrictEqual(runner.run('query.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('query.4', (t) => {
    t.assert.deepStrictEqual(runner.run('query.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('query.5', (t) => {
    t.assert.deepStrictEqual(runner.run('query.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
