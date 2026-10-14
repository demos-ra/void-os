"""how a package's zip entries and XML parts are read as nodes"""
__all__ = ['nodes', 'CompressionMethodNotAllowedError', 'FailedError']
import zlib
from typing import Any
from xml.etree import ElementTree

def nodes(source: str) -> dict[str, Any,]:
    with open(source, 'rb') as file:
        octets = file.read()
    found = []
    for entry in _entries(octets):
        if entry['name'].endswith('.xml') or entry['name'].endswith('.rels'):
            if entry['method'] != 0 and entry['method'] != 8:
                raise CompressionMethodNotAllowedError('compression method not allowed')
            try:
                root = ElementTree.fromstring(_data(octets, entry))
            except ElementTree.ParseError:
                raise FailedError('failed')
            found.extend(_part(entry['name'], root))
    return {'sheet name': 'nodes', 'header': ['part', 'node', 'parent', 'kind', 'name', 'value'], 'records': found}

class CompressionMethodNotAllowedError(Exception):
    """A zip entry compressed otherwise MUST end the read of its package as compression method not allowed."""

class FailedError(Exception):
    """A package that is not a zip file, or an entry it reads as XML that is not well-formed, MUST end the read of its package as failed."""

def _data(octets: bytes, entry: dict[str, Any,]) -> bytes:
    start = entry['offset'] + 30 + int.from_bytes(octets[entry['offset'] + 26:entry['offset'] + 28], 'little') + int.from_bytes(octets[entry['offset'] + 28:entry['offset'] + 30], 'little')
    compressed = octets[start:start + entry['size']]
    if entry['method'] == 0:
        return compressed
    package_1_deflate_read = zlib.decompress(compressed, wbits=-15)
    return package_1_deflate_read

def _element(part: str, element: ElementTree.Element, parent: str, found: list[list[str]]) -> None:
    place = str(len(found))
    found.append([part, place, parent, 'element', element.tag, ''])
    for key, value, in element.attrib.items():
        found.append([part, str(len(found)), place, 'attribute', key, value])
    if element.text:
        found.append([part, str(len(found)), place, 'text', '', element.text])
    for child in element:
        _element(part, child, place, found)
        if child.tail:
            found.append([part, str(len(found)), place, 'text', '', child.tail])

def _entries(octets: bytes) -> list[dict[str, Any,]]:
    end = len(octets) - 22
    while end >= 0 and int.from_bytes(octets[end:end + 4], 'little') != 0x06054b50:
        end = end - 1
    if end < 0:
        raise FailedError('failed')
    found = []
    at = int.from_bytes(octets[end + 16:end + 20], 'little')
    while len(found) < int.from_bytes(octets[end + 10:end + 12], 'little'):
        if int.from_bytes(octets[at:at + 4], 'little') != 0x02014b50:
            raise FailedError('failed')
        length = int.from_bytes(octets[at + 28:at + 30], 'little')
        found.append({'name': str(octets[at + 46:at + 46 + length], 'utf-8', 'replace'), 'method': int.from_bytes(octets[at + 10:at + 12], 'little'), 'size': int.from_bytes(octets[at + 20:at + 24], 'little'), 'offset': int.from_bytes(octets[at + 42:at + 46], 'little')})
        at = at + 46 + length + int.from_bytes(octets[at + 30:at + 32], 'little') + int.from_bytes(octets[at + 32:at + 34], 'little')
    return found

def _part(part: str, root: ElementTree.Element) -> list[list[str]]:
    found = []
    _element(part, root, '', found)
    return found
