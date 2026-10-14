"""what a pathname names: a file, a directory of files, or the data bank"""
__all__ = ['members', 'RefusedError']
import os
from typing import Any

def members(pathname: str) -> tuple[dict[str, Any,], dict[str, Any,],]:
    if not pathname.startswith('/'):
        raise RefusedError('not absolute')
    read_input_3_is_a_directory = os.path.isdir(pathname)
    read_input_3_is_a_regular_file = os.path.isfile(pathname)
    if read_input_3_is_a_regular_file:
        try:
            with open(pathname, 'rb') as file:
                read_input_3_read_a_file = file.read()
        except OSError:
            raise RefusedError('cannot be read')
        read_input_4_resolve_pathname = os.path.realpath(pathname, strict=True)
        return {'sheet name': 'file', 'header': ['file', 'source'], 'records': [['1', read_input_4_resolve_pathname]]}, {'sheet name': 'not read', 'header': ['file', 'status', 'reason'], 'records': []},
    if not read_input_3_is_a_directory:
        raise RefusedError('names neither a directory nor a regular file')
    try:
        read_input_2_list_directory = os.listdir(bytes(pathname, 'utf-8'))
    except OSError:
        raise RefusedError('cannot be listed')
    place = pathname if pathname.endswith('/') else pathname + '/'
    found = []
    left = []
    for name in sorted(read_input_2_list_directory):
        input_1_utf_8_decode = str(name, 'utf-8')
        if not input_1_utf_8_decode.startswith('.'):
            read_input_2_is_a_regular_file = os.path.isfile(place + input_1_utf_8_decode)
            read_input_2_is_a_directory = os.path.isdir(place + input_1_utf_8_decode)
            if read_input_2_is_a_regular_file:
                read_input_4_resolve_pathname = os.path.realpath(place + input_1_utf_8_decode, strict=True)
                if read_input_4_resolve_pathname not in [record[1] for record in found]:
                    found.append([str(len(found) + 1), read_input_4_resolve_pathname])
            elif not read_input_2_is_a_directory:
                found.append([str(len(found) + 1), place + input_1_utf_8_decode])
                left.append([str(len(found)), 'skipped', ''])
    return {'sheet name': 'file', 'header': ['file', 'source'], 'records': found}, {'sheet name': 'not read', 'header': ['file', 'status', 'reason'], 'records': left},

class RefusedError(Exception):
    """A pathname that names neither a directory nor a regular file, a directory that cannot be listed, and a file named directly that cannot be read MUST be refused with the reason: names neither a directory nor a regular file, cannot be listed, or cannot be read.

A pathname that is not absolute MUST be refused as not absolute."""
