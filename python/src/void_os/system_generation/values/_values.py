"""where the Values are read from, and how values.mtsv is written"""
__all__ = ['values', 'NotMTSVError']
import os
import types
from typing import Any

def values(folder: str, relational_model: types.ModuleType) -> dict[str, Any,]:
    try:
        with open(os.path.join(folder, 'values.mtsv'), 'rb') as file:
            values_1_read_a_file = file.read()
        sheets = relational_model.load(values_1_read_a_file)
    except OSError:
        raise NotMTSVError('not MTSV')
    except relational_model.NotMTSVError as error:
        raise NotMTSVError(str(error))
    sheet = [relation for relation in sheets if relation['sheet name'] == 'Values'][0]
    header = sheet['header']
    return {'sheet name': 'Values', 'header': ['Value', 'Given'], 'records': [[record[header.index('Value')], record[header.index('Given')]] for record in sheet['records']]}

class NotMTSVError(Exception):
    """A values.mtsv that cannot be read, or that the parser rejects, MUST end values as not MTSV."""
