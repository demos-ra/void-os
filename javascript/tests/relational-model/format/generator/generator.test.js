import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('generator.1', (t) => {
    t.assert.deepStrictEqual(runner.run('generator.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('generator.2', (t) => {
    t.assert.deepStrictEqual(runner.run('generator.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('generator.3', (t) => {
    t.assert.deepStrictEqual(runner.run('generator.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
