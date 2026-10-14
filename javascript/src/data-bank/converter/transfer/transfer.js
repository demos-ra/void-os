import * as key from './key/key.js';
import * as order from './order/order.js';
import * as relation from './relation/relation.js';
export function transfer(schema, input) {
    const layout = relation.relations(schema, input);
    return layout.concat([key.keys(layout[4], input[0]), order.order(schema, [layout[0], layout[2]])]);
}
