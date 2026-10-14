"""what the whole data bank holds: each input, its values, and its days"""
__all__ = ['overview']
import datetime
from typing import Any

def overview(names: dict[str, Any,], days: dict[str, Any,]) -> dict[str, Any,]:
    found = []
    for name in names['records']:
        totals = {}
        for record in days['records']:
            if record[0] == name[0]:
                totals[record[1]] = totals.get(record[1], 0) + int(record[3])
        first = ''
        last = ''
        activity = ''
        if totals:
            dates = sorted(totals)
            first = dates[0]
            last = dates[len(dates) - 1]
            overview_2_max = max(totals.values(), default=0)
            day = datetime.date.fromisoformat(first)
            while day <= datetime.date.fromisoformat(last):
                count = totals.get(day.isoformat(), 0)
                activity = activity + (chr(9600 + (8 * count + overview_2_max - 1) // overview_2_max) if count > 0 else ' ')
                day = day + datetime.timedelta(days=1)
        found.append([name[0], name[1], first, last, activity])
    return {'sheet name': 'overview', 'header': ['input', 'values', 'first', 'last', 'activity'], 'records': found}
