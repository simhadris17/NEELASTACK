# MCP

MCP tools are listed at `GET /mcp/tools`, executed via `POST /mcp/execute`, and
managed through authenticated register/delete endpoints. Only registered
handlers can be enabled; arbitrary callable names and user-supplied database
configuration are rejected.
