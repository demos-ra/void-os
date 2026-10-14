import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('schema.1', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.11', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.11', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.13', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.13', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.16', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.16', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.17', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.17', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.2', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.3', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.4', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.4', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.5', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.5', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.6', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.6', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.7', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.7', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.8', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.8', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('schema.9', (t) => {
    t.assert.deepStrictEqual(runner.run('schema.9', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
