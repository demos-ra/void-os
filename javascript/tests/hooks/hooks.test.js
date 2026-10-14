import test from 'node:test';
import * as relationalModel from '../../src/relational-model/relational-model.js';
import * as values from '../../src/system-generation/values/values.js';
import * as runner from '../system-generation/runner/runner.js';
test('hooks.1', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.1', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('hooks.2', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.2', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('hooks.3', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.3', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('hooks.5', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.5', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('hooks.6', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.6', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('hooks.7', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.7', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('hooks.8', (t) => {
    t.assert.deepStrictEqual(runner.run('hooks.8', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
