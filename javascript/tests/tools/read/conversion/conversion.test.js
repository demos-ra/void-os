import test from 'node:test';
import * as relationalModel from '../../../../src/relational-model/relational-model.js';
import * as values from '../../../../src/system-generation/values/values.js';
import * as runner from '../../../system-generation/runner/runner.js';
test('conversion.1', (t) => {
    t.assert.deepStrictEqual(runner.run('conversion.1', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('conversion.2', (t) => {
    t.assert.deepStrictEqual(runner.run('conversion.2', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('conversion.3', (t) => {
    t.assert.deepStrictEqual(runner.run('conversion.3', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
test('conversion.4', (t) => {
    t.assert.deepStrictEqual(runner.run('conversion.4', 1, import.meta.dirname + '/../../../../../conformance', relationalModel, values), []);
});
