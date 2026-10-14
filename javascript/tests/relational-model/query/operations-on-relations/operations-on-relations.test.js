import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('operations-on-relations.1', (t) => {
    t.assert.deepStrictEqual(runner.run('operations-on-relations.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('operations-on-relations.2', (t) => {
    t.assert.deepStrictEqual(runner.run('operations-on-relations.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('operations-on-relations.3', (t) => {
    t.assert.deepStrictEqual(runner.run('operations-on-relations.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('operations-on-relations.4', (t) => {
    t.assert.deepStrictEqual(runner.run('operations-on-relations.4', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('operations-on-relations.5', (t) => {
    t.assert.deepStrictEqual(runner.run('operations-on-relations.5', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('operations-on-relations.6', (t) => {
    t.assert.deepStrictEqual(runner.run('operations-on-relations.6', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
