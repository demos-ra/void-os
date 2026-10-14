import test from 'node:test';
import * as relationalModel from '../../../src/relational-model/relational-model.js';
import * as values from '../../../src/system-generation/values/values.js';
import * as runner from '../runner/runner.js';
test('distribution-package.1', (t) => {
    t.assert.deepStrictEqual(runner.run('distribution-package.1', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('distribution-package.2', (t) => {
    t.assert.deepStrictEqual(runner.run('distribution-package.2', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('distribution-package.3', (t) => {
    t.assert.deepStrictEqual(runner.run('distribution-package.3', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('distribution-package.4', (t) => {
    t.assert.deepStrictEqual(runner.run('distribution-package.4', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
test('distribution-package.5', (t) => {
    t.assert.deepStrictEqual(runner.run('distribution-package.5', 1, import.meta.dirname + '/../../../../conformance', relationalModel, values), []);
});
