import * as field from './field/field.js';
import * as file from './file/file.js';
import * as record from './record/record.js';
import * as sheet from './sheet/sheet.js';
export function sheets(layout, relationalModel) {
    return sheet.sheets(layout);
}
export function write(transferred, input, relationalModel) {
    const fields = field.fields(transferred[5], input);
    const texts = new Map(transferred[5].records.map((cell, index) => [cell[0] + '\n' + cell[1] + '\n' + cell[4] + '\n' + cell[3], fields[0].records[index][4]]));
    const held = record.records([transferred[4], transferred[5], transferred[6], transferred[7]]);
    const sheets = sheet.sheets([transferred[0], transferred[1], transferred[2], transferred[3], transferred[7]]);
    for (const [index, relation] of held.entries()) {
        const count = relation.header[1] === '_instance' ? 4 : 1;
        sheets[index].records = relation.records.map((row) => row.slice(0, count).concat(row.slice(count).map((value, position) => texts.get(relation['sheet name'] + '\n' + row[0] + '\n' + value + '\n' + relation.header[count + position]) ?? '')));
    }
    for (const named of sheets.slice(held.length)) {
        named.records = fields[1].records;
    }
    return relationalModel.dumps(file.file(sheets));
}
