# Copilot instructions for CircuitProIA (Circuit Pro)

This file collects the repository-specific guidance Copilot-powered agents should use when operating on this project.

---

## 1) Build, run, test, and lint (concrete commands)

Prereqs: Python 3.8+ (CI/workflow uses 3.11). Node/npm only needed for MCP tooling.

Windows (recommended for local development):
```powershell
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Single test (no tests currently committed):
```powershell
# If pytest is added, run one test like:
pytest path\to\test_file.py::test_name
```

Linting: no linter configured. If added, prefer `ruff`/`flake8` and document commands here.

Requirements (tracked): see `requirements.txt` (streamlit, pandas, numpy, plotly).

---

## 2) High-level architecture (what matters across files)

- app.py: single entrypoint. Sets page config, injects global CSS, initializes `st.session_state`, registers pages via `st.navigation()` and runs navigation.
- pages/: top-level Streamlit pages (0_Inicio.py ... 4_Negocio.py). Pages orchestrate layout and call feature modules.
- components/: reusable UI primitives
  - components/theme.py — palette (COLORS dict), global CSS injection (Consolas monospace font), layout helpers
  - components/ui.py — declarative helpers (cards, metric tiles, chips, step cards, hero, etc.)
- modules/students/unit_1/: domain modules (each file exposes a render() function): teoria.py, ejercicios.py, cuestionarios.py, glosario.py, graficos.py, flujo_carga.py, sistema6.py, factor_potencia.py
- data/: mock and content data (mock_data.py, cuestionarios_data.py, unidad_1_data.py)

State and flow:
- Centralized `st.session_state` keys are initialized in app.py. Important keys:
  - quiz_ohm_answered, case_answered, checklist_done (list), agent_steps_seen (int)
  - ej_expanded (dict), ej_answered (dict), ej_checked (dict)
- UI widgets use stable key prefixes (e.g., radio_{...}, btn_{...}, fc_*) so reruns preserve state.
- Font: Monospace (Consolas, fallback Courier New); palette defined in components/theme.py as COLORS dict.

---

## 3) Key repository conventions (for Copilot to follow)

- Module API: feature modules expose a top-level `render()` that pages call; avoid moving rendering logic into pages. New modules like sistema6.py, flujo_carga.py, factor_potencia.py follow this pattern.
- Data schema for formative quizzes (`data/cuestionarios_data.py`): each question is a dict with keys: `q` (str), `opciones` (list), `correcta` (int index), `pista` (str), `ok` (str shown on correct), `fb` (feedback str). Preserve this structure when adding questions.
- UI components are canonical: prefer `components/ui.py` helpers over ad-hoc HTML/CSS in pages. Always use COLORS dict from theme.py for consistency.
- Language: all user-facing copy is Spanish. Keep terminology aligned to electrical engineering and training domain (V, A, W, Ω, Hz, pu, etc.).
- No server-side persistence: state is in `st.session_state`. Do not assume a DB or authentication unless adding them explicitly.
- Tests and linters are not present; if adding, include a minimal README entry and CI step.
- Widget keys must be stable across reruns to preserve state (use prefixes like `radio_`, `btn_`, `fc_`, `ej_` based on context).
- CSS is injected globally via `inject_global_css()` in app.py and called once per page load.

---

## 4) Files and CI relevant to Copilot

- `requirements.txt` lists the primary Python deps (streamlit, pandas, numpy, plotly). Use these versions for local envs.
- `.github/workflows/copilot-setup-steps.yml` exists and installs Python deps and the Playwright MCP package (`@playwright/mcp`) for MCP server usage.
- There are no other AI-assistant config files (no CLAUDE.md, AGENTS.md, .cursorrules, etc.).

---

## 5) MCP servers (Playwright)

The repository workflow installs the Playwright MCP package. Helpful local steps to match CI (optional):
```powershell
npm install -g @playwright/mcp
# or run via npx: npx @playwright/mcp
```
Add further MCP server config (ports, user, certs) only if planning to run browser-driven e2e or UI-recording sessions.

If you want, Copilot can add a short README snippet or a local start script for the MCP server.

---

## 6) Suggested additions (small, high-value)

- Add a short `dev-setup.md` with exact steps for Windows/macOS (venv activation differences).
- Add a minimal `pyproject.toml` or `requirements-dev.txt` if adding linters/tests.
- If RAG/agents are integrated later, add an `AGENTS.md` describing expected connectors and secrets handling.

---

Summary: updated and consolidated repository-specific Copilot instructions, added explicit commands, highlighted module and data conventions, and noted Playwright MCP setup in CI/workflow.

If this looks good, apply it to `.github/copilot-instructions.md` (already updated). Want Copilot to also add a small dev-setup.md and a local MCP start script? Reply with preference or ask me to proceed.
