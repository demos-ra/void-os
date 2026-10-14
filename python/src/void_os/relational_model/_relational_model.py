"""what a datum is: a relation, written as text and read back, and operated on by the relational algebra"""
__all__ = ['chosen', 'dump', 'dumps', 'instances', 'kept', 'load', 'loads', 'named', 'CannotBeRepresentedError', 'NamesNotUniqueError', 'NotMTSVError', 'NotAJSONTextError', 'RefusedError']
from typing import Any
from void_os.relational_model.format import _format
from void_os.relational_model.query import _query

def chosen(sheets: list[dict[str, Any,]], origins: dict[str, Any,], file: dict[str, Any,], lead: str, sheet: str, records: str, fields: str, filter: str, join: str) -> tuple[list[dict[str, Any,]], dict[str, Any,],]:
    try:
        return _query.chosen(sheets, origins, file, lead, sheet, records, fields, filter, join)
    except _query.RefusedError as error:
        raise RefusedError(str(error))

def dump(sheets: list[dict[str, Any,]]) -> bytes:
    try:
        return _format.dump(sheets)
    except _format.CannotBeRepresentedError as error:
        raise CannotBeRepresentedError(str(error))

def dumps(sheets: list[dict[str, Any,]]) -> str:
    try:
        return _format.dumps(sheets)
    except _format.CannotBeRepresentedError as error:
        raise CannotBeRepresentedError(str(error))

def instances(octets: bytes) -> tuple[dict[str, Any,], dict[str, Any,], list[str],]:
    try:
        return _format.instances(octets)
    except _format.NamesNotUniqueError as error:
        raise NamesNotUniqueError(str(error))
    except _format.NotAJSONTextError as error:
        raise NotAJSONTextError(str(error))

def kept(sheets: list[dict[str, Any,]], filter: str) -> list[dict[str, Any,]]:
    try:
        return _query.kept(sheets, filter)
    except _query.RefusedError as error:
        raise RefusedError(str(error))

def load(octets: bytes) -> list[dict[str, Any,]]:
    try:
        return _format.load(octets)
    except _format.NotMTSVError as error:
        raise NotMTSVError(str(error))

def loads(text: str) -> list[dict[str, Any,]]:
    try:
        return _format.loads(text)
    except _format.NotMTSVError as error:
        raise NotMTSVError(str(error))

def named(instances: dict[str, Any,], pointer: str) -> dict[str, Any,]:
    return _format.named(instances, pointer)

class CannotBeRepresentedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NamesNotUniqueError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NotMTSVError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NotAJSONTextError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class RefusedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
