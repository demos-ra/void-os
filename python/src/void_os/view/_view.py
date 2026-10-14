"""how a person sees the whole data bank: overview first, zoom and filter, then details on demand"""
__all__ = ['view', 'KeepingFailedError', 'RefusedError']
import types
from typing import Any
from void_os.view.details import _details
from void_os.view.filter import _filter
from void_os.view.overview import _overview
from void_os.view.terminal import _terminal
from void_os.view.zoom import _zoom

def view(values: dict[str, Any,], operands: list[str], is_a_terminal: bool, offset: int | float, relational_model: types.ModuleType, data_bank: types.ModuleType) -> None:
    chosen = operands
    filters = []
    if len(chosen) >= 2 and chosen[0] == '--filter':
        filters = [chosen[1]]
        chosen = chosen[2:]
    if len(chosen) > 3:
        raise RefusedError('too many operands')
    try:
        inputs = [relation for relation in data_bank.names(values, relational_model) if relation['sheet name'] == '_inputs'][0]
        if len(chosen) == 0:
            every = [_zoom.days(values, record[0], offset, relational_model, data_bank) for record in inputs['records']]
            level = [_overview.overview(inputs, {'sheet name': 'days', 'header': ['input', 'day', 'event', 'values'], 'records': [record for relation in every for record in relation['records']]})]
        if len(chosen) >= 1:
            if chosen[0] not in [record[0] for record in inputs['records']]:
                raise RefusedError('no input ' + chosen[0])
            level = [_zoom.days(values, chosen[0], offset, relational_model, data_bank)]
        if len(chosen) >= 2:
            if chosen[1] not in [record[1] for record in level[0]['records']]:
                raise RefusedError('no day ' + chosen[1])
            level = [_zoom.turns(values, chosen[0], chosen[1], offset, relational_model, data_bank)]
        if len(chosen) == 3:
            if chosen[2] not in [record[1] for record in level[0]['records']]:
                raise RefusedError('no position ' + chosen[2])
            level = _details.details(values, chosen[0], int(chosen[2]), relational_model, data_bank)
        for query in filters:
            level = _filter.kept(level, query, relational_model)
    except data_bank.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _zoom.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _details.KeepingFailedError as error:
        raise KeepingFailedError(str(error))
    except _filter.RefusedError as error:
        raise RefusedError(str(error))
    text = _terminal.lay_out(values, level, is_a_terminal, relational_model)
    if is_a_terminal:
        _terminal.page(values, text, relational_model)
    if not is_a_terminal:
        _terminal.write(text, relational_model)

class KeepingFailedError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""

class RefusedError(Exception):
    """An input, day or position that does not exist MUST be refused with the reason no input, no day or no position, a space, and the operand.

More than three operands MUST be refused as too many operands."""
