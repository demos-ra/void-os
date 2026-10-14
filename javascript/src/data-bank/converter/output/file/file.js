export function file(sheets) {
    return sheets.filter((sheet) => sheet.records.length > 0);
}
