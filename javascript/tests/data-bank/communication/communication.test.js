import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('communication.1', (t) => {
    t.assert.deepStrictEqual(runner.run('communication.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('communication.2', (t) => {
    t.assert.deepStrictEqual(runner.run('communication.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('communication.3', (t) => {
    t.assert.deepStrictEqual(runner.run('communication.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('communication.4', (t) => {
    t.assert.deepStrictEqual(runner.run('communication.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('communication.5', (t) => {
    t.assert.deepStrictEqual(runner.run('communication.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
