import * as fs from 'node:fs';
import * as zlib from 'node:zlib';
export function nodes(source) {
    const octets = fs.readFileSync(source);
    const found = [];
    for (const entry of entries(octets)) {
        if (entry.name.endsWith('.xml') || entry.name.endsWith('.rels')) {
            if (entry.method !== 0 && entry.method !== 8) {
                throw new CompressionMethodNotAllowedError('compression method not allowed');
            }
            found.push(...parsed(entry.name, new TextDecoder('utf-8', { fatal: true }).decode(data(octets, entry))));
        }
    }
    return { 'sheet name': 'nodes', header: ['part', 'node', 'parent', 'kind', 'name', 'value'], records: found };
}
export class CompressionMethodNotAllowedError extends Error {}
export class FailedError extends Error {}
function data(octets, entry) {
    const start = entry.offset + 30 + octets.readUInt16LE(entry.offset + 26) + octets.readUInt16LE(entry.offset + 28);
    const compressed = octets.subarray(start, start + entry.size);
    if (entry.method === 0) {
        return compressed;
    }
    const package1DEFLATERead = zlib.inflateRawSync(compressed);
    return package1DEFLATERead;
}
function decoded(raw) {
    let found = '';
    let at = 0;
    while (raw.indexOf('&', at) >= 0) {
        const ampersand = raw.indexOf('&', at);
        const semicolon = raw.indexOf(';', ampersand);
        if (semicolon < 0) {
            throw new FailedError('failed');
        }
        found = found + raw.slice(at, ampersand) + reference(raw.slice(ampersand + 1, semicolon));
        at = semicolon + 1;
    }
    return found + raw.slice(at);
}
function element(state, part, parent, scope, found) {
    state.at = state.at + 1;
    const tag = name(state);
    const attributes = [];
    space(state);
    while (!starts(state, '/>') && !starts(state, '>')) {
        const key = name(state);
        space(state);
        if (!starts(state, '=')) {
            throw new FailedError('failed');
        }
        state.at = state.at + 1;
        space(state);
        const quote = state.text[state.at];
        const close = state.text.indexOf(quote, state.at + 1);
        if (!'"\''.includes(quote) || close < 0) {
            throw new FailedError('failed');
        }
        attributes.push([key, decoded(state.text.slice(state.at + 1, close).replaceAll('\t', ' ').replaceAll('\n', ' '))]);
        state.at = close + 1;
        space(state);
    }
    const own = new Map(scope);
    for (const [key, value] of attributes) {
        if (key === 'xmlns') {
            own.set('', value);
        }
        else {
            if (key.startsWith('xmlns:')) {
                own.set(key.slice(6), value);
            }
        }
    }
    const place = String(found.length);
    found.push([part, place, parent, 'element', expanded(tag, own, true), '']);
    for (const [key, value] of attributes) {
        if (key !== 'xmlns' && !key.startsWith('xmlns:')) {
            found.push([part, String(found.length), place, 'attribute', expanded(key, own, false), value]);
        }
    }
    if (starts(state, '/>')) {
        state.at = state.at + 2;
        return;
    }
    state.at = state.at + 1;
    let text = '';
    while (!starts(state, '</')) {
        if (state.at >= state.text.length) {
            throw new FailedError('failed');
        }
        else {
            if (starts(state, '<!--')) {
                skip(state, '-->');
            }
            else {
                if (starts(state, '<![CDATA[')) {
                    text = text + skip(state, ']]>').slice(9);
                }
                else {
                    if (starts(state, '<?')) {
                        skip(state, '?>');
                    }
                    else {
                        if (starts(state, '<')) {
                            if (text !== '') {
                                found.push([part, String(found.length), place, 'text', '', text]);
                                text = '';
                            }
                            element(state, part, place, own, found);
                        }
                        else {
                            text = text + decoded(skip(state, '<'));
                            state.at = state.at - 1;
                        }
                    }
                }
            }
        }
    }
    if (text !== '') {
        found.push([part, String(found.length), place, 'text', '', text]);
    }
    state.at = state.at + 2;
    if (name(state) !== tag) {
        throw new FailedError('failed');
    }
    space(state);
    if (!starts(state, '>')) {
        throw new FailedError('failed');
    }
    state.at = state.at + 1;
}
function entries(octets) {
    let end = octets.length - 22;
    while (end >= 0 && octets.readUInt32LE(end) !== 0x06054b50) {
        end = end - 1;
    }
    if (end < 0) {
        throw new FailedError('failed');
    }
    const found = [];
    let at = octets.readUInt32LE(end + 16);
    while (found.length < octets.readUInt16LE(end + 10)) {
        if (octets.readUInt32LE(at) !== 0x02014b50) {
            throw new FailedError('failed');
        }
        const length = octets.readUInt16LE(at + 28);
        found.push({ name: octets.toString('utf8', at + 46, at + 46 + length), method: octets.readUInt16LE(at + 10), size: octets.readUInt32LE(at + 20), offset: octets.readUInt32LE(at + 42) });
        at = at + 46 + length + octets.readUInt16LE(at + 30) + octets.readUInt16LE(at + 32);
    }
    return found;
}
function expanded(qualified, scope, named) {
    const colon = qualified.indexOf(':');
    if (colon < 0) {
        const namespace = named ? scope.get('') ?? '' : '';
        return namespace === '' ? qualified : '{' + namespace + '}' + qualified;
    }
    const namespace = scope.get(qualified.slice(0, colon));
    if (namespace === undefined) {
        throw new FailedError('failed');
    }
    return '{' + namespace + '}' + qualified.slice(colon + 1);
}
function misc(state) {
    space(state);
    while (starts(state, '<?') || starts(state, '<!')) {
        if (starts(state, '<?')) {
            skip(state, '?>');
        }
        else {
            if (starts(state, '<!--')) {
                skip(state, '-->');
            }
            else {
                if (state.text.indexOf('[', state.at) >= 0 && state.text.indexOf('[', state.at) < state.text.indexOf('>', state.at)) {
                    skip(state, ']');
                    skip(state, '>');
                }
                else {
                    skip(state, '>');
                }
            }
        }
        space(state);
    }
}
function name(state) {
    const start = state.at;
    while (state.at < state.text.length && !' \t\n/>=?'.includes(state.text[state.at])) {
        state.at = state.at + 1;
    }
    if (state.at === start) {
        throw new FailedError('failed');
    }
    return state.text.slice(start, state.at);
}
function parsed(part, text) {
    const state = { text: text.replaceAll('\r\n', '\n').replaceAll('\r', '\n'), at: 0 };
    const found = [];
    misc(state);
    if (!starts(state, '<')) {
        throw new FailedError('failed');
    }
    element(state, part, '', new Map([['xml', 'http://www.w3.org/XML/1998/namespace']]), found);
    misc(state);
    if (state.at < state.text.length) {
        throw new FailedError('failed');
    }
    return found;
}
function reference(entity) {
    if (entity.startsWith('#x')) {
        return String.fromCodePoint(parseInt(entity.slice(2), 16));
    }
    if (entity.startsWith('#')) {
        return String.fromCodePoint(parseInt(entity.slice(1), 10));
    }
    const named = new Map([['lt', '<'], ['gt', '>'], ['amp', '&'], ['apos', "'"], ['quot', '"']]).get(entity);
    if (named === undefined) {
        throw new FailedError('failed');
    }
    return named;
}
function skip(state, end) {
    const close = state.text.indexOf(end, state.at);
    if (close < 0) {
        throw new FailedError('failed');
    }
    const skipped = state.text.slice(state.at, close);
    state.at = close + end.length;
    return skipped;
}
function space(state) {
    while (state.at < state.text.length && ' \t\n'.includes(state.text[state.at])) {
        state.at = state.at + 1;
    }
}
function starts(state, token) {
    return state.text.startsWith(token, state.at);
}
