"""
CircuitPro · IA — Plataforma de IA aplicada a educación e industria
Punto de entrada principal. Define la navegación multipágina con st.navigation.

Ejecutar con: streamlit run app.py
"""
import streamlit as st

from components.theme import inject_global_css
from components.ui import sidebar_brand

st.set_page_config(
    page_title="CircuitPro · IA para educación e industria",
    page_icon="None",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# Inicialización de estado compartido entre módulos
def _init_state():
    defaults = {
        # Estado general
        "quiz_ohm_answered": False,
        "case_answered":     False,
        "checklist_done":    [],
        "agent_steps_seen":  0,
        # ── Estado de ejercicios (fix del expander) ──
        "ej_expanded":       {},   # {ej_id: bool}  — mantiene expander abierto
        "ej_answered":       {},   # {ej_id: int}   — índice de opción elegida
        "ej_checked":        {},   # {ej_id: bool}  — si ya verificó
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ---------------------------------------------------------------------------
inicio      = st.Page("pages/0_Inicio.py",      title="Inicio",                icon="🏠", default=True)
estudiantes = st.Page("pages/1_Estudiantes.py", title="Estudiantes",           icon="🎓")
industria   = st.Page("pages/2_Industria.py",   title="Capacitación industrial",icon="🏭")
agentes     = st.Page("pages/3_Agentes.py",     title="Agentes B2B",           icon="🤖")
negocio     = st.Page("pages/4_Negocio.py",     title="Impacto y negocio",     icon="📈")

sidebar_brand()

pg = st.navigation({
    "Plataforma":              [inicio],
    "Módulos":                 [estudiantes, industria, agentes],
    "Asistencia Especializada":[negocio],
})

st.sidebar.markdown("---")
st.sidebar.caption("Prototipo de demostración · v0.1")
st.sidebar.caption("© 2026 CircuitProIA")

pg.run()