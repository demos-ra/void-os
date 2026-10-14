import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('terminal.1', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('terminal.2', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('terminal.3', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('terminal.4', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('terminal.5', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('terminal.6', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.6', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('terminal.7', (t) => {
    t.assert.deepStrictEqual(runner.run('terminal.7', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
