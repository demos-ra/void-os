import test from 'node:test';
import * as relationalModel from '../../../../../src/relational-model/relational-model.js';
import * as values from '../../../../../src/system-generation/values/values.js';
import * as runner from '../../../../system-generation/runner/runner.js';
test('record.1', (t) => {
    t.assert.deepStrictEqual(runner.run('record.1', 1, import.meta.dirname + '/../../../../../../conformance', relationalModel, values), []);
});
