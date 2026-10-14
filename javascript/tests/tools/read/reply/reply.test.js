import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('reply.1', (t) => {
    t.assert.deepStrictEqual(runner.run('reply.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('reply.2', (t) => {
    t.assert.deepStrictEqual(runner.run('reply.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('reply.3', (t) => {
    t.assert.deepStrictEqual(runner.run('reply.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('reply.5', (t) => {
    t.assert.deepStrictEqual(runner.run('reply.5', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
