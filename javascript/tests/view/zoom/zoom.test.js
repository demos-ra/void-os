import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('zoom.1', (t) => {
    t.assert.deepStrictEqual(runner.run('zoom.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('zoom.2', (t) => {
    t.assert.deepStrictEqual(runner.run('zoom.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('zoom.3', (t) => {
    t.assert.deepStrictEqual(runner.run('zoom.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('zoom.4', (t) => {
    t.assert.deepStrictEqual(runner.run('zoom.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('zoom.5', (t) => {
    t.assert.deepStrictEqual(runner.run('zoom.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
