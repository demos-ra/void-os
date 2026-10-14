import * as read from './read/read.js';
import * as server from './server/server.js';
export function serve(values, relationalModel, dataBank) {
    return server.serve(values, relationalModel, dataBank, read);
}
