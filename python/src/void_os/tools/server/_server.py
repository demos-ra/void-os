"""how the tool is offered and called over MCP"""
__all__ = ['serve']
import types
from mcp.server import MCPServer
from mcp.types import CallToolResult, TextContent
from typing import Any

def serve(values: dict[str, Any,], relational_model: types.ModuleType, data_bank: types.ModuleType, read: types.ModuleType) -> None:
    given = dict(values['records'])
    server = MCPServer(given['server name'], instructions=given['server instructions'].replace('{data bank folder}', data_bank.folder(values, relational_model)), version=given['version'])

    def reading(pathname: str, sheet: str='', records: str='', fields: str='', filter: str='', join: str='') -> CallToolResult:
        try:
            return CallToolResult(content=[TextContent(type='text', text=read.read(values, pathname, sheet, records, fields, filter, join, relational_model, data_bank))])
        except read.RefusedError as error:
            return CallToolResult(content=[TextContent(type='text', text=str(error))], is_error=True)
        except read.KeepingFailedError as error:
            return CallToolResult(content=[TextContent(type='text', text=str(error))], is_error=True)
    server.tool(name=given['tool name'], description=given['tool description'], structured_output=False)(reading)
    server.run()
