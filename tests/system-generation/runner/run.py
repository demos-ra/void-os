#!/usr/bin/env python3
"""The test runner: runs each conformance case against each implementation and
gives back each comparison that does not hold, none where a case passes.

It reads only the case files of a conformance folder and an ixit.mtsv, the
implementation extra information for testing (ISO/IEC 9646-1), which says how
each implementation is reached. It knows no project and no language: it calls
the code under test through the implementation's driver, one process per call,
or runs a component's command. Rows cited are the books' runner.N; "runner"
alone cites a choice of this runner's own, stated where it is made.

A finding is MISSING where a case expects what is not there, EXTRA where there
is what no case expects, CHANGED where it is there and differs; each names the
row that owns it, as canon's checker does.

The ixit's sheets and the case format's are the schemas IXIT and CASES below,
the ixit's relations in normal form, each keyed and referenced as KEYS and
REFERENCES give. types: form one of FORMS; item the type of a list's items.
expansion steps: step one of STEPS. providers: a call that fills a parameter
no case gives, its arguments by notation in provider arguments.

The driver is run as its command line, then the request's pathname and the
response's. The request is a JSON object: file, function, arguments, then
results, one {"form", "dump"} for each result. An argument is a JSON value,
{"$bytes": base64}, {"$module": file}, or {"$call": request} for what that
call gives, "index" picking an item of it. A result whose dump is given is that call's octets, handed the
result, as a list where its form is relation. The response is a JSON object:
results, or error and reason, or failure.

Usage: run.py [--repository R] [--conformance C] [--ixit I] [--notation N]...
              [--timeout S] [--keep] [requirement[:case]]...
"""
import base64
import json
import os
import re
import shutil
import signal
import sqlite3
import struct
import subprocess
import sys
import tempfile
import threading
import zlib

CASES = {  # the case format: each relation and its columns, as the books' runner Domains give them
    "cases": ["requirement", "case", "module", "access program", "error", "reason", "output", "diagnostic",
              "assertion"],
    "arguments": ["requirement", "case", "position", "item", "value"],
    "environment": ["requirement", "case", "name", "value"],
    "stdin": ["requirement", "case", "line", "text"],
    "fixtures": ["fixture", "sheet", "record", "field", "value"],
    "placed": ["requirement", "case", "when", "pathname", "fixture"],
    "octets": ["requirement", "case", "pathname", "file", "modified"],
    "zip entries": ["requirement", "case", "pathname", "entry", "name", "method", "text"],
    "database statements": ["requirement", "case", "pathname", "statement", "text"],
    "absent": ["requirement", "case", "pathname"],
    "results": ["requirement", "case", "position", "item", "value"],
    "result instances": ["requirement", "case", "position", "pointer", "type", "value"],
    "stdout lines": ["requirement", "case", "line", "pointer", "type", "value"],
    "expected files": ["requirement", "case", "pathname", "file"],
    "file texts": ["requirement", "case", "pathname", "position", "text"],
    "file instances": ["requirement", "case", "pathname", "pointer", "type", "value"],
}
IXIT = {  # runner: the ixit's relations in normal form (CODD1970 1.3), each by its columns, its key first
    "notations": ["notation"],
    "modules": ["module"],
    "access programs": ["module", "access program"],
    "types": ["type", "form", "item"],
    "errors": ["error"],
    "providers": ["provider", "module", "access program"],
    "module files": ["module", "notation", "file"],
    "functions": ["module", "access program", "notation", "function"],
    "parameters": ["module", "access program", "position", "type", "provided"],
    "results": ["module", "access program", "position", "type"],
    "handed": ["module", "position", "handed"],
    "error names": ["error", "notation", "name"],
    "provider arguments": ["provider", "notation", "position", "argument"],
    "commands": ["module", "access program", "notation", "position", "argument"],
    "time columns": ["relation", "column"],
    "sheets": ["direction", "module", "access program"],
    "expansion steps": ["name", "position", "step", "argument"],
    "drivers": ["notation", "position", "argument"],
}
KEYS = {  # CODD1970 1.4: how many of each relation's first columns are its primary key
    "notations": 1, "modules": 1, "access programs": 2, "types": 1, "errors": 1, "providers": 1, "module files": 2,
    "functions": 3, "parameters": 3, "results": 3, "handed": 2, "error names": 2, "provider arguments": 3,
    "commands": 4, "time columns": 2, "sheets": 1, "expansion steps": 2, "drivers": 2,
}
REFERENCES = [  # CODD1970 1.4: each foreign key, the relation whose primary key it names; empty allowed where marked
    ("access programs", ["module"], "modules", False),
    ("types", ["item"], "types", True),
    ("providers", ["module", "access program"], "access programs", False),
    ("module files", ["module"], "modules", False),
    ("module files", ["notation"], "notations", False),
    ("functions", ["module", "access program"], "access programs", False),
    ("functions", ["notation"], "notations", False),
    ("parameters", ["module", "access program"], "access programs", False),
    ("parameters", ["type"], "types", False),
    ("parameters", ["provided"], "providers", True),
    ("results", ["module", "access program"], "access programs", False),
    ("results", ["type"], "types", False),
    ("handed", ["module"], "modules", False),
    ("handed", ["handed"], "modules", False),
    ("error names", ["error"], "errors", False),
    ("error names", ["notation"], "notations", False),
    ("provider arguments", ["provider"], "providers", False),
    ("provider arguments", ["notation"], "notations", False),
    ("commands", ["module", "access program"], "access programs", False),
    ("commands", ["notation"], "notations", False),
    ("sheets", ["module", "access program"], "access programs", False),
    ("drivers", ["notation"], "notations", False),
]
FORMS = ("text", "number", "boolean", "bytes", "list", "relation", "relations", "json", "none")
STEPS = ("from", "file URI path", "segments", "percent-encode", "double leading", "join")
TIMEOUT = 60  # runner: seconds a call may run before it is stopped, unless --timeout gives others
CONTROL = dict(  # RFC 20 names of the control characters; HT also as MTSV names it, TAB
    [(name, chr(code)) for code, name in enumerate(
        "NUL SOH STX ETX EOT ENQ ACK BEL BS HT LF VT FF CR SO SI DLE DC1 DC2 DC3 DC4 NAK SYN "
        "ETB CAN EM SUB ESC FS GS RS US".split())] + [("TAB", "\t"), ("DEL", "\x7f")])
