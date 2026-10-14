import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('sheet.1', (t) => {
    t.assert.deepStrictEqual(runner.run('sheet.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('sheet.2', (t) => {
    t.assert.deepStrictEqual(runner.run('sheet.2', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('sheet.3', (t) => {
    t.assert.deepStrictEqual(runner.run('sheet.3', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('sheet.4', (t) => {
    t.assert.deepStrictEqual(runner.run('sheet.4', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
test('sheet.5', (t) => {
    t.assert.deepStrictEqual(runner.run('sheet.5', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
