![VOID OS](banner.svg)

# void-os

**Memory is space. Time is CPU cycles.**

Void OS is the gate operating within the liminal space between unstructured
and structured data. It is your personal operating system for Artificial and
Super Intelligence agent infrastructure. It gives memory a shape: a 3D grid,
mapped on the x, y and z axes, of sheets, columns and rows. Relational mapping
in pure text is the native format for agents, which means your agents operate
at maximum productivity.

Databases have always been the way to store and manage data, and their shape
never changes: a book for each subject, a sheet for each kind of thing, a
column for each category, a row for each entry, and a cell for each value.
That three-dimensional grid powers the entirety of Void OS: your data, one
shape everywhere. You and your agents all read, write and query one grid.

## The structure

Void OS has no schema of its own to learn. It takes yours.

Your agents already work in a hierarchy: the folders of your projects and
repositories. Void OS keys everything it keeps by the folder an agent works
in, so the data bank's namespace is your file system's. The path is
deterministic: the folder's resolved path, each segment percent-encoded
(RFC 3986), becomes the book's path, with no registry, index or configuration
in between.

```
~/Documents/void-os/                     the data bank
└── home/you/projects/app.mtsv           a book: one folder you work in
    ├── hook input                       a sheet: one row per event kept
    ├── _instances                       a sheet: one row per value in an event
    └── _runs                            a sheet: long text, one row per run
```

The containment is strict and uniform: folders hold books, books hold sheets,
sheets hold rows, rows hold cells. The same read path serves any folder of
yours, a directory as its books and a file as one book, so your workspace and
your data bank are one structure, and your agents operate on it directly.

