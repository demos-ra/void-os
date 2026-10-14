"""Write the outputs of the books the Values give: values.mtsv in each package (values.2), python/pyproject.toml
(distribution-package.1) and javascript/package.json (distribution-package.2).

A stand-in, to be replaced by the one system generation reader that writes every output of the books from rules
the books state (patches/fracas.mtsv, correction C1 of defect D1). values.mtsv is written through the mtsv package;
pyproject.toml as TOML-ABNF writes a table and a keyval; package.json as RFC 8259 writes a JSON text.

Usage: derive_outputs.py REPOSITORY [MTSV_SOURCE], MTSV_SOURCE the folder that holds the mtsv package where it is
not installed. Run again after the books change; an output that differs from what this writes is out of step.
"""
import json
import os
import sys

if len(sys.argv) > 2:
    sys.path.insert(0, sys.argv[2])
import mtsv  # noqa: E402

repository = sys.argv[1]
BOOKS = ["void-os", "relational-model", "data-bank", "tools", "hooks", "view", "system-generation"]  # the groups' order


def values():
    """The Values of every book, the root's first, then each group's in the order of the groups: Value and Given."""
    found = []
    for book in BOOKS:
        with open(os.path.join(repository, "spec", book + ".mtsv"), "rb") as file:
            for sheet in mtsv.load(file):
                if sheet["sheet name"] == "Values" and sheet["header"]:
                    position = {name: index for index, name in enumerate(sheet["header"])}
                    found += [(record[position["Value"]], record[position["Given"]]) for record in sheet["records"]]
    return found


def write_values(given):
    """values.2: values.mtsv, the Values sheet's Value and Given columns, as the generator writes a sheet."""
    sheet = [{"sheet name": "Values", "header": ["Value", "Given"], "records": [list(pair) for pair in given]}]
    for path in ("python/src/void_os/system_generation/values/values.mtsv",
                 "javascript/src/system-generation/values/values.mtsv"):
        with open(os.path.join(repository, path), "wb") as file:
            mtsv.dump(sheet, file)


def toml_string(text):
    """A TOML basic string: the characters JSON escapes, escaped as TOML-ABNF basic-string escapes them."""
    return json.dumps(text, ensure_ascii=False)


def write_pyproject(value):
    """distribution-package.1: the build system the Values build requires and build backend name, and the project:
    name void-os, the version, requires-python, the dependency the Value python dependency mcp gives, the license,
    Apache-2.0 by the user's choice where the books' placeholder gives MIT, the [project.scripts] entry of the
    void-os command, and values.mtsv as package data."""
    lines = [
        "[build-system]",
        f"requires = [{toml_string(value['build requires'])}]",
        f"build-backend = {toml_string(value['build backend'])}",
        "",
        "[project]",
        f"name = {toml_string('void-os')}",
        f"version = {toml_string(value['version'])}",
        f"requires-python = {toml_string(value['requires-python'])}",
        f"dependencies = [{toml_string(value['python dependency mcp'])}]",
        f"license = {toml_string('Apache-2.0')}",
        "",
        "[project.scripts]",
        f"{value['void-os command']} = {toml_string('void_os._void_os:void_os')}",
        "",
        "[tool.setuptools.package-data]",
        f"{toml_string('void_os.system_generation.values')} = [{toml_string('values.mtsv')}]",
    ]
    with open(os.path.join(repository, "python/pyproject.toml"), "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def requirement(given):
    """A name and a version range, as npm install writes them: the name, @, the range; a scoped name begins with @."""
    at = given.rindex("@")
    return given[:at], given[at + 1:]


def write_package(value):
    """distribution-package.2: the name void-os, the version, the type module, the bin entry of the void-os command
    naming src/void-os.js, the engines the Value node engine gives, the dependencies the Values javascript dependency
    server and zod give, the license, Apache-2.0 by the user's choice where the books' placeholder gives MIT, its
    files the folder src alone, and the mcpName the Value registry name gives."""
    dependencies = dict(requirement(value[name]) for name in ("javascript dependency server", "javascript dependency zod"))
    package = {"name": "void-os", "version": value["version"], "type": "module",
               "bin": {value["void-os command"]: "src/void-os.js"}, "engines": {"node": value["node engine"]},
               "dependencies": dependencies, "license": "Apache-2.0", "files": ["src"], "mcpName": value["registry name"]}
    with open(os.path.join(repository, "javascript/package.json"), "w", encoding="utf-8") as file:
        file.write(json.dumps(package, indent=2, ensure_ascii=False) + "\n")


given = values()
write_values(given)
write_pyproject(dict(given))
write_package(dict(given))
print(len(given), "values written")
