"""Derive void-os's ixit.mtsv from the books (spec/) and the mapping (.mapping.mtsv).

A stand-in, to be replaced by the one system generation reader that writes every
output of the books (ixit.mtsv, values.mtsv, server.json) from rules the books
state. Each sheet's rows come from the book sheet or mapping rule named at it;
three sheets (sheets, expansion steps, drivers) are written here, each from the
source cited. Written through the mtsv package, never by hand.

Usage: derive_ixit.py REPOSITORY OUTPUT [MTSV_SOURCE], MTSV_SOURCE the folder
that holds the mtsv package where it is not installed. Run again after the books
change; an ixit that differs from what this writes is out of step with them.
"""
import keyword
import os
import sys

if len(sys.argv) > 3:
    sys.path.insert(0, sys.argv[3])
import mtsv  # noqa: E402

repository, output = sys.argv[1], sys.argv[2]
BOOKS = ["void-os", "relational-model", "data-bank", "tools", "hooks", "view", "system-generation"]


def book_rows(sheet):
    """Every book's rows of a sheet, the root's first, then each group's, each a dict by its header."""
    rows = []
    for book in BOOKS:
        with open(os.path.join(repository, "spec", book + ".mtsv"), "rb") as file:
            for found in mtsv.load(file):
                if found["sheet name"] == sheet and found["header"]:
                    rows += [dict(zip(found["header"], record)) for record in found["records"]]
    return rows


def words(name, separators):
    for separator in separators:
        name = name.replace(separator, " ")
    return name.split()


def python_function(name):
    """Mapping 6-naming, python function: lowercase; spaces and hyphens as underscores; a keyword, then _."""
    written = name.lower().replace(" ", "_").replace("-", "_")
    return written + "_" if keyword.iskeyword(written) else written


def javascript_function(name):
    """Mapping 6-naming, javascript function: the words split at each space, hyphen and underscore, the
    first lowercase, each later one capitalized, joined; a ReservedWord's export keeps the name."""
    parts = words(name, " -_")
    return parts[0].lower() + "".join(part[:1].upper() + part[1:] for part in parts[1:])


def error_name(name):
    """Mapping 6-naming, python exception and javascript error: the words split at each space and
    hyphen, each capitalized, joined, then Error."""
    return "".join(part[:1].upper() + part[1:] for part in words(name, " -")) + "Error"


def form_of(written):
    """The runner's form of a Types row, by its Written column."""
    if written.startswith("one record for each item"):
        return "list"
    if written.startswith("the fixture placed at it, its sheets in order"):
        return "relations"
    if written.startswith("the fixture placed at it"):
        return "relation"
    if written.startswith("its instances in result instances"):
        return "json"
    if written.startswith(("nothing", "never written")):
        return "none"
    if written == "true or false":
        return "boolean"
    if written.startswith("as a JSON text writes the number"):
        return "number"
    if written.startswith("the text the octets hold"):
        return "bytes"
    return "text"


NOTATIONS = {"python": (".py", python_function), "javascript": (".js", javascript_function)}
files = book_rows("Files")
access_programs = book_rows("Access programs")
parameters = book_rows("Parameters")


def module_file(module, notation):
    """Mapping 2-modules: the module's interface file, the one Files row of its module whose path ends
    .py or .js, under the notation's folder."""
    found = [row["Path"] for row in files if row["Module"] == module and row["Path"].startswith(notation + "/")
             and row["Path"].endswith(NOTATIONS[notation][0])]
    return found[0] if found else None


sheets = {}
sheets["notations"] = [[notation] for notation in NOTATIONS]
sheets["modules"] = [[row["Module"]] for row in book_rows("Modules")]
sheets["access programs"] = [[row["Module"], row["Access program"]] for row in access_programs]
sheets["types"] = [[row["Type"], form_of(row["Written"]), row["Item type"]] for row in book_rows("Types")]
errors = []
for row in book_rows("Errors"):
    if row["Error"] not in errors:
        errors.append(row["Error"])
sheets["errors"] = [[error] for error in errors]
provided = [(row["Module"], row["Access program"]) for row in parameters if row["Relation"] == "Values"]
sheets["providers"] = [["values", "values", "values"]] if provided else []
sheets["module files"] = [[module[0], notation, module_file(module[0], notation)]
                          for module in sheets["modules"] for notation in NOTATIONS if module_file(module[0], notation)]
sheets["functions"] = [[row["Module"], row["Access program"], notation, rule(row["Access program"])]
                       for row in access_programs for notation, (_, rule) in NOTATIONS.items()]
sheets["parameters"] = [[row["Module"], row["Access program"], row["Position"], row["Type"],
                         "values" if row["Relation"] == "Values" else ""] for row in parameters]
sheets["results"] = [[row["Module"], row["Access program"], row["Position"], row["Type"]]
                     for row in book_rows("Results")]
handed, positions = [], {}
for row in book_rows("Compositions"):
    positions[row["Part"]] = positions.get(row["Part"], 0) + 1
    handed.append([row["Part"], str(positions[row["Part"]]), row["Handed"]])
sheets["handed"] = handed
sheets["error names"] = [[error, notation, error_name(error)] for error in errors for notation in NOTATIONS]
sheets["provider arguments"] = [["values", notation, "1", "$REPOSITORY/" + os.path.dirname(module_file("values", notation))]
                                for notation in NOTATIONS] if provided else []
commands = []
for row in access_programs:
    if row["Starts"]:
        python_file = module_file(row["Module"], "python")
        dotted = python_file[len("python/src/"):-len(".py")].replace("/", ".")
        start = (f"import sys; sys.path.insert(0, '$REPOSITORY/python/src'); "
                 f"from {dotted} import {python_function(row['Access program'])} as start; sys.exit(start())")
        commands += [[row["Module"], row["Access program"], "python", "1", "python3"],
                     [row["Module"], row["Access program"], "python", "2", "-c"],
                     [row["Module"], row["Access program"], "python", "3", start],
                     [row["Module"], row["Access program"], "javascript", "1", "node"],
                     [row["Module"], row["Access program"], "javascript", "2",
                      "$REPOSITORY/javascript/src/" + row["Starts"].replace(" ", "-") + ".js"]]
sheets["commands"] = commands
sheets["time columns"] = [[row["Relation"], row["Column"]] for row in book_rows("Domains") if row["Type"] == "time"]
sheets["sheets"] = [["load", "relational model", "load"], ["dump", "relational model", "dump"]]
sheets["expansion steps"] = [["INPUT", "1", "from", "PWD"], ["INPUT", "2", "file URI path", ""],
                             ["INPUT", "3", "segments", ""], ["INPUT", "4", "percent-encode", ""],
                             ["INPUT", "5", "double leading", "_"], ["INPUT", "6", "join", "/"]]
sheets["drivers"] = [["python", "1", "python3"],
                     ["python", "2", "$REPOSITORY/python/tests/void_os/system_generation/runner/driver.py"],
                     ["javascript", "1", "node"],
                     ["javascript", "2", "$REPOSITORY/javascript/tests/system-generation/runner/driver.mjs"]]

sys.path.insert(0, os.path.join(repository, "tests", "system-generation", "runner"))
import run  # noqa: E402  the runner's own schema, so the two cannot differ

out = [{"sheet name": name, "header": run.IXIT[name], "records": sheets[name]} for name in run.IXIT]
with open(output, "wb") as file:
    mtsv.dump(out, file)
for name in run.IXIT:
    print(len(sheets[name]), name)
