import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../../system-generation/runner/runner.js';
test('server.1', (t) => {
    t.assert.deepStrictEqual(runner.run('server.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('server.2', (t) => {
    t.assert.deepStrictEqual(runner.run('server.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('server.3', (t) => {
    t.assert.deepStrictEqual(runner.run('server.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('server.4', (t) => {
    t.assert.deepStrictEqual(runner.run('server.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('server.5', (t) => {
    t.assert.deepStrictEqual(runner.run('server.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('server.6', (t) => {
    t.assert.deepStrictEqual(runner.run('server.6', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
