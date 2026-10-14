"""how a file of another format becomes sheets, and what it leaves behind"""
__all__ = ['sheets', 'FailedError', 'NoFormatError']
import types
from typing import Any
from void_os.tools.read.conversion.csv import _csv
from void_os.tools.read.conversion.json import _json
from void_os.tools.read.conversion.ods import _ods
from void_os.tools.read.conversion.package import _package
from void_os.tools.read.conversion.sqlite import _sqlite
from void_os.tools.read.conversion.xlsx import _xlsx

def sheets(source: str, relational_model: types.ModuleType) -> tuple[list[dict[str, Any,]], list[str],]:
    name = source[source.rfind('/') + 1:]
    extension = name[name.rfind('.') + 1:] if '.' in name else ''
    if extension not in ['mtsv', 'csv', 'json', 'xlsx', 'ods', 'sqlite']:
        raise NoFormatError('no format')
    try:
        if extension == 'sqlite':
            return _sqlite.load(source)
        if extension == 'xlsx':
            return _xlsx.load(_package.nodes(source))
        if extension == 'ods':
            return _ods.load(_package.nodes(source))
        try:
            with open(source, 'rb') as file:
                conversion_1_read_a_file = file.read()
        except OSError:
            raise FailedError('cannot be read')
        if extension == 'mtsv':
            return relational_model.load(conversion_1_read_a_file), [],
        if extension == 'csv':
            return _csv.load(conversion_1_read_a_file)
        return _json.load(conversion_1_read_a_file, relational_model)
    except _sqlite.CannotBeRepresentedError:
        raise FailedError('cannot be represented')
    except _sqlite.FailedError:
        raise FailedError('failed')
    except _package.FailedError:
        raise FailedError('failed')
    except _package.CompressionMethodNotAllowedError:
        raise FailedError('compression method not allowed')
    except _xlsx.CannotBeRepresentedError:
        raise FailedError('cannot be represented')
    except _xlsx.FailedError:
        raise FailedError('failed')
    except _ods.CannotBeRepresentedError:
        raise FailedError('cannot be represented')
    except _ods.FailedError:
        raise FailedError('failed')
    except relational_model.NotMTSVError:
        raise FailedError('not MTSV')
    except _csv.CannotBeRepresentedError:
        raise FailedError('cannot be represented')
    except _json.CannotBeRepresentedError:
        raise FailedError('cannot be represented')
    except _json.NotAJSONTextError:
        raise FailedError('not a JSON text')
    except _json.NamesNotUniqueError:
        raise FailedError('names not unique')

class FailedError(Exception):
    """A file whose extension names no format MUST end its conversion as no format; one that cannot be read, as failed, its reason cannot be read; and one whose conversion ends with an error, as failed, its reason that error's name."""

class NoFormatError(Exception):
    """A file whose extension names no format MUST end its conversion as no format; one that cannot be read, as failed, its reason cannot be read; and one whose conversion ends with an error, as failed, its reason that error's name."""
