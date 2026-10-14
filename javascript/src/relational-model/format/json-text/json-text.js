export function instances(octets) {
    try {
        const jsonText1UTF8Decode = new TextDecoder('utf-8', { fatal: true, ignoreBOM: true }).decode(octets);
        return read(jsonText1UTF8Decode);
    }
    catch (error) {
        if (error instanceof TypeError) {
            throw new NotAJSONTextError('not a JSON text: not UTF-8');
        }
        throw error;
    }
}
export function named(instances, pointer) {
    return jsonPointer(instances, pointer);
}
export class NamesNotUniqueError extends Error {}
export class NotAJSONTextError extends Error {}
const fragment = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~!$&'()*+,;=:@/?";
function jsonPointer(instances, pointer) {
    const records = instances.records;
    let named = records.slice(0, 1);
    if (pointer !== '' && !pointer.startsWith('/')) {
        named = [];
    }
    for (const token of pointer.split('/').slice(1)) {
        named = records.filter((record) => named.length > 0 && record[1] === named[0][0] && record[2] === '/' + token);
    }
    return { 'sheet name': 'instances', header: instances.header, records: named };
}
function percentEncoding(text) {
    return [...text].map((character) => fragment.includes(character) ? character : [...new TextEncoder().encode(character)].map((octet) => '%' + octet.toString(16).toUpperCase().padStart(2, '0')).join('')).join('');
}
function read(text) {
    let position = 0;
    const instances = [];
    const runs = [];
    const notCarried = [];
    const objects = [];
    function jsonText() {
        ws();
        value('', '', '');
        ws();
        if (position < text.length) {
            refused();
        }
    }
    function beginArray() {
        ws();
        literal('[');
        ws();
    }
    function beginObject() {
        ws();
        literal('{');
        ws();
    }
    function endArray() {
        ws();
        literal(']');
        ws();
    }
    function endObject() {
        ws();
        literal('}');
        ws();
    }
    function nameSeparator() {
        ws();
        literal(':');
        ws();
    }
    function valueSeparator() {
        ws();
        literal(',');
        ws();
    }
    function ws() {
        while (position < text.length && ' \t\n\r'.includes(text[position])) {
            position = position + 1;
        }
    }
    function value(parent, pointer, place) {
        const record = [String(instances.length), parent, pointer, '', ''];
        instances.push(record);
        if (text.startsWith('f', position)) {
            record[3] = 'boolean';
            record[4] = false_();
        }
        else {
            if (text.startsWith('n', position)) {
                record[3] = 'null';
                null_();
            }
            else {
                if (text.startsWith('t', position)) {
                    record[3] = 'boolean';
                    record[4] = true_();
                }
                else {
                    if (text.startsWith('{', position)) {
                        record[3] = 'object';
                        object(record[0], place);
                    }
                    else {
                        if (text.startsWith('[', position)) {
                            record[3] = 'array';
                            array(record[0], place);
                        }
                        else {
                            if (text.startsWith('"', position)) {
                                record[3] = 'string';
                                record[4] = carried(string(), record[0], place);
                            }
                            else {
                                record[3] = 'number';
                                record[4] = number();
                            }
                        }
                    }
                }
            }
        }
    }
    function false_() {
        literal('false');
        return 'false';
    }
    function null_() {
        literal('null');
    }
    function true_() {
        literal('true');
        return 'true';
    }
    function object(instance, place) {
        beginObject();
        const names = [];
        objects.push([place, names]);
        if (!text.startsWith('}', position)) {
            member(instance, place, names);
            ws();
            while (text.startsWith(',', position)) {
                valueSeparator();
                member(instance, place, names);
                ws();
            }
        }
        endObject();
    }
    function member(instance, place, names) {
        const name = string();
        nameSeparator();
        names.push(name);
        const token = referenceToken(name);
        if (token !== name.replaceAll('~', '~0').replaceAll('/', '~1')) {
            notCarried.push(place + '/' + token);
        }
        value(instance, '/' + token, place + '/' + token);
    }
    function array(instance, place) {
        beginArray();
        let index = 0;
        if (!text.startsWith(']', position)) {
            value(instance, '/0', place + '/0');
            ws();
            while (text.startsWith(',', position)) {
                valueSeparator();
                index = index + 1;
                value(instance, '/' + String(index), place + '/' + String(index));
                ws();
            }
        }
        endArray();
    }
    function number() {
        const start = position;
        if (text.startsWith('-', position)) {
            minus();
        }
        int();
        if (text.startsWith('.', position)) {
            frac();
        }
        if (text.startsWith('e', position) || text.startsWith('E', position)) {
            exp();
        }
        return text.slice(start, position);
    }
    function decimalPoint() {
        literal('.');
    }
    function digit19() {
        if (position === text.length || !'123456789'.includes(text[position])) {
            refused();
        }
        position = position + 1;
    }
    function e() {
        if (position === text.length || !'eE'.includes(text[position])) {
            refused();
        }
        position = position + 1;
    }
    function exp() {
        e();
        if (text.startsWith('-', position)) {
            minus();
        }
        else {
            if (text.startsWith('+', position)) {
                plus();
            }
        }
        digits(1);
    }
    function frac() {
        decimalPoint();
        digits(1);
    }
    function int() {
        if (text.startsWith('0', position)) {
            zero();
        }
        else {
            digit19();
            digits(0);
        }
    }
    function minus() {
        literal('-');
    }
    function plus() {
        literal('+');
    }
    function zero() {
        literal('0');
    }
    function string() {
        quotationMark();
        const characters = [];
        while (!text.startsWith('"', position)) {
            characters.push(char());
        }
        quotationMark();
        return characters.join('');
    }
    function char() {
        if (!text.startsWith('\\', position)) {
            return unescaped();
        }
        escape();
        const character = text.slice(position, position + 1);
        position = position + 1;
        if (character === 'u') {
            return String.fromCharCode(hexadecimal(4));
        }
        if (character === '' || !'"\\/bfnrt'.includes(character)) {
            refused();
        }
        return '"\\/\b\f\n\r\t'['"\\/bfnrt'.indexOf(character)];
    }
    function escape() {
        literal('\\');
    }
    function quotationMark() {
        literal('"');
    }
    function unescaped() {
        if (position === text.length || text[position] < ' ' || '"\\'.includes(text[position])) {
            refused();
        }
        position = position + 1;
        return text[position - 1];
    }
    function literal(word) {
        if (!text.startsWith(word, position)) {
            refused();
        }
        position = position + word.length;
    }
    function digits(least) {
        const start = position;
        while (position < text.length && '0123456789'.includes(text[position])) {
            position = position + 1;
        }
        if (position - start < least) {
            refused();
        }
    }
    function hexadecimal(count) {
        const hexdig = text.slice(position, position + count);
        if (hexdig.length < count || ![...hexdig].every((character) => '0123456789abcdefABCDEF'.includes(character))) {
            refused();
        }
        position = position + count;
        let code = 0;
        for (const character of hexdig.toLowerCase()) {
            code = code * 16 + '0123456789abcdef'.indexOf(character);
        }
        return code;
    }
    function carried(characters, instance, place) {
        const kept = characters.replace(/\p{Cs}|\r(?!\n)/gu, '');
        if (kept.length < characters.length) {
            notCarried.push(place);
        }
        if (!kept.includes('\f') && !kept.includes('\n') && !kept.includes('\t')) {
            return kept;
        }
        for (const [pageNumber, page] of kept.split('\f').entries()) {
            for (const [lineNumber, line] of page.replaceAll('\r\n', '\n').split('\n').entries()) {
                for (const [runNumber, run] of line.split('\t').entries()) {
                    runs.push([instance, String(pageNumber), String(lineNumber), String(runNumber), run]);
                }
            }
        }
        return '';
    }
    function refused() {
        throw new NotAJSONTextError('not a JSON text: at character ' + String(position + 1));
    }
    jsonText();
    for (const [place, names] of objects) {
        for (const [index, name] of names.entries()) {
            if (names.slice(0, index).includes(name)) {
                throw new NamesNotUniqueError('#' + percentEncoding(place));
            }
        }
    }
    return [{ 'sheet name': 'instances', header: ['_instance', '_parent', '_pointer', '_type', '_value'], records: instances }, { 'sheet name': 'runs', header: ['_instance', '_page', '_line', '_position', '_value'], records: runs }, notCarried];
}
function referenceToken(name) {
    const token = name.replaceAll('~', '~0').replaceAll('/', '~1');
    return token.replace(/[\t\n\f\r]|\p{Cs}/gu, '');
}
