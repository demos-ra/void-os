"""the decisions postponed to release, and how void-os is built, described and installed"""
__all__ = ['values', 'NotMTSVError']
import os
import types
from typing import Any
from void_os.system_generation.values import _values

def values(relational_model: types.ModuleType) -> dict[str, Any,]:
    system_generation_1_module_folder = os.path.dirname(__file__)
    try:
        return _values.values(os.path.join(system_generation_1_module_folder, 'values'), relational_model)
    except _values.NotMTSVError as error:
        raise NotMTSVError(str(error))

class NotMTSVError(Exception):
    """An error that ends an access program a module calls MUST end the module's access as that error, by its name, unless Ended errors names a requirement that ends it otherwise or rules it out."""
