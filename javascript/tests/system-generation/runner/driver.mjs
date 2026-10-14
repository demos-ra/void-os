// The test driver for JavaScript: makes the one call a test runner asks for, and
// writes back what it gives.
//
// Run as: node driver.mjs REQUEST RESPONSE, the last two arguments the pathnames
// of the request and of the response, each a JSON text, as the test runner's
// run.py states them. It writes nothing on standard output or standard error,
// which are the code's under test. Its steps, in order, are those of every
// language's driver: read the request, build each argument, load the module,
// find the function, call it, give each result, write the response. An .mjs
// file is an ECMAScript module whatever the project's package.json says (NODE-ESM).
import fs from 'node:fs';
import url from 'node:url';

// A call the driver cannot make or give back, as the response's failure.
class Failure extends Error {}

// The call, its response written whatever it ends with: results, an error and
// its reason, or the driver's failure.
async function main(argv) {
  let response;
  try {
    response = await call(readRequest(argv[argv.length - 2]));
  } catch (error) {
    if (!(error instanceof Failure)) throw error;
    response = { failure: error.message };
  }
  writeResponse(argv[argv.length - 1], response);
}

// The request: file, function, arguments and results.
function readRequest(path) {
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

// The function called with its arguments, awaited where it gives a promise: its
// results, each as its form gives it; or the error it ends with, by its class's
// name and its reason.
async function call(request) {
  const function_ = functionOf(await load(request.file), request.function, request.file);
  const arguments_ = [];
  for (const value of request.arguments) arguments_.push(await argument(value));
  let value;
  try {
    value = await function_(...arguments_);
  } catch (error) { // every error the code ends with, the runner's to compare
    return { error: error?.constructor?.name ?? typeof error, reason: error?.message ?? String(error) };
  }
  return { results: await results(value, request.results) };
}

// One argument: octets for {"$bytes"}, a module for {"$module"}, what a call
// gives for {"$call"}, an item of it by "index"; a JSON value as it is.
async function argument(value) {
  if (Array.isArray(value)) {
    const items = [];
    for (const item of value) items.push(await argument(item));
    return items;
  }
  if (value === null || typeof value !== 'object') return value;
  const names = Object.keys(value);
  if (names.length === 1 && names[0] === '$bytes') return new Uint8Array(Buffer.from(value.$bytes, 'base64'));
  if (names.length === 1 && names[0] === '$module') return load(value.$module);
  if ('$call' in value) {
    const given = await givenBy(value.$call);
    return 'index' in value ? given[value.index] : given;
  }
  const members = {};
  for (const name of names) members[name] = await argument(value[name]);
  return members;
}

// What a call the request names gives: a call made for the case's call, not the
// case's own.
async function givenBy(request) {
  const function_ = functionOf(await load(request.file), request.function, request.file);
  const arguments_ = [];
  for (const value of request.arguments) arguments_.push(await argument(value));
  try {
    return await function_(...arguments_);
  } catch (error) {
    throw new Failure(`${request.function} of ${request.file}: ${error?.constructor?.name}: ${error?.message}`);
  }
}

// NODE-ESM: the module a file holds, imported by its file URL, so it is the one
// module the code under test imports.
async function load(file) {
  try {
    return await import(url.pathToFileURL(file).href);
  } catch (error) {
    throw new Failure(`${file}: ${error?.constructor?.name}: ${error?.message}`);
  }
}

// The function a module exports by a name.
function functionOf(module, name, file) {
  if (typeof module[name] !== 'function') throw new Failure(`${file}: no function ${name}`);
  return module[name];
}

// Each result, as its form gives it: an array of them for more than one; a
// relation's or relations' dumped as MTSV octets by the dump the request names,
// handed it.
async function results(value, forms) {
  const values = forms.length > 1 && Array.isArray(value) ? value : [value];
  if (values.length !== forms.length && forms.length > 0) {
    throw new Failure(`${values.length} results, expected ${forms.length}`);
  }
  const given = [];
  for (const [index, form] of forms.entries()) {
    given.push(jsonValue(form.dump ? await dumped(values[index], form) : values[index]));
  }
  return given;
}

// A relation's or relations' MTSV octets: the dump the request names, handed the
// relations, a relation as a list of one, then what the dump's module is handed.
async function dumped(result, form) {
  const dump = form.dump;
  const function_ = functionOf(await load(dump.file), dump.function, dump.file);
  const handed = [];
  for (const value of dump.arguments) handed.push(await argument(value));
  try {
    return await function_(form.form === 'relation' ? [result] : result, ...handed);
  } catch (error) {
    throw new Failure(`${dump.function} of ${dump.file}: ${error?.constructor?.name}: ${error?.message}`);
  }
}

// A result as JSON holds it: octets as {"$bytes"}, undefined as null; a value
// JSON cannot hold a failure, never a text made of it.
function jsonValue(value) {
  if (value instanceof Uint8Array) return { $bytes: Buffer.from(value).toString('base64') };
  if (Array.isArray(value)) return value.map(jsonValue);
  if (value === undefined || value === null) return null;
  if (typeof value === 'number' && !Number.isFinite(value)) {
    throw new Failure(`a result ${value}, which JSON cannot write`);
  }
  if (['string', 'boolean', 'number'].includes(typeof value)) return value;
  if (Object.getPrototypeOf(value) === Object.prototype) {
    const members = {};
    for (const name of Object.keys(value)) members[name] = jsonValue(value[name]);
    return members;
  }
  throw new Failure(`a result of type ${value?.constructor?.name ?? typeof value}, which JSON cannot hold`);
}

// The response, a JSON text in UTF-8 (RFC 8259).
function writeResponse(path, response) {
  fs.writeFileSync(path, JSON.stringify(response), 'utf8');
}

await main(process.argv);
