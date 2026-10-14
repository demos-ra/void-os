export function named(written, count) {
    return { 'sheet name': 'positions', header: ['position'], records: selected(written, count).map((found) => [String(found)]) };
}
export function written(positions) {
    return runs(positions);
}
export class RefusedError extends Error {}
function runs(positions) {
    const spans = [];
    for (const record of positions.records) {
        const number = Number(record[0]);
        if (spans.length > 0 && spans[spans.length - 1][1] + 1 === number) {
            spans[spans.length - 1][1] = number;
        }
        else {
            spans.push([number, number]);
        }
    }
    return spans.map(([first, last]) => first === last ? String(first) : String(first) + '-' + String(last)).join(';');
}
function selected(written, count) {
    function selection() {
        const named = [];
        for (const spec of written.split(';')) {
            for (const found of singlespec(spec)) {
                if (!named.includes(found)) {
                    named.push(found);
                }
            }
        }
        return named;
    }
    function singlespec(spec) {
        const separator = spec.indexOf('-');
        if (separator === -1) {
            const start = position(spec);
            return start >= 1 && start <= count ? [start] : [];
        }
        const start = position(spec.slice(0, separator));
        const end = position(spec.slice(separator + 1));
        if (start > end) {
            return [];
        }
        const numbers = [];
        let index = Math.max(start, 1);
        while (index <= Math.min(end, count)) {
            numbers.push(index);
            index = index + 1;
        }
        return numbers;
    }
    function position(text) {
        if (text === '*') {
            return count;
        }
        return number(text);
    }
    function number(text) {
        if (text === '' || ![...text].every((character) => '0123456789'.includes(character))) {
            throw new RefusedError('a selection must be written as 2, 1;3, 1-3 or 2-*: ' + written);
        }
        return Number(text);
    }
    return selection();
}
