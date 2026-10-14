"""what the data bank gives: names, records by their keys, and what is new"""
__all__ = ['names', 'new', 'records', 'KeepingFailedError']
import types
from typing import Any

def names(values: dict[str, Any,], relational_model: types.ModuleType, converter: types.ModuleType, storage: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return [storage.inputs(values, relational_model, converter)] + storage.names(values, relational_model, converter)
    except storage.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

def new(values: dict[str, Any,], input_name: str, session: str, agent: str, places: list[str], relational_model: types.ModuleType, converter: types.ModuleType, storage: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        first = storage.communicated(values, input_name, session, agent, relational_model, converter)
        last = _count(values, input_name, relational_model, converter, storage) - 1
        found = _given(values, input_name, first, last, places, relational_model, converter, storage)
        storage.mark_communicated(values, input_name, session, agent, last + 1, relational_model, converter)
        return found + [storage.stored(values, input_name, first, last, relational_model, converter)]
    except storage.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

def records(values: dict[str, Any,], input_name: str, first: int | float, last: int | float, places: list[str], relational_model: types.ModuleType, converter: types.ModuleType, storage: types.ModuleType) -> list[dict[str, Any,]]:
    try:
        return _given(values, input_name, first, last, places, relational_model, converter, storage)
    except storage.KeepingFailedError as error:
        raise KeepingFailedError(str(error))

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

def _count(values: dict[str, Any,], input_name: str, relational_model: types.ModuleType, converter: types.ModuleType, storage: types.ModuleType) -> int:
    return next((int(record[1]) for record in storage.inputs(values, relational_model, converter)['records'] if record[0] == input_name), 0)

def _given(values: dict[str, Any,], input_name: str, first: int | float, last: int | float, places: list[str], relational_model: types.ModuleType, converter: types.ModuleType, storage: types.ModuleType) -> list[dict[str, Any,]]:
    named = storage.names(values, relational_model, converter)
    held = storage.relations(values, input_name, relational_model, converter)
    listed = [place for place in named[0]['records'] if place[0] == input_name]
    chosen = [place for place in listed if place[1] in places] if places else listed
    found = []
    for place in chosen:
        rows = [record for sheet in held if sheet['sheet name'] == place[2] for record in sheet['records'] if first <= int(record[0]) <= last]
        if rows:
            found.append({'sheet name': place[2], 'header': [field[3] for field in named[1]['records'] if field[0] == input_name and field[1] == place[1]], 'records': rows})
    return found
