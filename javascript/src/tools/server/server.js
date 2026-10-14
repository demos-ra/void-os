import { McpServer } from '@modelcontextprotocol/server';
import { StdioServerTransport } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';
export function serve(values, relationalModel, dataBank, read) {
    const given = new Map(values.records);
    const server = new McpServer({ name: given.get('server name'), version: given.get('version') }, { instructions: given.get('server instructions').replace('{data bank folder}', dataBank.folder(values, relationalModel)) });
    server.registerTool(given.get('tool name'), { description: given.get('tool description'), inputSchema: z.object({ pathname: z.string(), sheet: z.string().optional(), records: z.string().optional(), fields: z.string().optional(), filter: z.string().optional(), join: z.string().optional() }) }, (input) => {
        try {
            return { content: [{ type: 'text', text: read.read(values, input.pathname, input.sheet ?? '', input.records ?? '', input.fields ?? '', input.filter ?? '', input.join ?? '', relationalModel, dataBank) }] };
        }
        catch (error) {
            if (error instanceof read.RefusedError) {
                return { content: [{ type: 'text', text: error.message }], isError: true };
            }
            if (error instanceof read.KeepingFailedError) {
                return { content: [{ type: 'text', text: error.message }], isError: true };
            }
            throw error;
        }
    });
    server.connect(new StdioServerTransport());
}