CONTROL_NAME = re.compile("<(" + "|".join(sorted(CONTROL, key=len, reverse=True)) + ")>")
NAME = {character: name for name, character in CONTROL.items() if name != "HT"}  # HT written TAB, as MTSV names it
CONTROL_CHARACTER = re.compile("[\x00-\x1f\x7f]")
DATE_TIME = re.compile(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?[Zz]\Z")  # RFC 3339 5.6, offset Z
UNRESERVED = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~")  # RFC 3986 2.3


class Stop(Exception):
    """A finding that ends a case: its kind, where, what, and the row that owns it."""

    def __init__(self, kind, where, what, rule):
        super().__init__(kind, where, what, rule)
        self.finding = (kind, where, what, rule)


# the run: every case chosen, against every implementation chosen

def main(argv):
    """Each case chosen, or every case, against each implementation chosen, or every one the ixit
    drives: one line for each finding; exit status 1 where any."""
    settings = options(argv)
    try:
        ixit = read_ixit(settings["ixit"])
    except Stop as stop:
        print("\t".join(stop.finding))
        return 1
    integrity = check_ixit(ixit)
    for finding in integrity:
        print(line_of(finding))
    if integrity:
        return 1
    cases = Cases(settings["conformance"])
    notations = settings["notations"] or sorted({row["notation"] for row in ixit["drivers"]})
    chosen = settings["chosen"]
    try:
        selected = [(r, c) for r, c in cases.all() if not chosen or r in chosen or f"{r}:{c}" in chosen]
    except Stop as stop:
        print("\t".join(stop.finding))
        return 1
    failed = 0
    for notation in notations:
        for requirement, case in selected:
            findings = run(cases, ixit, notation, requirement, case, settings)
            for finding in findings:
                print(line_of((notation, requirement, str(case)) + finding))
            failed += bool(findings)
    print(f"{len(selected) * len(notations)} runs, {failed} failed")
    return 1 if failed else 0


def line_of(fields):
    """A finding as one line, its fields joined by HT, each control character within a field written
    as its name between < and >, as the Types sheet writes a text."""
    return "\t".join(CONTROL_CHARACTER.sub(lambda match: f"<{NAME[match.group(0)]}>", field) for field in fields)


def options(argv):
    """The command line: the repository, the conformance folder (runner.1: the repository's folder
    conformance, unless given), the ixit (beside this file, unless given), the notations, the
    timeout, whether rooms are kept, and the cases chosen."""
    repository = os.getcwd()
    settings = {"conformance": None, "ixit": os.path.join(os.path.dirname(os.path.abspath(__file__)), "ixit.mtsv"),
                "notations": [], "timeout": TIMEOUT, "keep": False, "chosen": []}
    index = 1
    while index < len(argv):
        name = argv[index]
        if name == "--repository":
            repository, index = argv[index + 1], index + 2
        elif name in ("--conformance", "--ixit"):
            settings[name[2:]], index = argv[index + 1], index + 2
        elif name == "--notation":
            settings["notations"].append(argv[index + 1])
            index += 2
        elif name == "--timeout":
            settings["timeout"], index = float(argv[index + 1]), index + 2
        elif name == "--keep":
            settings["keep"], index = True, index + 1
        else:
            settings["chosen"].append(name)
            index += 1
    settings["repository"] = os.path.realpath(repository)
    settings["conformance"] = os.path.realpath(settings["conformance"] or os.path.join(repository, "conformance"))
    return settings


def run(cases, ixit, notation, requirement, case, settings):
    """One case against one implementation, arranged as find, bench, call and compare: each finding,
    none where the case passes; its room removed after, unless kept."""
    variables = {"$REPOSITORY": settings["repository"]}
    try:
        read = find(cases, requirement, case)
        environment = room(variables)
        expansions(ixit, variables)
        stdin = bench(read, environment, variables)
        outcome = call(read, ixit, notation, environment, stdin, variables, settings["timeout"])
        return compare(read, ixit, outcome, variables)
    except Stop as stop:
        return [stop.finding]
    finally:
        if "$PWD" in variables and not settings["keep"]:
            shutil.rmtree(variables["$PWD"], ignore_errors=True)


# case: what the case says, from its file and the files above it

def find(cases, requirement, case):
    """runner.1, runner.9: the case, by its requirement and case, among the cases of the
    conformance folder's files, and never by its place on disk; no case ends the run as no case."""
    for path in cases.paths():
        for row in table(cases.sheets(path), "cases"):
            if row["requirement"] == requirement and row["case"] == str(case):
                return Case(cases, path, row)
    raise Stop("MISSING", f"{requirement} case {case}", "no case", "runner.9")


class Case:
    """One case: its row of cases, its rows of each other relation, and the fixtures and files of
    its module's file and of the nodes above."""

    def __init__(self, cases, path, row):
        self.cases, self.path, self.row = cases, path, row

    def rows(self, sheet):
        """The case's rows of a relation of the case format."""
        return [row for row in table(self.cases.sheets(self.path), sheet)
                if row["requirement"] == self.row["requirement"] and row["case"] == self.row["case"]]

    def fixture(self, name):
        """runner.3, runner.16: a fixture's sheets, held once in the file of the lowest module whose
        cases place it, reached by the cases of that module and of the modules below it."""
        for folder in self.cases.above(self.path):
            for held in sorted(os.listdir(folder)):
                if held.endswith(".mtsv"):
                    rows = [row for row in table(self.cases.sheets(os.path.join(folder, held)), "fixtures")
                            if row["fixture"] == name]
                    if rows:
                        return fixture_sheets(rows)
        raise Stop("MISSING", f"fixture {name}", "held in no file of the case's module or a node above", "runner.3")

    def held(self, name):
        """runner.12, runner.18: a file of octets, held beside the file of the lowest module whose
        cases name it."""
        for folder in self.cases.above(self.path):
            if os.path.isfile(os.path.join(folder, name)):
                return os.path.join(folder, name)
        raise Stop("MISSING", f"file {name}", "held beside no file of the case's module or a node above", "runner.12")


class Cases:
    """The conformance folder's case files, each read once and checked against the case format."""

    def __init__(self, folder):
        self.folder = folder
        self.files = {}

    def paths(self):
        """Each MTSV file in the folder and the folders within it, in name order."""
        found = []
        for folder, folders, names in os.walk(self.folder):
            folders.sort()
            found += [os.path.join(folder, name) for name in sorted(names) if name.endswith(".mtsv")]
        return found

    def all(self):
        """Each case of every file, by its requirement and case."""
        return [(row["requirement"], int(row["case"]))
                for path in self.paths() for row in table(self.sheets(path), "cases")]

    def sheets(self, path):
        """runner.10: a case file's sheets; one the parser rejects, or whose sheets the case format
        does not name or whose headers are not its, ends the run."""
        if path not in self.files:
            where = os.path.relpath(path, self.folder)
            with open(path, "rb") as file:
                sheets = read_mtsv(file.read(), where, "runner.10")
            for name, header, _ in sheets:
                if name not in CASES:
                    raise Stop("EXTRA", f"{where} {name}", "a sheet the case format does not name", "runner.10")
                if header != CASES[name]:
                    raise Stop("CHANGED", f"{where} {name}", f"header {header}, expected {CASES[name]}", "runner.10")
            self.files[path] = sheets
        return self.files[path]

    def above(self, path):
        """The case file's folder, then each folder above it, up to the conformance folder."""
        folder = os.path.dirname(path)
        while True:
            yield folder
            if folder == self.folder:
                return
            folder = os.path.dirname(folder)


def fixture_sheets(rows):
    """fixtures: record 0 the sheet's name, 1 its header, its records from 2, each field not held
    empty."""
    cells = {}
    for row in rows:
        cells.setdefault(int(row["sheet"]), {}).setdefault(int(row["record"]), {})[int(row["field"])] = row["value"]
    sheets = []
    for number in sorted(cells):
        records = cells[number]
        names = records.get(1, {})
        header = [names.get(field, "") for field in range(1, max(names, default=0) + 1)]
        body = [[records[record].get(field, "") for field in range(1, len(header) + 1)]
                for record in sorted(records) if record >= 2]
        sheets.append((records.get(0, {}).get(1, ""), header, body))
    return sheets


# bench: a room made for the case, and what the case places in it

def room(variables):
    """runner.2: an empty directory made for the case, its resolved pathname $PWD, $PWD/home the
    home folder by the variable the platform reads it from, TZ UTC0, and no other variable but PATH
    and those the platform needs to start a program."""
    variables["$PWD"] = os.path.realpath(tempfile.mkdtemp(prefix="case-"))
    variables["$HOME"] = os.path.join(variables["$PWD"], "home")
    environment = {"PATH": os.environ.get("PATH", "")}
    if os.name == "nt":
        environment["SYSTEMROOT"] = os.environ.get("SYSTEMROOT", "")  # Windows starts no program without it
        environment["USERPROFILE"] = variables["$HOME"]  # the variable Windows reads the home folder from
    else:
        environment["HOME"] = variables["$HOME"]  # POSIX XBD 8.3
    environment["TZ"] = "UTC0"  # POSIX XBD 8.3: UTC, offset 0
    return environment


def expansions(ixit, variables):
    """runner.6: each name the ixit builds, as $INPUT, from its steps in order."""
    for name in sorted({row["name"] for row in ixit["expansion steps"]}):
        value = ""
        for row in ordered(pick(ixit, "expansion steps", {"name": name}), "position"):
            value = expansion_step(row["step"], row["argument"], value, variables)
        variables["$" + name] = value


def expansion_step(step, argument, value, variables):
    """One step of an expansion: from a variable; as RFC 8089 writes a file URI's path; split into the
    segments of a path, each empty one left out (RFC 3986 2.2: / delimits them); each segment, or the
    value, percent-encoded as RFC 3986 encodes data, its UTF-8 octets each written as itself where
    unreserved; each, or the value, its leading argument doubled where it begins with it; or the
    segments joined by the argument."""
    if isinstance(value, list) and step in ("percent-encode", "double leading"):
        return [expansion_step(step, argument, segment, variables) for segment in value]
    if step == "from":
        return variables["$" + argument]
    if step == "file URI path":  # RFC 8089 E.2: a drive letter after a /
        value = value.replace(os.sep, "/")
        return value if value.startswith("/") else "/" + value
    if step == "segments":
        return [segment for segment in value.split("/") if segment]
    if step == "percent-encode":  # RFC 3986 2.3, 2.5
        return "".join(chr(octet) if octet in UNRESERVED else f"%{octet:02X}" for octet in value.encode("utf-8"))
    if step == "join":
        return argument.join(value)
    return argument + value if value.startswith(argument) else value  # double leading


def bench(read, environment, variables):
    """What the case places before the call, each as its rows give it: its variables, its fixtures,
    its files of octets, its zip packages and its databases; then its standard input."""
    for row in read.rows("environment"):
        environment[row["name"]] = expand(text(row["value"]), variables)
    for row in read.rows("placed"):
        if row["when"] == "before" and not row["pathname"].startswith(("argument ", "result ")):
            place_fixture(pathname(row["pathname"], variables), read_fixture(read.fixture(row["fixture"]), variables))
    for row in read.rows("octets"):
        place_octets(pathname(row["pathname"], variables), read.held(row["file"]), row["modified"])
    for package in sorted({row["pathname"] for row in read.rows("zip entries")}):
        entries = ordered([row for row in read.rows("zip entries") if row["pathname"] == package], "entry")
        place_zip(pathname(package, variables),
                  [(row["name"], int(row["method"]), expand(text(row["text"]), variables)) for row in entries])
    for database in sorted({row["pathname"] for row in read.rows("database statements")}):
        statements = ordered([row for row in read.rows("database statements") if row["pathname"] == database],
                             "statement")
        place_database(pathname(database, variables), [expand(row["text"], variables) for row in statements])
    return [expand(text(row["text"]), variables) for row in ordered(read.rows("stdin"), "line")]


def place_fixture(path, sheets):
    """runner.3: a fixture placed before, written at its pathname as the generator writes MTSV,
    the directories its pathname needs made."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as file:
        file.write(write_mtsv(sheets))


def place_octets(path, held, modified):
    """runner.12: a file placed by its octets, nothing in it expanded, the directories its pathname
    needs made, and its modification time, where modified gives one, that many seconds before."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    shutil.copyfile(held, path)
    if modified:
        moment = os.stat(path).st_mtime - float(modified)
        os.utime(path, (moment, moment))  # POSIX futimens


def place_zip(path, entries):
    """runner.13: a ZIP file as ZIP-APPNOTE writes one, its entries in order, each with its name, its
    method and the CRC-32 of its text in UTF-8, its data that text compressed by DEFLATE where its
    method is 8 and held as it is otherwise; then the central directory and its end record."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body, directory = b"", b""
    for name, method, data in entries:
        octets, named = data.encode("utf-8"), name.encode("utf-8")
        stored = deflate(octets) if method == 8 else octets
        flags = 0x0800 if not name.isascii() else 0  # APPNOTE 4.4.4 bit 11: the name in UTF-8
        common = struct.pack("<HHHHHIII", 20, flags, method, 0, 0x21, zlib.crc32(octets), len(stored),
                             len(octets))  # APPNOTE 4.4.3 version 2.0; 4.4.6 time 00:00, date 1980-01-01
        directory += (struct.pack("<IH", 0x02014B50, 20) + common
                      + struct.pack("<HHHHHII", len(named), 0, 0, 0, 0, 0, len(body)) + named)
        body += struct.pack("<I", 0x04034B50) + common + struct.pack("<HH", len(named), 0) + named + stored
    end = struct.pack("<IHHHHIIH", 0x06054B50, 0, 0, len(entries), len(entries), len(directory), len(body), 0)
    with open(path, "wb") as file:
        file.write(body + directory + end)


def deflate(octets):
    """RFC 1951: octets compressed, raw, with no zlib wrapper."""
    compressor = zlib.compressobj(wbits=-15)
    return compressor.compress(octets) + compressor.flush()


def place_database(path, statements):
    """runner.14: a database placed, the directories its pathname needs made, built by running its
    statements in order on a new database there."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    connection = sqlite3.connect(path)
    try:
        for statement in statements:
            connection.execute(statement)
        connection.commit()
    finally:
        connection.close()


# call: the case's access program, through the driver or as a command, or nothing

def call(read, ixit, notation, environment, stdin, variables, timeout):
    """The case's call: nothing where its module and access program are empty (runner.8); the
    component's command where the ixit gives one (runner.11); the driver otherwise (runner.4)."""
    module, access_program = read.row["module"], read.row["access program"]
    if not module and not access_program:
        return outcome_of(results=None, forms=[])
    command = pick(ixit, "commands", {"module": module, "access program": access_program, "notation": notation})
    if command:
        return call_program(command, read.rows("arguments"), environment, stdin, variables, timeout)
    return call_in_place(read, ixit, notation, environment, stdin, variables, timeout)


def outcome_of(**given):
    """What a call gives: its failure, error, reason, results and their forms, standard output and
    standard error, and whether it was stopped; each nothing unless given."""
    outcome = {"failure": None, "error": "", "reason": None, "results": None, "forms": [], "stdout": b"",
               "stderr": b"", "stopped": False}
    outcome.update(given)
    return outcome


def call_program(command, arguments, environment, stdin, variables, timeout):
    """runner.11, runner.22: the component run as its command starts it, its operands the case's
    arguments; its exit status result 1, a number, its standard error what reason compares."""
    line = [expand(row["argument"], variables) for row in ordered(command, "position")]
    operands = [expand(text(row["value"]), variables)
                for row in sorted(arguments, key=lambda row: (int(row["position"]), int(row["item"])))]
    status, stdout, stderr, stopped = start(line + operands, environment, stdin, variables["$PWD"], timeout, True)
    return outcome_of(reason=stderr.decode("utf-8", "replace"), results=[status], forms=["number"],
                      stdout=stdout, stderr=stderr, stopped=stopped)


def call_in_place(read, ixit, notation, environment, stdin, variables, timeout):
    """runner.4: the access program called on its module through the implementation's driver, one
    process in $PWD; its error named as the books name it."""
    request = request_of(read, ixit, notation, variables)
    driver = [expand(row["argument"], variables)
              for row in ordered(pick(ixit, "drivers", {"notation": notation}), "position")]
    if not driver:
        raise Stop("MISSING", f"ixit drivers {notation}", "no driver", "runner.4")
    response, stdout, stderr, stopped = drive(driver, request, environment, stdin, variables["$PWD"], timeout)
    names = {row["name"]: row["error"] for row in pick(ixit, "error names", {"notation": notation})}
    error = response.get("error") or ""
    return outcome_of(failure=response.get("failure"), error=names.get(error, error), reason=response.get("reason"),
                      results=decode_bytes(response.get("results")), forms=[r["form"] for r in request["results"]],
                      stdout=stdout, stderr=stderr, stopped=stopped)


def request_of(read, ixit, notation, variables):
    """runner.4: the call the driver makes: the case's arguments by the parameters' positions, then
    what the module is handed; then each result's form, and the dump of a relation's."""
    module, access_program = read.row["module"], read.row["access program"]
    key = {"module": module, "access program": access_program}
    given = [argument(row, read, ixit, notation, variables) for row in ordered(pick(ixit, "parameters", key), "position")]
    request = module_call(ixit, notation, module, access_program, given, variables["$REPOSITORY"])
    request["results"] = []
    for row in ordered(pick(ixit, "results", key), "position"):
        kind = form(ixit, row["type"])[0]
        dump = sheets_call(ixit, notation, "dump", [], variables["$REPOSITORY"]) if kind in ("relation", "relations") else None
        request["results"].append({"form": kind, "dump": dump})
    return request


def argument(parameter, read, ixit, notation, variables):
    """runner.4: one parameter's argument: the fixture placed at it, loaded as relations; or the case's
    value, as its type writes it; or its provider's call; none of them a finding."""
    position, kind = parameter["position"], form(ixit, parameter["type"])[0]
    placed = [row for row in read.rows("placed")
              if row["when"] == "before" and row["pathname"] == f"argument {position}"]
    rows = [row for row in read.rows("arguments") if row["position"] == position]
    if placed:
        octets = write_mtsv(read_fixture(read.fixture(placed[0]["fixture"]), variables))
        load = {"$call": sheets_call(ixit, notation, "load", [encode_bytes(octets)], variables["$REPOSITORY"])}
        return dict(load, index=0) if kind == "relation" else load
    if rows and kind in ("relation", "relations"):
        return []  # one record of item 0 with an empty value, no fixture placed: no sheet
    if rows:
        return read_value(ixit, parameter["type"], rows, variables)
    if parameter["provided"]:
        provider = pick(ixit, "providers", {"provider": parameter["provided"]})[0]
        arguments = [expand(row["argument"], variables) for row in ordered(
            pick(ixit, "provider arguments", {"provider": parameter["provided"], "notation": notation}), "position")]
        return {"$call": module_call(ixit, notation, provider["module"], provider["access program"], arguments,
                                     variables["$REPOSITORY"])}
    raise Stop("MISSING", f"argument {position}", "no value, fixture placed or provider", "runner.4")


def module_call(ixit, notation, module, access_program, arguments, repository):
    """runner.4: a call on a module, loaded from its file: its function, the arguments, then each
    module it is handed, loaded the same way."""
    files = pick(ixit, "module files", {"module": module, "notation": notation})
    functions = pick(ixit, "functions", {"module": module, "access program": access_program, "notation": notation})
    if not files or not functions:
        raise Stop("MISSING", f"ixit module files or functions {module} {access_program} {notation}",
                   "no file or function", "runner.4")
    handed = []
    for row in ordered(pick(ixit, "handed", {"module": module}), "position"):
        file = pick(ixit, "module files", {"module": row["handed"], "notation": notation})
        if not file:
            raise Stop("MISSING", f"ixit module files {row['handed']} {notation}", "no file", "runner.4")
        handed.append({"$module": os.path.join(repository, file[0]["file"])})
    return {"file": os.path.join(repository, files[0]["file"]), "function": functions[0]["function"],
            "arguments": arguments + handed}


def sheets_call(ixit, notation, direction, arguments, repository):
    """The call that loads octets as relations, or dumps relations as octets."""
    row = pick(ixit, "sheets", {"direction": direction})
    if not row:
        raise Stop("MISSING", f"ixit sheets {direction}", "no call", "runner.4")
    return module_call(ixit, notation, row[0]["module"], row[0]["access program"], arguments, repository)


def drive(driver, request, environment, stdin, folder, timeout):
    """The driver started with the request's pathname and the response's: its response, or its
    failure where it writes none."""
    exchange = os.path.realpath(tempfile.mkdtemp(prefix="driver-"))
    asked, answer = os.path.join(exchange, "request.json"), os.path.join(exchange, "response.json")
    try:
        with open(asked, "w", encoding="utf-8") as file:
            json.dump(request, file)
        _, stdout, stderr, stopped = start(driver + [asked, answer], environment, stdin, folder, timeout, False)
        try:
            with open(answer, encoding="utf-8") as file:
                response = json.load(file)
        except (OSError, ValueError):
            response = {"failure": stderr.decode("utf-8", "replace").strip() or "no response"}
    finally:
        shutil.rmtree(exchange, ignore_errors=True)
    return response, stdout, stderr, stopped


def start(command, environment, stdin, folder, timeout, pair):
    """runner.11: a child process in the folder with the environment alone, its standard input each
    line then LF, in UTF-8, written when it starts, and closed once the lines of standard output read
    hold a response for each request among the lines written, or standard output ends; its standard
    output the lines read, then the rest; stopped, with every process it started, after the timeout."""
    process = subprocess.Popen(command, cwd=folder, env=environment, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=os.name != "nt")
    stopped = []
    timer = threading.Timer(timeout, lambda: (stopped.append(True), stop_process(process)))
    errors = []
    reader = threading.Thread(target=lambda: errors.append(process.stderr.read()))
    timer.start()
    reader.start()
    lines = []
    try:
        pending = set()
        for line in stdin:
            sent = message(line)
            if pair and sent is not None and "method" in sent and "id" in sent:  # MCP basic: a request
                pending.add(json.dumps(sent["id"]))
            process.stdin.write(line.encode("utf-8") + b"\n")
        process.stdin.flush()
        while pending:
            line = process.stdout.readline()
            if not line:
                break
            lines.append(line)
            got = message(line)
            if got is not None and "id" in got and ("result" in got or "error" in got):  # MCP basic: a response
                pending.discard(json.dumps(got["id"]))
        process.stdin.close()
        rest = process.stdout.read()
        process.wait()
    finally:
        timer.cancel()
        reader.join()
    return process.returncode, b"".join(lines) + rest, errors[0] if errors else b"", bool(stopped)


def stop_process(process):
    """The process stopped, and on POSIX every process of its session with it."""
    if os.name == "nt":
        process.kill()
    else:
        os.killpg(process.pid, signal.SIGKILL)


# compare: what the case expects, against what the call gives

def compare(read, ixit, outcome, variables):
    """Each finding: the call's end, its error and reason, its streams, its results, the instances
    of its JSON texts, the fixtures, pathnames and files after it."""
    if outcome["stopped"]:
        return [("MISSING", "the call's end", "stopped by the timeout", "runner.11")]
    if outcome["failure"]:
        return [("MISSING", "the driver's response", outcome["failure"], "runner.4")]
    times = {(row["relation"], row["column"]) for row in ixit["time columns"]}
    return (compare_error(read.row, outcome, variables)
            + compare_streams(read.row, outcome)
            + compare_results(read.rows("results"), outcome, variables)
            + compare_result_instances(read.rows("result instances"), outcome, variables)
            + compare_stdout_lines(read.rows("stdout lines"), outcome, variables)
            + compare_placed(read, outcome, times, variables)
            + compare_absent(read.rows("absent"), variables)
            + compare_files(read, outcome, variables)
            + compare_texts(read.rows("file texts"), variables)
            + compare_file_instances(read.rows("file instances"), variables))


def compare_error(case, outcome, variables):
    """runner.15: the error the call ends with, and its reason where the case gives one."""
    want, got = case["error"], outcome["error"]
    if want and not got:
        return [("MISSING", "error", want, "runner.15")]
    if got and not want:
        return [("EXTRA", "error", f"{got}: {outcome['reason']!r}", "runner.15")]
    if got != want:
        return [("CHANGED", "error", f"{got!r}, expected {want!r}", "runner.15")]
    reason = expand(text(case["reason"]), variables)
    if case["reason"] and outcome["reason"] != reason:
        return [("CHANGED", "reason", f"{outcome['reason']!r}, expected {reason!r}", "runner.15")]
    return []


def compare_streams(case, outcome):
    """runner.15: whether standard output holds anything, and whether standard error holds a
    diagnostic, where the case gives them."""
    found = []
    for column, stream in (("output", "stdout"), ("diagnostic", "stderr")):
        held = outcome[stream] != b""
        if case[column] == "true" and not held:
            found.append(("MISSING", column, "nothing written", "runner.15"))
        elif case[column] == "false" and held:
            found.append(("EXTRA", column, repr(outcome[stream][:200]), "runner.15"))
    return found


def compare_results(rows, outcome, variables):
    """runner.15: each result of results, as its text: one record for each item of a list, from 1,
    item 0 alone for one value or for none."""
    found = []
    results, forms = outcome["results"] or [], outcome["forms"]
    for position in sorted({row["position"] for row in rows}, key=int):
        index = int(position) - 1
        mine = ordered([row for row in rows if row["position"] == position], "item")
        if index >= len(forms):
            found.append(("MISSING", f"result {position}", "no such result", "runner.15"))
            continue
        got = results[index] if index < len(results) else None
        if forms[index] == "list":
            want = [expand(text(row["value"]), variables) for row in mine if row["item"] != "0"]
            got = [written(item) for item in got or []]
        else:
            want, got = expand(text(mine[0]["value"]), variables), written(got)
        if got != want:
            found.append(("CHANGED", f"result {position}", f"{got!r}, expected {want!r}", "runner.15"))
    return found


def compare_result_instances(rows, outcome, variables):
    """runner.5: each result of type JSON text by its instances: every instance result instances
    names, and no other."""
    found = []
    results = outcome["results"] or []
    for position in sorted({row["position"] for row in rows}, key=int):
        index = int(position) - 1
        value = results[index] if index < len(results) else None
        found += compare_instances(f"result {position}", value, [r for r in rows if r["position"] == position],
                                   True, variables)
    return found


def compare_stdout_lines(rows, outcome, variables):
    """runner.5: each line of standard output by the instances stdout lines names."""
    found = []
    lines = outcome["stdout"].split(b"\n")
    for number in sorted({row["line"] for row in rows}, key=int):
        line = lines[int(number) - 1] if int(number) <= len(lines) else None
        found += compare_instances(f"stdout line {number}", line, [r for r in rows if r["line"] == number],
                                   False, variables)
    return found


def compare_file_instances(rows, variables):
    """runner.5: each file of file instances by the instances it names."""
    found = []
    for path in sorted({row["pathname"] for row in rows}):
        try:
            with open(pathname(path, variables), "rb") as file:
                data = file.read()
        except OSError:
            found.append(("MISSING", path, "no file", "runner.5"))
            continue
        found += compare_instances(path, data, [row for row in rows if row["pathname"] == path], False, variables)
    return found


def compare_instances(where, data, rows, every, variables):
    """runner.5, runner.21: a JSON text by its instances, each by its pointer, type and value, a text
    JSON text rejects holding none: each instance named, and, where every, no other."""
    found = instances(data) if data is not None else None
    found = found or {}
    want = {row["pointer"]: (row["type"], expand(text(row["value"]), variables) if row["type"] == "string"
                             else row["value"]) for row in rows}
    mismatches = []
    for pointer, expected in want.items():
        if pointer not in found:
            mismatches.append(("MISSING", f"{where} {pointer!r}", repr(expected), "runner.5"))
        elif found[pointer] != expected:
            mismatches.append(("CHANGED", f"{where} {pointer!r}", f"{found[pointer]!r}, expected {expected!r}",
                               "runner.5"))
    if every:
        mismatches += [("EXTRA", f"{where} {pointer!r}", repr(value), "runner.5")
                       for pointer, value in found.items() if pointer not in want]
    return mismatches


def compare_placed(read, outcome, times, variables):
    """runner.16: each fixture placed after, compared as its sheets with what is at its pathname:
    a file, standard output, or a result."""
    found = []
    for row in read.rows("placed"):
        if row["when"] != "after":
            continue
        where = row["pathname"]
        data = placed_data(where, outcome, variables)
        if data is None:
            found.append(("MISSING", where, "nothing there", "runner.16"))
        else:
            found += compare_sheets(where, read_fixture(read.fixture(row["fixture"]), variables), data, times)
    return found


def placed_data(where, outcome, variables):
    """What is at a pathname after the call: standard output for -, a result's octets for result
    and a position, a result of type text as the octets of its UTF-8, a file's octets otherwise;
    None where nothing is."""
    if where == "-":
        return outcome["stdout"]
    if where.startswith("result "):
        results, index = outcome["results"] or [], int(where.split(" ")[1]) - 1
        if index < len(results) and isinstance(results[index], str):
            return results[index].encode("utf-8")
        return results[index] if index < len(results) and isinstance(results[index], bytes) else None
    try:
        with open(pathname(where, variables), "rb") as file:
            return file.read()
    except OSError:
        return None


def compare_sheets(where, expected, data, times):
    """runner.16, runner.20: sheets against a fixture's, read as values, by name, header and record, in
    order; a field of a time column any RFC 3339 date-time with the offset Z."""
    try:
        actual = read_mtsv(data, where, "runner.16")
    except Stop as stop:
        return [stop.finding]
    names, want_names = [s[0] for s in actual], [s[0] for s in expected]
    if names != want_names:
        return [("CHANGED", where, f"sheets {names}, expected {want_names}", "runner.16")]
    found = []
    for (name, header, records), (_, want_header, want_records) in zip(actual, expected):
        if header != want_header:
            found.append(("CHANGED", f"{where} {name}", f"header {header}, expected {want_header}", "runner.16"))
            continue
        for number in range(max(len(records), len(want_records))):
            at = f"{where} {name} record {number + 2}"
            if number >= len(records):
                found.append(("MISSING", at, repr(want_records[number]), "runner.16"))
            elif number >= len(want_records):
                found.append(("EXTRA", at, repr(records[number]), "runner.16"))
            else:
                want = want_records[number]
                if not all(matches(w, a, (name, column) in times) for column, w, a in zip(header, want, records[number])):
                    found.append(("CHANGED", at, f"{records[number]}, expected {want}", "runner.16"))
    return found


def matches(expected, actual, time):
    """runner.20: a field equal, or, in a time column, any RFC 3339 date-time with the offset Z."""
    return bool(DATE_TIME.match(actual)) if time else expected == actual


def compare_absent(rows, variables):
    """runner.17: each pathname of absent holding nothing after the call."""
    return [("EXTRA", row["pathname"], "exists", "runner.17") for row in rows
            if os.path.lexists(pathname(row["pathname"], variables))]


def compare_files(read, outcome, variables):
    """runner.18: each expected file holding, after the call, the octets of the file it names."""
    found = []
    for row in read.rows("expected files"):
        with open(read.held(row["file"]), "rb") as file:
            want = file.read()
        got = outcome["stdout"] if row["pathname"] == "-" else placed_data(row["pathname"], outcome, variables)
        if got is None:
            found.append(("MISSING", row["pathname"], "no file", "runner.18"))
        elif got != want:
            found.append(("CHANGED", row["pathname"], f"octets differ from {row['file']}", "runner.18"))
    return found


def compare_texts(rows, variables):
    """runner.19: each text held within one of the lines, or the incomplete line, of its file."""
    found = []
    for path in sorted({row["pathname"] for row in rows}):
        try:
            with open(pathname(path, variables), encoding="utf-8") as file:
                lines = file.read().split("\n")  # POSIX XBD 3.206, 3.195
        except (OSError, UnicodeDecodeError):
            found.append(("MISSING", path, "no file of UTF-8 text", "runner.19"))
            continue
        for row in ordered([row for row in rows if row["pathname"] == path], "position"):
            want = expand(text(row["text"]), variables)
            if not any(want in line for line in lines):
                found.append(("MISSING", path, f"no line holds {want!r}", "runner.19"))
    return found


# values: how a case's values are read and expanded

def read_value(ixit, type_, rows, variables):
    """runner.7: an argument, as its type's form writes it: item 0 for one value, from 1 for each
    item of a list; a number as a JSON text writes it, a boolean true or false, bytes as UTF-8."""
    kind, item = form(ixit, type_)
    if kind == "list":
        return [read_value(ixit, item, [row], variables) for row in ordered(rows, "item") if row["item"] != "0"]
    value = expand(text(rows[0]["value"]), variables)
    if kind == "number":
        return json.loads(value)
    if kind == "boolean":
        return value == "true"
    if kind == "bytes":
        return encode_bytes(value.encode("utf-8"))
    return value


def form(ixit, type_):
    """runner.7: a type's form and its items' type, as the ixit's types give them."""
    row = pick(ixit, "types", {"type": type_})
    if not row:
        raise Stop("MISSING", f"ixit types {type_}", "no form", "runner.7")
    if row[0]["form"] not in FORMS:
        raise Stop("CHANGED", f"ixit types {type_}", f"form {row[0]['form']!r}, expected one of {FORMS}", "runner.7")
    return row[0]["form"], row[0]["item"]


def pathname(value, variables):
    """runner.6, runner.8: a pathname expanded, each / the platform's separator, a relative one
    relative to the repository."""
    value = expand(value, variables).replace("/", os.sep)
    return value if value == "-" or os.path.isabs(value) else os.path.join(variables["$REPOSITORY"], value)


def expand(value, variables):
    """runner.6: $PWD, $HOME, $INPUT, $REPOSITORY and each name the ixit builds, and nothing else."""
    for name in sorted(variables, key=len, reverse=True):
        value = value.replace(name, variables[name])
    return value


def text(value):
    """The Types sheet's text: each control character written as its name between < and >."""
    return CONTROL_NAME.sub(lambda match: CONTROL[match.group(1)], value)


def read_fixture(sheets, variables):
    """runner.6, runner.7: a fixture's sheet names, headers and fields, each read as the Types sheet's
    text is written, then expanded."""
    def value(field):
        return expand(text(field), variables)

    return [(value(name), [value(field) for field in header], [[value(field) for field in record] for record in records])
            for name, header, records in sheets]


# frame: the ixit, MTSV, JSON and octets, which every part uses

def read_ixit(path):
    """The ixit's sheets, each a list of dicts by its header, every sheet of IXIT and no other."""
    try:
        with open(path, "rb") as file:
            sheets = read_mtsv(file.read(), path, "runner")
    except OSError:
        raise Stop("MISSING", path, "no ixit", "runner") from None
    ixit = {}
    for name, header, _ in sheets:
        if name not in IXIT:
            raise Stop("EXTRA", f"{path} {name}", "a sheet the ixit does not name", "runner")
        if header != IXIT[name]:
            raise Stop("CHANGED", f"{path} {name}", f"header {header}, expected {IXIT[name]}", "runner")
        ixit[name] = table(sheets, name)
    for name in IXIT:
        if name not in ixit:
            raise Stop("MISSING", f"{path} {name}", "a sheet the ixit names", "runner")
    return ixit


def check_ixit(ixit):
    """CODD1970 1.4: each relation's primary key unique and never empty, each foreign key the primary
    key of a row of the relation it names; each form one of FORMS and each step one of STEPS."""
    found = []
    for name, rows in ixit.items():
        key = IXIT[name][:KEYS[name]]
        seen = set()
        for row in rows:
            value = tuple(row[column] for column in key)
            if "" in value:
                found.append(("MISSING", f"ixit {name} {value}", "a primary key field", "CODD1970 1.4"))
            elif value in seen:
                found.append(("EXTRA", f"ixit {name} {value}", "a second row of one primary key", "CODD1970 1.4"))
            seen.add(value)
    for name, columns, target, optional in REFERENCES:
        keys = {tuple(row[column] for column in IXIT[target][:KEYS[target]]) for row in ixit[target]}
        for row in ixit[name]:
            value = tuple(row[column] for column in columns)
            if not (optional and value == ("",) * len(columns)) and value not in keys:
                found.append(("MISSING", f"ixit {target} {value}", f"the row {name} names", "CODD1970 1.4"))
    found += [("CHANGED", f"ixit types {row['type']}", f"form {row['form']!r}, expected one of {FORMS}", "runner")
              for row in ixit["types"] if row["form"] not in FORMS]
    found += [("CHANGED", f"ixit expansion steps {row['name']}", f"step {row['step']!r}, expected one of {STEPS}",
               "runner") for row in ixit["expansion steps"] if row["step"] not in STEPS]
    return found


def pick(ixit, sheet, match):
    """The rows of an ixit sheet whose columns hold the values given."""
    return [row for row in ixit[sheet] if all(row[column] == value for column, value in match.items())]


def ordered(rows, column):
    """Rows by a column that holds a number, from the least."""
    return sorted(rows, key=lambda row: int(row[column]))


def read_mtsv(data, where, rule):
    """MTSV-DRAFT: the sheets of an MTSV file in UTF-8, a U+FEFF at its start an encoding signature;
    the lines before the first FF the first sheet, its name empty; each line that begins with FF a
    new sheet; LF or CRLF each line's break; every record as many fields as its sheet's header."""
    try:
        text_ = data.decode("utf-8") if isinstance(data, bytes) else data
    except UnicodeDecodeError:
        raise Stop("CHANGED", where, "not MTSV: not UTF-8", rule) from None
    lines = text_.removeprefix("﻿").split("\n")
    if lines[-1] != "":
        raise Stop("CHANGED", where, f"not MTSV: line {len(lines)} has no line break", rule)
    sheets = [["", None, []]]
    for number, line in enumerate(lines[:-1], 1):
        line = line.removesuffix("\r")
        if "\r" in line or "\f" in line[1:]:
            raise Stop("CHANGED", where, f"not MTSV: line {number}", rule)
        if line.startswith("\f"):
            sheets.append([line[1:], None, []])
        elif sheets[-1][1] is None:
            sheets[-1][1] = line.split("\t")
        elif len(line.split("\t")) != len(sheets[-1][1]):
            raise Stop("CHANGED", where, f"not MTSV: line {number} has not as many fields as its header", rule)
        else:
            sheets[-1][2].append(line.split("\t"))
    if sheets[0][1] is None:
        sheets.pop(0)  # no lines before the first FF: no first sheet
    return [(name, header or [], records) for name, header, records in sheets]


def write_mtsv(sheets):
    """MTSV-DRAFT, as a generator writes it: an FF line before every sheet, a line break after
    every record, in UTF-8; a name or field that holds HT, LF, FF or CR is not written (Generators,
    block 4), and ends the case as a finding of runner.4."""
    for name, header, records in sheets:
        for field in [name] + header + [field for record in records for field in record]:
            if any(character in field for character in "\t\n\f\r"):
                raise Stop("CHANGED", f"fixture sheet {name!r}", f"a field {field!r} MTSV cannot hold", "runner.4")
    out = []
    for name, header, records in sheets:
        out.append("\f" + name + "\n" + "\t".join(header) + "\n")
        out.extend("\t".join(record) + "\n" for record in records)
    return "".join(out).encode("utf-8")


def table(sheets, name):
    """The records of a sheet, each a dict by its header."""
    for sheet, header, records in sheets:
        if sheet == name:
            return [dict(zip(header, record)) for record in records]
    return []


class Number(str):
    """A JSON number, kept as it is written."""


def instances(data):
    """RFC 8259, RFC 6901: each instance of a JSON text in UTF-8 by its pointer, its type and its
    value: a string's characters, a number as written, true or false, empty for null, an object and
    an array; None where the text is not a JSON text, its names not unique among them."""
    def pairs(items):
        if len({name for name, _ in items}) != len(items):
            raise ValueError("names not unique")
        return dict(items)

    def reject(constant):
        raise ValueError(constant)

    try:
        value = json.loads(data.decode("utf-8") if isinstance(data, bytes) else data, object_pairs_hook=pairs,
                           parse_int=Number, parse_float=Number, parse_constant=reject)
    except (ValueError, RecursionError):
        return None
    found = {}

    def walk(pointer, value):
        if isinstance(value, dict):
            found[pointer] = ("object", "")
            for name, member in value.items():
                walk(pointer + "/" + name.replace("~", "~0").replace("/", "~1"), member)
        elif isinstance(value, list):
            found[pointer] = ("array", "")
            for index, member in enumerate(value):
                walk(f"{pointer}/{index}", member)
        elif isinstance(value, Number):
            found[pointer] = ("number", str(value))
        elif isinstance(value, bool):
            found[pointer] = ("boolean", "true" if value else "false")
        elif value is None:
            found[pointer] = ("null", "")
        else:
            found[pointer] = ("string", value)

    walk("", value)
    return found


def message(line):
    """A line that holds a JSON object, as a dict; None for any other line."""
    try:
        value = json.loads(line)
    except (ValueError, UnicodeDecodeError):
        return None
    return value if isinstance(value, dict) else None


def written(value):
    """A result as its text: true or false, octets as UTF-8, nothing as empty, a number as a JSON
    text writes it, a text as it is."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value)


def encode_bytes(octets):
    """Octets as the driver takes them."""
    return {"$bytes": base64.b64encode(octets).decode("ascii")}


def decode_bytes(value):
    """The driver's results, each {"$bytes": ...} back to octets."""
    if isinstance(value, dict) and set(value) == {"$bytes"}:
        return base64.b64decode(value["$bytes"])
    if isinstance(value, list):
        return [decode_bytes(item) for item in value]
    if isinstance(value, dict):
        return {name: decode_bytes(member) for name, member in value.items()}
    return value


if __name__ == "__main__":
    sys.exit(main(sys.argv))
