![VOID OS](banner.svg)

void-os
=======

**Memory is space. Time is CPU cycles.**

Void OS is the gate operating within the liminal space between unstructured
and structured data. It is your personal operating system for Artificial and
Super Intelligence agent infrastructure. It gives memory a shape: a 3D grid,
mapped on the x, y and z axes, of sheets, columns and rows. Relational mapping
in pure text is the native format for agents, enabling your agents to operate
at maximum productivity.

Databases have always been the way to store and manage data, and their shape
never changes: a book for each subject, a sheet for each kind of thing, a
column for each category, a row for each entry, and a cell for each value.
Each row is one fact, stated once, keyed to every fact it touches and to
where it came from, so the grid is not a log to search for what was said
but memory itself, a substrate any agent can reason across. That
three-dimensional grid powers the entirety of Void OS: your data, one shape
everywhere. You and your agents all read, write and query one grid.

Why It Is Useful
----------------

AI agents already work in folders, and void-os keeps everything they do by
the folder they work in, so it needs no schema, registry or configuration
of its own. Each folder's book is one Multi-Sheet Tab-Separated Values
(MTSV) file: any text editor opens it, and [mtsv](https://github.com/demos-ra/mtsv) converts it to and from
Excel (XLSX), ODS, CSV, JSON, SQLite, Parquet and Arrow. You and every agent
read, write and query the same data bank, through one Model Context Protocol
(MCP) server and its hooks.

Get Started
-----------

* Install: `pipx install void-os` (Python 3.11 or later) or `npm install --global void-os` (Node 22.13 or later)
* Serve the tool: register an MCP server whose command is `void-os`, with no arguments, over standard input and output
* Run the hooks: on each event, run `void-os` with the event's name as its one argument and the event's JSON on standard input: SessionStart, SubagentStart, UserPromptSubmit, PostToolUse, SubagentStop and Stop in Claude Code, Codex and any other harness; sessionStart, subagentStart, beforeSubmitPrompt, postToolUse, subagentStop and stop in Cursor
* Work in your folders: run each hook in the folder your agent works in; nothing else is configured
* See the data bank: `void-os view [--filter filter] [input [day [position]]]`, on your terminal

How It Works
------------

* Relational model: every sheet is a relation in normal form (Codd, 1970), written as MTSV; a reader names what it wants by position, as `2`, `1;3`, `1-3` or `2-*`, or by a filter, with restriction, projection, join and union
* Data bank: the JSON a harness sends, and the JSON Schema that describes it, become one book per input, kept at the path of its folder in `~/Documents/void-os/`, or the folder `VOID_OS_DATA_BANK` names; values are only ever added
* Tools: the MCP server's one tool, `read`: a file, a directory or the data bank, as MTSV, with Excel, ODS, CSV, JSON and SQLite converted and whatever a conversion cannot carry reported
* Hooks: every event is kept; Claude Code, Codex and Cursor get context back: at the start of a session, what the data bank holds and what is new, and on later events, what is new since
* View: overview first, then zoom and filter, then details on demand, in your terminal
* Modules: five, each hiding one design decision (Parnas, 1972) and using only the modules before it

Details
-------

* Specification: [spec/](spec/), as MTSV; the code of both implementations is generated from it with the same canon as [living-architecture](https://github.com/demos-ra/living-architecture)
* Format: [MTSV, an IETF Internet-Draft](https://github.com/demos-ra/mtsv-spec)
* Conformance: 257 cases run against both implementations, 514 runs; in 0.1.0, 458 pass, and the rest are known: 44 check the test runner the current one replaced, 6 expect the MIT License the specification held as a placeholder, 2, in JavaScript, expect an answer to server/discover from the 2026-07-28 revision of MCP, which the MCP TypeScript SDK serves over HTTP only, and 4 wait on two questions the specification will settle
* Requirements: Python 3.11 or later, or Node 22.13 or later
* Version: 0.1.0; each release tagged vX.Y.Z and published on [PyPI](https://pypi.org/project/void-os/), on [npm](https://www.npmjs.com/package/void-os) and in the [MCP registry](https://registry.modelcontextprotocol.io) as `io.github.demos-ra/void-os`; versions follow [Semantic Versioning](https://semver.org)
* Layout: [spec/](spec/), the specification; [conformance/](conformance/), one case per requirement; [python/](python/) and [javascript/](javascript/), the two implementations; [tests/](tests/), the test runner; .spec.mtsv, .templates.mtsv, .mapping.mtsv and .canon.mtsv, how the code is generated
* License: [Apache-2.0](LICENSE); see [NOTICE](NOTICE)

Get Help
--------

* Issues: [void-os issue tracker](https://github.com/demos-ra/void-os/issues)
* Maintainer: Demos Ra
* More: [all MTSV tools by Demos Ra](https://github.com/demos-ra)
