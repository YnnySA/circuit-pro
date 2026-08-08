#!/usr/bin/env bash
# Start Playwright MCP server (bash)
# Usage: ./start-mcp.sh from repo root

if ! command -v npx >/dev/null 2>&1; then
  echo "npx not found. Install Node.js and npm: https://nodejs.org/"
  exit 1
fi

npx @playwright/mcp
