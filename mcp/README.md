# Arrow Core MCP Server

Official Model Context Protocol (MCP) server for Arrow Core on Robinhood Chain (Chain ID: 4663).

## Features
- `arrow_get_balance`: Live balance checking on Robinhood Chain RPC.
- `arrow_privacy_audit`: Real on-chain anonymity and exposure analysis.
- `arrow_get_quote`: Live private swap rate estimations.
- `arrow_protocol_stats`: Current protocol TVL, blocks, and anonymity set.

## Running Locally
```bash
node mcp/server.js
```

## Adding to Claude Desktop
Edit `claude_desktop_config.json` (located at `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "arrowcore": {
      "command": "node",
      "args": ["<FULL_PATH_TO>/mcp/server.js"]
    }
  }
}
```
