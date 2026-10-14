"""which sheets the whole input's one MTSV file holds, and in which order"""
__all__ = ['file']
from typing import Any

def file(sheets: list[dict[str, Any,]]) -> list[dict[str, Any,]]:
    return [sheet for sheet in sheets if sheet['records']]
