# Start Playwright MCP server (PowerShell)
# Usage: Open PowerShell in the repo root and run: .\start-mcp.ps1

if (-not (Get-Command npx -ErrorAction SilentlyContinue)) {
    Write-Error "npx not found. Install Node.js and npm: https://nodejs.org/"
    exit 1
}

# Start the MCP server via npx (uses latest available locally/remote)
npx @playwright/mcp
