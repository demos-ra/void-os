"""The test driver for Python: makes the one call a test runner asks for, and
writes back what it gives.

Run as: python3 driver.py REQUEST RESPONSE, the last two arguments the
pathnames of the request and of the response, each a JSON text, as the test
runner's run.py states them. It writes nothing on standard output or standard
error, which are the code's under test. Its steps, in order, are those of every
language's driver: read the request, build each argument, load the module, find
the function, call it, give each result, write the response.
"""
import base64
import importlib
import json
import os
import sys


class Failure(Exception):
    """A call the driver cannot make or give back, as the response's failure."""


def main(argv):
    """The call, its response written whatever it ends with: results, an error and its reason,
    or the driver's failure."""
    del sys.path[0]  # the driver's own folder is no place the code under test is found
    try:
        response = call(read_request(argv[-2]))
    except Failure as failure:
        response = {"failure": str(failure)}
    write_response(argv[-1], response)
    return 0


def read_request(path):
    """The request: file, function, arguments and results."""
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def call(request):
    """The function called with its arguments: its results, each as its form gives it; or the error
    it ends with, by its class's name and its reason."""
    function = function_of(load(request["file"]), request["function"], request["file"])
    arguments = [argument(value) for value in request["arguments"]]
    try:
        value = function(*arguments)
    except Exception as error:  # every error the code ends with, the runner's to compare
        return {"error": type(error).__name__, "reason": str(error)}
    return {"results": results(value, request["results"])}


def argument(value):
    """One argument: octets for {"$bytes"}, a module for {"$module"}, what a call gives for {"$call"},
    an item of it by "index"; a JSON value as it is."""
    if isinstance(value, list):
        return [argument(item) for item in value]
    if not isinstance(value, dict):
        return value
    if set(value) == {"$bytes"}:
        return base64.b64decode(value["$bytes"])
    if set(value) == {"$module"}:
        return load(value["$module"])
    if "$call" in value:
        given = given_by(value["$call"])
        return given[value["index"]] if "index" in value else given
    return {name: argument(member) for name, member in value.items()}


def given_by(request):
    """What a call the request names gives: a call made for the case's call, not the case's own."""
    function = function_of(load(request["file"]), request["function"], request["file"])
    arguments = [argument(value) for value in request["arguments"]]
    try:
        return function(*arguments)
    except Exception as error:
        raise Failure(f"{request['function']} of {request['file']}: {type(error).__name__}: {error}") from None


def load(file):
    """PY-IMPORT: the module a file holds, imported by its dotted name from the folder above its top
    regular package, so it is the one module the code under test imports."""
    folder = os.path.dirname(os.path.abspath(file))
    names = [os.path.splitext(os.path.basename(file))[0]]
    while os.path.isfile(os.path.join(folder, "__init__.py")):
        names.insert(0, os.path.basename(folder))
        folder = os.path.dirname(folder)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    try:
        return importlib.import_module(".".join(names))
    except Exception as error:
        raise Failure(f"{file}: {type(error).__name__}: {error}") from None


def function_of(module, name, file):
    """The function a module exports by a name."""
    function = getattr(module, name, None)
    if not callable(function):
        raise Failure(f"{file}: no function {name}")
    return function


def results(value, forms):
    """Each result, as its form gives it: a tuple of them for more than one; a relation's or
    relations' dumped as MTSV octets by the dump the request names, handed it."""
    values = list(value) if len(forms) > 1 and isinstance(value, tuple) else [value]
    if len(values) != len(forms) and forms:
        raise Failure(f"{len(values)} results, expected {len(forms)}")
    return [json_value(dumped(result, form) if form["dump"] else result) for result, form in zip(values, forms)]


def dumped(result, form):
    """A relation's or relations' MTSV octets: the dump the request names, handed the relations, a
    relation as a list of one, then what the dump's module is handed."""
    dump = form["dump"]
    function = function_of(load(dump["file"]), dump["function"], dump["file"])
    handed = [argument(value) for value in dump["arguments"]]
    try:
        return function([result] if form["form"] == "relation" else result, *handed)
    except Exception as error:
        raise Failure(f"{dump['function']} of {dump['file']}: {type(error).__name__}: {error}") from None


def json_value(value):
    """A result as JSON holds it: octets as {"$bytes"}, a tuple as a list; a value JSON cannot hold
    a failure, never a text made of it."""
    if isinstance(value, (bytes, bytearray)):
        return {"$bytes": base64.b64encode(value).decode("ascii")}
    if isinstance(value, (list, tuple)):
        return [json_value(item) for item in value]
    if isinstance(value, dict) and all(isinstance(name, str) for name in value):
        return {name: json_value(member) for name, member in value.items()}
    if value is None or isinstance(value, (str, bool, int, float)):
        return value
    raise Failure(f"a result of type {type(value).__name__}, which JSON cannot hold")


def write_response(path, response):
    """The response, a JSON text in UTF-8 (RFC 8259); a number JSON cannot write a failure."""
    try:
        text = json.dumps(response, ensure_ascii=False, allow_nan=False)
    except ValueError as error:
        text = json.dumps({"failure": f"a result JSON cannot write: {error}"})
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
