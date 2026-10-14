import test from 'node:test';
import * as relationalModel from '../../src/relational-model/relational-model.js';
import * as values from '../../src/system-generation/values/values.js';
import * as runner from '../system-generation/runner/runner.js';
test('view.1', (t) => {
    t.assert.deepStrictEqual(runner.run('view.1', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('view.2', (t) => {
    t.assert.deepStrictEqual(runner.run('view.2', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('view.3', (t) => {
    t.assert.deepStrictEqual(runner.run('view.3', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('view.5', (t) => {
    t.assert.deepStrictEqual(runner.run('view.5', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('view.6', (t) => {
    t.assert.deepStrictEqual(runner.run('view.6', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('view.8', (t) => {
    t.assert.deepStrictEqual(runner.run('view.8', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
test('view.9', (t) => {
    t.assert.deepStrictEqual(runner.run('view.9', 1, import.meta.dirname + '/../../../conformance', relationalModel, values), []);
});
