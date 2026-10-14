import test from 'node:test';
import * as relationalModel from '../src/relational-model/relational-model.js';
import * as values from '../src/system-generation/values/values.js';
import * as runner from './system-generation/runner/runner.js';
test('void-os.1', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.1', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.10', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.10', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.11', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.11', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.2', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.2', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.3', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.3', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.4', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.4', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.5', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.5', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.6', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.6', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.7', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.7', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.8', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.8', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
test('void-os.9', (t) => {
    t.assert.deepStrictEqual(runner.run('void-os.9', 1, import.meta.dirname + '/../../conformance', relationalModel, values), []);
});
