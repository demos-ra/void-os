import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('package.1', (t) => {
    t.assert.deepStrictEqual(runner.run('package.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('package.2', (t) => {
    t.assert.deepStrictEqual(runner.run('package.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('package.3', (t) => {
    t.assert.deepStrictEqual(runner.run('package.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('package.4', (t) => {
    t.assert.deepStrictEqual(runner.run('package.4', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
