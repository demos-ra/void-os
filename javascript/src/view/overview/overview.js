export function overview(names, days) {
    const found = [];
    for (const name of names.records) {
        const totals = new Map();
        for (const record of days.records) {
            if (record[0] === name[0]) {
                totals.set(record[1], (totals.get(record[1]) ?? 0) + Number(record[3]));
            }
        }
        let first = '';
        let last = '';
        let activity = '';
        if (totals.size > 0) {
            const dates = [...totals.keys()].sort();
            first = dates[0];
            last = dates[dates.length - 1];
            const overview2Max = Math.max(0, ...totals.values());
            let moment = Date.parse(first);
            while (moment <= Date.parse(last)) {
                const count = totals.get(new Date(moment).toISOString().slice(0, 10)) ?? 0;
                activity = activity + (count > 0 ? String.fromCodePoint(9600 + Math.ceil(8 * count / overview2Max)) : ' ');
                moment = moment + 86400000;
            }
        }
        found.push([name[0], name[1], first, last, activity]);
    }
    return { 'sheet name': 'overview', header: ['input', 'values', 'first', 'last', 'activity'], records: found };
}