A book is one [MTSV](https://github.com/demos-ra/mtsv-spec) file, a format
registered as an IETF Internet-Draft. Each of its three axes is delimited by
one character:

| Axis | Holds   | Separated by |
|------|---------|--------------|
| x    | columns | a tab        |
| y    | rows    | a line break |
| z    | sheets  | a form feed  |

Any text editor opens a book, and the [mtsv](https://github.com/demos-ra/mtsv)
library converts it to and from Excel, ODS, CSV, JSON, SQLite, Parquet and
Arrow. Every sheet is a relation in normal form: each row begins with its key,
each cell holds one value, and no two rows are alike (Codd, 1970). Where a
schema names the categories of what is kept, each category is a column; what
no schema names is kept in `_instances`, one row per value, by its place in
the event.

## Install

Void OS is one product in two implementations that behave the same.

```
pipx install void-os             # Python 3.11 or later
npm install --global void-os     # Node 22.13 or later
```

Each installs one command, `void-os`:

| Command                                           | Starts                                          |
|---------------------------------------------------|-------------------------------------------------|
| `void-os`                                         | the MCP server, over the standard streams        |
| `void-os <hook-event>`                            | the hook of that event, for example `SessionStart` |
| `void-os view [--filter filter] [input [day [position]]]` | the view, on your terminal              |

Any other operands print the usage message and end with exit status 1. No
command ends with exit status 2, which would block a harness.

## Setup

Void OS becomes your agents' operating system when their harness runs it in
two places. Any harness can; give these three steps to your agent and it can
wire them in itself, with your permission.

1. **Serve the tool.** Register an MCP server whose command is `void-os`,
   with no arguments, over standard input and output.
2. **Run the hooks.** On each of these six events, run `void-os` with the
   event's name as its one argument, and the event's JSON on standard input.
   Use the names your harness uses where it is one of these; otherwise the
   first column's:

   | Event                  | Claude Code, Codex, any other | Cursor               |
   |------------------------|-------------------------------|----------------------|
   | a session starts       | `SessionStart`                | `sessionStart`       |
   | a subagent starts      | `SubagentStart`               | `subagentStart`      |
   | a prompt is submitted  | `UserPromptSubmit`            | `beforeSubmitPrompt` |
   | a tool call succeeds   | `PostToolUse`                 | `postToolUse`        |
   | a subagent finishes    | `SubagentStop`                | `subagentStop`       |
   | the model finishes     | `Stop`                        | `stop`               |
3. **Work in your folders.** Run each hook in the folder your agent works in.
   Void OS takes the folder from the harness where it reports one, and from
   the working directory otherwise; nothing else is configured.

Every event is kept. Claude Code, Codex and Cursor also get context back on
their hook output: at the start of a session, what the data bank holds and
what is new; on later events, a prompt or, in Cursor, a tool call, what is
new since.

## How it works

Void OS is five modules. Each hides one design decision behind its interface
(Parnas, 1972), and each depends only on the modules before it.

### 1. Relational model: the grid itself

What a datum is: a relation, written as MTSV text and read back, and operated
on by the relational algebra.

* **Format.** MTSV is written and parsed exactly as the Internet-Draft
  specifies. JSON appears only at the edges, where each JSON text becomes the
  relations of its instances.
* **Query.** A reader names what it wants by position, as `2`, `1;3`, `1-3` or
  `2-*`, counted from 1, or by a filter expression. Selection restricts rows,
  projects columns, joins sheets on shared columns, and unites a sheet across
  files. With the data bank's `new`, which gives what is new, the set is
  relationally complete.

### 2. Data bank: write

Where relations are kept and how they are given back. Writing is converting:
JSON in, relations in normal form out.

* **Converter.** The JSON values a harness sends, and the JSON Schema
  (draft-07) that describes them, become relations in normal form, written as
  one MTSV book per input: a sheet for each kind of thing, a sheet of
  instances for values of no fixed shape, and a sheet of runs for text that
  holds a tab, a line break or a form feed.
* **Storage.** Each input is kept in its own book at the path of its folder,
  as [the structure](#the-structure) shows, in the data bank: the folder
  `~/Documents/void-os/` or the folder the variable `VOID_OS_DATA_BANK` names.
  Beside the books, the data bank keeps its own catalog: `_sheets` and
  `_fields`, what each book holds; `_stored`, when each value was kept; and
  `_communicated`, what each session and agent has been given. Values are
  inserted whole and only ever added: no row is changed or erased.
* **Communication.** The data bank gives the names of what it holds, any
  records by their keys, and what is new to a given session and agent.

### 3. Tools: read and query

The MCP server and the one tool it offers, `read`.

* **Input.** An absolute pathname: a file, a directory, whose regular files
  are read in the order of their names, or the data bank itself.
* **Conversion.** Excel, ODS, CSV, JSON and SQLite are read as sheets, and
  anything a conversion cannot carry is reported, never dropped silently.
* **Reply.** Every reply is MTSV: first the report of what was read, not read
  and left behind, then the map of each sheet's columns, or, with a
  selection of sheets, rows, columns, a filter or a join, the values chosen.

### 4. Hooks: the harness's way in

How a harness's events reach the data bank, and what they give back.

* **Hook input.** On each event, what the harness sends is inserted into the
  book of the folder the hook runs for, as step 3 of [setup](#setup) says.
* **Hook output.** At the start of a session the hook gives the harness, as
  context, the data bank's names and then what is new to that session and
  agent; on later events, such as each prompt, what is new. Each value comes
  with its record of when it was kept, and the context is cut to the most
  recent whole values within the context limit.

### 5. View: for people

How a person sees the whole data bank: overview first, zoom and filter, then
details on demand.

* **Overview:** each input, its values, and its days.
* **Zoom:** one input's days, then the turns of a day.
* **Filter:** the rows a level keeps, by the filter the query part gives.
* **Details:** one value in full, every row of every sheet it gives.
* **Terminal:** laid out for a terminal, through your pager; written as MTSV
  when the output is piped.

## What is in this repository

| Path                                                            | Contents                                                        |
|-----------------------------------------------------------------|-----------------------------------------------------------------|
| [`spec/`](spec/)                                                | the specification, as MTSV: modules, requirements and sources   |
| [`conformance/`](conformance/)                                  | the conformance cases, one per requirement                      |
| [`python/`](python/)                                            | the Python implementation                                       |
| [`javascript/`](javascript/)                                    | the JavaScript implementation                                   |
| [`tests/`](tests/)                                              | the test runner and its drivers, and the programs that derive the release files from the specification |
| `.spec.mtsv`, `.templates.mtsv`, `.mapping.mtsv`, `.canon.mtsv` | how the code is generated from the specification                |

Both implementations are generated from the one specification and pass the
same conformance cases. Conformance is the same for every language, so it sits
beside the language folders rather than inside one.

## Conformance

The test runner runs every case against both implementations: 257 cases, 514
runs. From the repository, with each implementation's dependencies installed:

```
python3 tests/system-generation/runner/run.py --repository .
```

In 0.1.0, 458 of the 514 runs pass. The rest are known, each with its cause:

* 44 runs check the test runner the current one replaced, and leave with the
  next revision of the specification.
* 6 runs expect the MIT License, which the specification held as a
  placeholder; Void OS is released under Apache-2.0.
* 2 runs, in JavaScript, expect an answer to `server/discover`, the
  2026-07-28 revision of MCP. The MCP TypeScript SDK serves that revision over
  HTTP only, so the JavaScript server speaks the 2025 handshake: clients that
  support both connect, falling back to `initialize`.
* 4 runs wait on two questions the specification will settle: how a test
  hands the code a table that holds a tab, and how files of one directory
  holding sheets of one name are given.

## Performance benchmark

To come.

## Version

0.1.0. Versions follow [Semantic Versioning](https://semver.org); each
release is tagged `vX.Y.Z` and published on
[PyPI](https://pypi.org/project/void-os/), on
[npm](https://www.npmjs.com/package/void-os) and in the
[MCP registry](https://registry.modelcontextprotocol.io) as
`io.github.demos-ra/void-os`.

## Help

Ask a question or report a problem in the
[issue tracker](https://github.com/demos-ra/void-os/issues). Void OS is
maintained by Demos Ra.

## License

[Apache-2.0](LICENSE). See [NOTICE](NOTICE).
