"""how the relations are written as MTSV, at its levels"""
__all__ = ['sheets', 'write']
import types
from typing import Any
from void_os.data_bank.converter.output.field import _field
from void_os.data_bank.converter.output.file import _file
from void_os.data_bank.converter.output.record import _record
from void_os.data_bank.converter.output.sheet import _sheet

def sheets(layout: list[dict[str, Any,]], relational_model: types.ModuleType) -> list[dict[str, Any,]]:
    return _sheet.sheets(layout)

def write(transferred: list[dict[str, Any,]], input: list[dict[str, Any,]], relational_model: types.ModuleType) -> str:
    fields = _field.fields(transferred[5], input)
    texts = {cell[0] + '\n' + cell[1] + '\n' + cell[4] + '\n' + cell[3]: text[4] for cell, text, in zip(transferred[5]['records'], fields[0]['records'])}
    held = _record.records([transferred[4], transferred[5], transferred[6], transferred[7]])
    sheets = _sheet.sheets([transferred[0], transferred[1], transferred[2], transferred[3], transferred[7]])
    for index, relation, in enumerate(held):
        count = 4 if relation['header'][1:2] == ['_instance'] else 1
        sheets[index]['records'] = [row[:count] + [texts.get(relation['sheet name'] + '\n' + row[0] + '\n' + value + '\n' + column, '') for value, column, in zip(row[count:], relation['header'][count:])] for row in relation['records']]
    for named in sheets[len(held):]:
        named['records'] = fields[1]['records']
    return relational_model.dumps(_file.file(sheets))
