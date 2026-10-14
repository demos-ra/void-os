export function kept(sheets, filter) {
    const holds = filterExpression(filter);
    return sheets.map((sheet) => ({ 'sheet name': sheet['sheet name'], header: sheet.header, records: sheet.records.filter((record) => holds(record, sheet.records)) }));
}
export class RefusedError extends Error {}
function equal(left, right) {
    if (Array.isArray(left) && Array.isArray(right)) {
        return left.length === right.length && left.every((first, index) => equal(first, right[index]));
    }
    return left === right;
}
function filterExpression(written) {
    const characters = [...written];
    let position = 0;
    function logicalExpr() {
        return logicalOrExpr();
    }
    function logicalOrExpr() {
        const operands = [logicalAndExpr()];
        while (ahead('||')) {
            operands.push(logicalAndExpr());
        }
        return (current, root) => operands.some((operand) => operand(current, root));
    }
    function logicalAndExpr() {
        const operands = [basicExpr()];
        while (ahead('&&')) {
            operands.push(basicExpr());
        }
        return (current, root) => operands.every((operand) => operand(current, root));
    }
    function basicExpr() {
        if (take('!')) {
            blank();
            const negated = at('(') ? parenExpr() : testExpr();
            return (current, root) => !negated(current, root);
        }
        if (at('(')) {
            return parenExpr();
        }
        if (at('match') || at('search')) {
            return testExpr();
        }
        const start = position;
        const left = comparable();
        const operator = comparisonOp();
        if (operator === null) {
            position = start;
            return testExpr();
        }
        return comparisonExpr(left, operator, comparable());
    }
    function parenExpr() {
        expect('(');
        blank();
        const inner = logicalExpr();
        blank();
        expect(')');
        return inner;
    }
    function testExpr() {
        if (at('@') || at('$')) {
            const query = singularQuery();
            return (current, root) => query(current, root).length > 0;
        }
        return functionExpr();
    }
    function comparisonExpr(left, operator, right) {
        const compare = { '==': equal, '!=': (first, second) => !equal(first, second), '<': less, '<=': (first, second) => less(first, second) || equal(first, second), '>': (first, second) => less(second, first), '>=': (first, second) => less(second, first) || equal(first, second) }[operator];
        return (current, root) => compare(left(current, root), right(current, root));
    }
    function literal() {
        if (at('"') || at("'")) {
            return stringLiteral();
        }
        for (const [word, value] of [['true', true], ['false', false], ['null', null]]) {
            if (take(word)) {
                return value;
            }
        }
        return number();
    }
    function comparable() {
        if (at('@') || at('$')) {
            return singularQuery();
        }
        const value = literal();
        return (current, root) => [value];
    }
    function comparisonOp() {
        for (const operator of ['==', '!=', '<=', '>=', '<', '>']) {
            if (ahead(operator)) {
                return operator;
            }
        }
        return null;
    }
    function singularQuery() {
        const relative = take('@');
        if (!relative) {
            expect('$');
        }
        const segments = singularQuerySegments();
        return (current, root) => selected(relative ? current : root, segments);
    }
    function singularQuerySegments() {
        const segments = [];
        while (true) {
            const start = position;
            blank();
            if (at('.') || at('["') || at("['")) {
                segments.push(nameSegment());
            }
            else {
                if (at('[')) {
                    segments.push(indexSegment());
                }
                else {
                    position = start;
                    return segments;
                }
            }
        }
    }
    function nameSegment() {
        if (take('[')) {
            stringLiteral();
            expect(']');
            return (value) => [];
        }
        expect('.');
        const start = position;
        while (position < characters.length && nameChar(characters[position], position === start)) {
            position += 1;
        }
        if (position === start) {
            refuse();
        }
        return (value) => [];
    }
    function indexSegment() {
        expect('[');
        const index = integer();
        if (Math.abs(index) > 9007199254740991) {
            refuse();
        }
        expect(']');
        return (value) => Array.isArray(value) && -value.length <= index && index < value.length ? [value.at(index)] : [];
    }
    function number() {
        const start = position;
        if (!take('-0')) {
            integer();
        }
        if (take('.')) {
            digits();
        }
        if (take('e') || take('E')) {
            take('-') || take('+');
            digits();
        }
        return Number(characters.slice(start, position).join(''));
    }
    function functionExpr() {
        const start = position;
        while (characters[position] >= 'a' && characters[position] <= 'z') {
            position += 1;
        }
        const name = characters.slice(start, position).join('');
        if (!['match', 'search'].includes(name)) {
            refuse();
        }
        expect('(');
        blank();
        const value = comparable();
        blank();
        expect(',');
        blank();
        const pattern = comparable();
        blank();
        expect(')');
        return (current, root) => matched(value(current, root), pattern(current, root), name === 'match');
    }
    function stringLiteral() {
        const quote = characters[position];
        position += 1;
        const found = [];
        while (!take(quote)) {
            if (position === characters.length || characters[position] < ' ') {
                refuse();
            }
            position += 1;
            if (characters[position - 1] !== '\\') {
                found.push(characters[position - 1]);
            }
            else {
                if (take('u') && characters.slice(position, position + 4).length === 4 && characters.slice(position, position + 4).every((digit) => '0123456789abcdefABCDEF'.includes(digit))) {
                    position += 4;
                    found.push(String.fromCharCode(parseInt(characters.slice(position - 4, position).join(''), 16)));
                }
                else {
                    if (['b', 'f', 'n', 'r', 't', '/', '\\', quote].includes(characters[position])) {
                        position += 1;
                        found.push('bfnrt'.includes(characters[position - 1]) ? { b: '\b', f: '\f', n: '\n', r: '\r', t: '\t' }[characters[position - 1]] : characters[position - 1]);
                    }
                    else {
                        refuse();
                    }
                }
            }
        }
        return found.join('');
    }
    function integer() {
        const start = position;
        if (!take('0')) {
            take('-');
            if (!(characters[position] >= '1' && characters[position] <= '9')) {
                refuse();
            }
            digits();
        }
        return Number(characters.slice(start, position).join(''));
    }
    function digits() {
        const start = position;
        while (characters[position] >= '0' && characters[position] <= '9') {
            position += 1;
        }
        if (position === start) {
            refuse();
        }
    }
    function blank() {
        while (position < characters.length && ' \t\n\r'.includes(characters[position])) {
            position += 1;
        }
    }
    function at(token) {
        return characters.slice(position, position + token.length).join('') === token;
    }
    function take(token) {
        if (at(token)) {
            position += token.length;
            return true;
        }
        return false;
    }
    function ahead(token) {
        const start = position;
        blank();
        if (take(token)) {
            blank();
            return true;
        }
        position = start;
        return false;
    }
    function expect(token) {
        if (!take(token)) {
            refuse();
        }
    }
    function refuse() {
        throw new RefusedError('not a filter expression at character ' + String(position + 1) + ': ' + written);
    }
    const holds = logicalExpr();
    if (position < characters.length) {
        refuse();
    }
    return holds;
}
function less(left, right) {
    if (left.length !== 1 || right.length !== 1) {
        return false;
    }
    if (typeof left[0] === 'string' && typeof right[0] === 'string') {
        return left[0] < right[0];
    }
    return typeof left[0] === 'number' && typeof right[0] === 'number' && left[0] < right[0];
}
function matched(value, pattern, whole) {
    if (value.length !== 1 || pattern.length !== 1 || typeof value[0] !== 'string' || typeof pattern[0] !== 'string') {
        return false;
    }
    try {
        return new RegExp(whole ? '^(?:' + pattern[0] + ')$' : pattern[0], 'u').test(value[0]);
    }
    catch {
        return false;
    }
}
function nameChar(character, first) {
    if (character.codePointAt(0) < 128) {
        return 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_'.includes(character) || !first && '0123456789'.includes(character);
    }
    return character.codePointAt(0) < 0xD800 || character.codePointAt(0) > 0xDFFF;
}
function selected(node, segments) {
    let found = [node];
    for (const segment of segments) {
        found = found.length > 0 ? segment(found[0]) : [];
    }
    return found;
}
