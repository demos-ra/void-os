"""Write the outputs of the books: values.mtsv in each package (values.2), python/pyproject.toml
(distribution-package.1), javascript/package.json (distribution-package.2), server.json (distribution-package.3),
each README (distribution-package.4) and each LICENSE (distribution-package.5).

A stand-in, to be replaced by the one system generation reader that writes every output of the books from rules
the books state (patches/fracas.mtsv, corrections C1 and C13). values.mtsv is written through the mtsv package;
pyproject.toml as TOML-ABNF writes a table and a keyval; package.json and server.json as RFC 8259 writes a JSON text;
each README as plain text; each LICENSE as the root LICENSE.

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
SCHEMA = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"  # MCP-REGISTRY server.json


def rows(sheet_name):
    """The records of a sheet of every book, the root's first, then each group's in the order of the groups, each a
    dict by its header."""
    found = []
    for book in BOOKS:
        with open(os.path.join(repository, "spec", book + ".mtsv"), "rb") as file:
            for sheet in mtsv.load(file):
                if sheet["sheet name"] == sheet_name and sheet["header"]:
                    found += [dict(zip(sheet["header"], record)) for record in sheet["records"]]
    return found


def values():
    """The Values of every book: Value and Given."""
    return [(row["Value"], row["Given"]) for row in rows("Values")]


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
    name void-os, the version, the readme, README as plain text (D18), requires-python, the dependency the Value
    python dependency mcp gives, the license, Apache-2.0 by the user's choice where the books' placeholder gives MIT
    (D17), the [project.scripts] entry of the void-os command, and values.mtsv as package data."""
    lines = [
        "[build-system]",
        f"requires = [{toml_string(value['build requires'])}]",
        f"build-backend = {toml_string(value['build backend'])}",
        "",
        "[project]",
        f"name = {toml_string('void-os')}",
        f"version = {toml_string(value['version'])}",
        f"readme = {{file = {toml_string('README')}, content-type = {toml_string('text/plain')}}}",
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
    server and zod give, the license, Apache-2.0 by the user's choice where the books' placeholder gives MIT (D17),
    its files the folder src alone, and the mcpName the Value registry name gives."""
    dependencies = dict(requirement(value[name]) for name in ("javascript dependency server", "javascript dependency zod"))
    package = {"name": "void-os", "version": value["version"], "type": "module",
               "bin": {value["void-os command"]: "src/void-os.js"}, "engines": {"node": value["node engine"]},
               "dependencies": dependencies, "license": "Apache-2.0", "files": ["src"], "mcpName": value["registry name"]}
    with open(os.path.join(repository, "javascript/package.json"), "w", encoding="utf-8") as file:
        file.write(json.dumps(package, indent=2, ensure_ascii=False) + "\n")


def write_server(value):
    """distribution-package.3: server.json, its $schema (D18), the server named by the Value registry name, described
    by the Value server description, at the version, and two packages, the npm package and the PyPI package, each
    named void-os, at the version, each run with no argument over stdio."""
    packages = [{"registryType": registry, "identifier": "void-os", "version": value["version"],
                 "transport": {"type": "stdio"}} for registry in ("npm", "pypi")]
    server = {"$schema": SCHEMA, "name": value["registry name"], "description": value["server description"],
              "version": value["version"], "packages": packages}
    with open(os.path.join(repository, "server.json"), "w", encoding="utf-8") as file:
        file.write(json.dumps(server, indent=2, ensure_ascii=False) + "\n")


def tree():
    """The Modules sheet's tree: each module, in the sheet's order, with its depth, the root at 0, and its secret."""
    modules = rows("Modules")
    parent = {row["Module"]: row["Parent"] for row in modules}

    def depth(module):
        return 0 if not parent[module] else depth(parent[module]) + 1

    return [(depth(row["Module"]), row["Module"], row["Secret"]) for row in modules]


def write_readmes(value):
    """distribution-package.4: each README says what void-os is, as scope.1 says it, and how it is installed, pipx
    install void-os for the PyPI package and npm install --global void-os for the npm package; lays out the modules
    as the Modules sheet's tree, each by its secret on one line, indented two spaces by its depth; and, for the PyPI
    package, holds the Value registry name as the registry's ownership verification names it, mcp-name: and the
    name on a line of its own."""
    scope = next(row["Statement"] for row in rows("Scope") if row["Id"] == "scope.1")
    what = "void-os is " + scope.split("defines void-os, ", 1)[1]
    modules = ["  " * level + f"{module}: {secret}" for level, module, secret in tree()]
    for path, install, verification in (
            ("python/README", "pipx install void-os", [f"mcp-name: {value['registry name']}", ""]),
            ("javascript/README", "npm install --global void-os", [])):
        lines = ["void-os", "", what, "", "Install", "", "    " + install, ""] + verification + ["Modules", ""] + modules
        with open(os.path.join(repository, path), "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")


def write_licenses():
    """distribution-package.5: each LICENSE the root LICENSE's text, the Apache License 2.0 by the user's choice where
    the books' placeholder gives MIT (D17)."""
    with open(os.path.join(repository, "LICENSE"), encoding="utf-8") as file:
        text = file.read()
    for path in ("python/LICENSE", "javascript/LICENSE"):
        with open(os.path.join(repository, path), "w", encoding="utf-8") as file:
            file.write(text)


given = values()
value = dict(given)
write_values(given)
write_pyproject(value)
write_package(value)
write_server(value)
write_readmes(value)
write_licenses()
print(len(given), "values written; pyproject.toml, package.json, server.json, two READMEs and two LICENSEs written")
