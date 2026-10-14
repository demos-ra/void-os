import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('parser.1', (t) => {
    t.assert.deepStrictEqual(runner.run('parser.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('parser.2', (t) => {
    t.assert.deepStrictEqual(runner.run('parser.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('parser.3', (t) => {
    t.assert.deepStrictEqual(runner.run('parser.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('parser.4', (t) => {
    t.assert.deepStrictEqual(runner.run('parser.4', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
