export function union(sheets, origins, file, lead) {
    const files = Object.fromEntries(origins.records.map((record) => [record[0], record[1]]));
    const sources = Object.fromEntries(file.records.map((record) => [record[0], record[1]]));
    const united = [];
    for (const [index, sheet] of sheets.entries()) {
        const led = lead === 'file' ? files[String(index + 1)] : sources[files[String(index + 1)]];
        const header = sheet.header === null ? null : [lead, ...sheet.header];
        let found = united.find((each) => each['sheet name'] === sheet['sheet name'] && JSON.stringify(each.header) === JSON.stringify(header));
        if (found === undefined) {
            found = { 'sheet name': sheet['sheet name'], header: header, records: [] };
            united.push(found);
        }
        found.records.push(...sheet.records.map((record) => [led, ...record]));
    }
    return united;
}
