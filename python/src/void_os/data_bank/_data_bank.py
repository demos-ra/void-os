"""how relations are kept and given back: converted in from JSON, inserted, and communicated"""
__all__ = ['folder', 'insert', 'names', 'new', 'records', 'stored', 'KeepingFailedError', 'NonConformingError']
import types
from typing import Any
from void_os.data_bank.communication import _communication
from void_os.data_bank.converter import _converter
from void_os.data_bank.storage import _storage

def folder(values: dict[str, Any,], relational_model: types.ModuleType) -> str:
    return _storage.folder(values, relational_model, _converter)

def insert(values: dict[str, Any,], input_name: str, input_values: list[bytes], module_specification: bytes, event: str, relational_model: types.ModuleType) -> int | float:
    try:
        return _storage.insert(values, input_name, input_values, module_specification, event, relational_model, _converter)
    except _storage.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _storage.NonConformingError as error:
        raise NonConformingError(str(error))

def names(values: dict[str, Any,], relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return _communication.names(values, relational_model, _converter, _storage)
    except _communication.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

def new(values: dict[str, Any,], input_name: str, session: str, agent: str, places: list[str], relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return _communication.new(values, input_name, session, agent, places, relational_model, _converter, _storage)
    except _communication.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

def records(values: dict[str, Any,], input_name: str, first: int | float, last: int | float, places: list[str], relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return _communication.records(values, input_name, first, last, places, relational_model, _converter, _storage)
    except _communication.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

def stored(values: dict[str, Any,], input_name: str, first: int | float, last: int | float, relational_model: types.ModuleType) -> dict[str, Any,]:
    try:
        return _storage.stored(values, input_name, first, last, relational_model, _converter)
    except _storage.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class NonConformingError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
