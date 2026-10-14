import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('json-text.1', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.2', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.3', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.4', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.4', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.5', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.5', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.6', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.6', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.7', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.7', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('json-text.8', (t) => {
    t.assert.deepStrictEqual(runner.run('json-text.8', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
