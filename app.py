"""
CircuitPro · IA — Plataforma de IA aplicada a educación e industria
Punto de entrada principal. Define la navegación multipágina con st.navigation.

Ejecutar con: streamlit run app.py
"""
import streamlit as st

from components.theme import inject_global_css
from components.ui import sidebar_brand
from data.i18n import t, get_language, set_language

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
        # ── Idioma ──
        "language":          "es", # código de idioma
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()

# ─────────────────────────────────────────────────────────
# Selector de idioma en la esquina superior derecha
# ─────────────────────────────────────────────────────────
col1, col2 = st.columns([0.80, 0.20])
with col2:
    lang = get_language()
    new_lang = st.selectbox(
        label=t("label.language", lang),
        options=["es", "en"],
        format_func=lambda x: t("label.spanish", lang) if x == "es" else t("label.english", lang),
        index=0 if lang == "es" else 1,
        key="lang_selector",
    )
    if new_lang != lang:
        set_language(new_lang)
        st.rerun()

# ─────────────────────────────────────────────────────────
# Navegación traduccida
# ─────────────────────────────────────────────────────────
lang = get_language()

inicio      = st.Page("pages/0_Inicio.py",      title=t("nav.inicio", lang),        icon="🏠", default=True)
estudiantes = st.Page("pages/1_Estudiantes.py", title=t("nav.estudiantes", lang),   icon="🎓")
industria   = st.Page("pages/2_Industria.py",   title=t("nav.industria", lang),     icon="🏭")
agentes     = st.Page("pages/3_Agentes.py",     title=t("nav.agentes", lang),       icon="🤖")
negocio     = st.Page("pages/4_Negocio.py",     title=t("nav.negocio", lang),       icon="📈")

sidebar_brand()

pg = st.navigation({
    t("sidebar.platform", lang):              [inicio],
    t("sidebar.modules", lang):                [estudiantes, industria, agentes],
    t("sidebar.specialized", lang):            [negocio],
})

st.sidebar.markdown("---")
st.sidebar.caption(t("sidebar.prototype", lang))
st.sidebar.caption(t("sidebar.copyright", lang))

pg.run()