"""how a relation is written as text and read back: MTSV, and JSON at void-os's edges"""
__all__ = ['dump', 'dumps', 'instances', 'load', 'loads', 'named', 'CannotBeRepresentedError', 'NamesNotUniqueError', 'NotMTSVError', 'NotAJSONTextError']
from typing import Any
from void_os.relational_model.format.generator import _generator
from void_os.relational_model.format.json_text import _json_text
from void_os.relational_model.format.parser import _parser

def dump(sheets: list[dict[str, Any,]]) -> bytes:
    try:
        return _generator.dump(sheets)
    except _generator.CannotBeRepresentedError as error:
        raise CannotBeRepresentedError(str(error))

def dumps(sheets: list[dict[str, Any,]]) -> str:
    try:
        return _generator.dumps(sheets)
    except _generator.CannotBeRepresentedError as error:
        raise CannotBeRepresentedError(str(error))

def instances(octets: bytes) -> tuple[dict[str, Any,], dict[str, Any,], list[str],]:
    try:
        return _json_text.instances(octets)
    except _json_text.NamesNotUniqueError as error:
        raise NamesNotUniqueError(str(error))
    except _json_text.NotAJSONTextError as error:
        raise NotAJSONTextError(str(error))

def load(octets: bytes) -> list[dict[str, Any,]]:
    try:
        return _parser.load(octets)
    except _parser.NotMTSVError as error:
        raise NotMTSVError(str(error))

def loads(text: str) -> list[dict[str, Any,]]:
    try:
        return _parser.loads(text)
    except _parser.NotMTSVError as error:
        raise NotMTSVError(str(error))

def named(instances: dict[str, Any,], pointer: str) -> dict[str, Any,]:
    return _json_text.named(instances, pointer)

class CannotBeRepresentedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NamesNotUniqueError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NotMTSVError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NotAJSONTextError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
