"""how each input value is read as a JSON text, and when it is rejected"""
__all__ = ['values', 'NonConformingError']
import types
from typing import Any

def values(input_values: list[bytes], start: int | float, relational_model: types.ModuleType) -> tuple[list[dict[str, Any,]], list[str],]:
    instances = {'sheet name': '_instances', 'header': ['_input value', '_instance', '_parent', '_pointer', '_type', '_value'], 'records': []}
    runs = {'sheet name': '_runs', 'header': ['_input value', '_instance', '_page', '_line', '_position', '_value'], 'records': []}
    not_carried = []
    for index, octets, in enumerate(input_values):
        position = str(start + index)
        try:
            found = relational_model.instances(octets)
        except relational_model.NotAJSONTextError as error:
            raise NonConformingError(position + ' ' + '#')
        except relational_model.NamesNotUniqueError as error:
            raise NonConformingError(position + ' ' + str(error))
        instances['records'].extend(([position] + record for record in found[0]['records']))
        runs['records'].extend(([position] + record for record in found[1]['records']))
        not_carried.extend(('/' + position + pointer for pointer in found[2]))
    return [instances, runs], not_carried,

class NonConformingError(Exception):
    """An input value JSON text rejects, as not a JSON text or as names not unique, MUST be rejected as non-conforming, its reason its zero-based position in the input, a space, and the JSON Pointer to the place within it, in its URI fragment representation: the first object, in the order written, that repeats a name, or else the value itself."""
