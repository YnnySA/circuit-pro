Developer setup (Windows and macOS)

This file documents the minimal, exact steps to set up a local development environment and run the app and the Playwright MCP server used by CI.

Windows (PowerShell)

```powershell
# 1) Create virtual environment
python -m venv venv
# 2) Activate
venv\Scripts\activate
# 3) Upgrade pip and install deps
python -m pip install --upgrade pip
pip install -r requirements.txt
# 4) Run the app
streamlit run app.py
```

macOS / Linux (bash)

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Playwright MCP server (local)

CI installs the Playwright MCP package. Locally use npx (no global install required):

```powershell
# Windows (PowerShell)
npx @playwright/mcp
```

```bash
# macOS / Linux
npx @playwright/mcp
```

If you prefer a global install:

```bash
npm install -g @playwright/mcp
# then
playwright-mcp --help
```

Notes
- Python: code was developed and CI uses Python 3.11; Python 3.8+ is supported.
- No tests or linters are committed; if adding them, document commands and add CI steps.
- All user-facing copy is Spanish; prefer Spanish for new strings.
- State is in st.session_state; no DB or auth present by default.
