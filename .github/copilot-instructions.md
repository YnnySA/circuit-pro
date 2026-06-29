# Copilot instructions for CircuitProIA

## Build, run, test, and lint

### Environment setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app
```bash
streamlit run app.py
```

### Tests and lint
- There is currently no test suite or lint configuration committed in this repository (`pytest`, `ruff`, `flake8`, etc. are not configured).
- If you add tests, prefer `pytest` and run a single test with:
```bash
pytest path\to\test_file.py::test_name
```

## High-level architecture

- `app.py` is the only entrypoint and controls global app behavior: Streamlit page config, global CSS injection, sidebar branding, shared `st.session_state` defaults, and navigation via `st.navigation` + `st.Page`.
- Main user-facing surfaces are in `pages/` (`0_Inicio.py` to `4_Negocio.py`). These files mostly orchestrate layout and delegate domain rendering.
- Reusable UI primitives live in `components/`:
  - `theme.py` centralizes design tokens (`COLORS`) and injects global CSS.
  - `ui.py` provides declarative helpers (`section_header`, `feature_card`, `metric_card`, `chips`, `step_card`, `hero`, etc.) and embeds the logo from `assets/`.
- Domain content and simulations are split by module:
  - `modules/students/unit_1/` contains educational content and interactive logic (`teoria`, `glosario`, `ejercicios`, `cuestionarios`, `graficos`, `flujo_carga`).
  - `data/mock_data.py` provides cross-page mock datasets (students, industry, agents, business).
  - `data/cuestionarios_data.py` contains the full formative-quiz banks and author attribution metadata.

## Key repository conventions

- **Page modules are composition layers**: keep `pages/*.py` focused on layout/flow and pull substantial logic into `modules/...` or `components/...`.
- **Module API convention**: feature modules expose a top-level `render()` function and are called from pages.
- **Shared state is explicit and namespaced**:
  - Cross-module keys are initialized in `app.py` (`quiz_ohm_answered`, `case_answered`, `checklist_done`, `ej_expanded`, etc.).
  - Quiz state is namespaced per questionnaire (`quiz_{qid}` in `cuestionarios.py`).
  - Widget keys use stable prefixes (`radio_{...}`, `btn_{...}`, `fc_*`) to preserve interaction state across reruns.
- **UI consistency comes from component helpers + global CSS**, not ad-hoc styling in each page. Prefer reusing `components/ui.py` helpers before adding new raw `st.markdown(..., unsafe_allow_html=True)` blocks.
- **Educational/quiz data has fixed structure**: in `cuestionarios_data.py`, each question uses `q`, `opciones`, `correcta` (index), `pista`, `ok`, and `fb`. Preserve this schema when adding content.
- **Language/content convention**: user-visible copy is Spanish and domain-specific to electrical engineering/industrial training; keep terminology and tone aligned.
