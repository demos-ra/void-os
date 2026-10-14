"""how a database becomes sheets"""
__all__ = ['load', 'CannotBeRepresentedError', 'FailedError']
import sqlite3
from typing import Any

def load(source: str) -> tuple[list[dict[str, Any,]], list[str],]:
    sqlite_1_sqlite_uri = source.replace('?', '%3f')
    sqlite_1_sqlite_uri = sqlite_1_sqlite_uri.replace('#', '%23')
    while '//' in sqlite_1_sqlite_uri:
        sqlite_1_sqlite_uri = sqlite_1_sqlite_uri.replace('//', '/')
    sqlite_1_sqlite_uri = 'file:' + sqlite_1_sqlite_uri
    try:
        sqlite_1_open_database = sqlite3.connect(sqlite_1_sqlite_uri + '?mode=ro', uri=True)
        try:
            return _loaded(sqlite_1_open_database)
        finally:
            sqlite_1_open_database.close()
    except sqlite3.DatabaseError:
        raise FailedError('failed')

class CannotBeRepresentedError(Exception):
    """A value whose typeof is blob, or a field that MTSV cannot hold, or a sheet name holding HT, LF, FF or CR, MUST end the load as cannot be represented."""

class FailedError(Exception):
    """A file that does not begin with the database header's magic string MUST end the load as failed."""

def _loaded(connection: sqlite3.Connection) -> tuple[list[dict[str, Any,]], list[str],]:
    sqlite_1_query = [list(row) for row in connection.execute('SELECT type, name FROM sqlite_schema').fetchall()]
    return [_sheet(connection, name) for kind, name, in sqlite_1_query if kind == 'table' and not name.startswith('sqlite_')], [kind + ' ' + name for kind, name, in sqlite_1_query if kind != 'table' or name.startswith('sqlite_')],

def _quoted(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'

def _record(row: list[Any]) -> list[str]:
    if 'blob' in row[::2]:
        raise CannotBeRepresentedError('cannot be represented')
    return [_text(text or '') for text in row[1::2]]

def _selected(index: int, column: str) -> str:
    return 'typeof(' + _quoted(column) + ') AS "t' + str(index) + '", CAST(' + _quoted(column) + ' AS TEXT) AS "v' + str(index) + '"'

def _sheet(connection: sqlite3.Connection, name: str) -> dict[str, Any,]:
    sqlite_1_query = [list(row) for row in connection.execute("SELECT name FROM pragma_table_info('" + name.replace("'", "''") + "')").fetchall()]
    header = [row[0] for row in sqlite_1_query]
    query = 'SELECT ' + ', '.join((_selected(index, column) for index, column, in enumerate(header))) + ' FROM ' + _quoted(name)
    sqlite_2_query = [list(row) for row in connection.execute(query).fetchall()]
    return {'sheet name': _text(name), 'header': [_text(column) for column in header], 'records': [_record(row) for row in sqlite_2_query]}

def _text(text: str) -> str:
    if any((character in text for character in '\t\n\f\r')):
        raise CannotBeRepresentedError('cannot be represented')
    return text
