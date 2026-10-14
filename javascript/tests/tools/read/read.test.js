import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('read.10', (t) => {
    t.assert.deepStrictEqual(runner.run('read.10', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('read.2', (t) => {
    t.assert.deepStrictEqual(runner.run('read.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('read.4', (t) => {
    t.assert.deepStrictEqual(runner.run('read.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('read.6', (t) => {
    t.assert.deepStrictEqual(runner.run('read.6', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('read.7', (t) => {
    t.assert.deepStrictEqual(runner.run('read.7', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('read.8', (t) => {
    t.assert.deepStrictEqual(runner.run('read.8', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('read.9', (t) => {
    t.assert.deepStrictEqual(runner.run('read.9', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
