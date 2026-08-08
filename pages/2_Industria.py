"""Módulo 2 — Capacitación aplicada para profesionales de la industria."""
import streamlit as st

from components.ui import section_header, metric_card, chips, divider
from data.mock_data import INDUSTRY_TRACKS, INDUSTRY_CASE, COMPLIANCE_CHECKLIST
from data.i18n import t, get_language

lang = get_language()

section_header(
    t("industria.section_eyebrow", lang),
    t("industria.section_title", lang),
    t("industria.section_desc", lang),
)

# --- Métricas ejecutivas -----------------------------------------------
prom = int(sum(track["progreso"] for track in INDUSTRY_TRACKS) / len(INDUSTRY_TRACKS))
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card(f"{len(INDUSTRY_TRACKS)}", t("industria.metric_routes", lang))
with m2:
    metric_card(f"{prom}%", t("industria.metric_progress", lang))
with m3:
    metric_card("24 h", t("industria.metric_hours", lang))
with m4:
    metric_card("98%", t("industria.metric_compliance", lang))

divider()

tab_rutas, tab_caso, tab_check = st.tabs([
    t("industria.tab_rutas", lang),
    t("industria.tab_caso", lang),
    t("industria.tab_checklist", lang),
])

# ---- Tab 1: Rutas de capacitación -------------------------------------
with tab_rutas:
    st.markdown(f"#### {t('industria.routes_header', lang)}")
    for track in INDUSTRY_TRACKS:
        with st.container(border=True):
            top = st.columns([3, 1, 1])
            with top[0]:
                st.markdown(f"**{track['nombre']}**")
            with top[1]:
                st.caption(f"{t('industria.level_label', lang)} {track['nivel']}")
            with top[2]:
                st.caption(f"{t('industria.duration_label', lang)} {track['duracion']}")
            st.progress(
                track["progreso"] / 100,
                text=f"{t('industria.progress_label', lang)} {track['progreso']}%",
            )
            chips(track["competencias"], variant="amber")

# ---- Tab 2: Caso práctico ---------------------------------------------
with tab_caso:
    st.markdown(f"#### {INDUSTRY_CASE['titulo']}")
    st.info(INDUSTRY_CASE["contexto"], icon="📋")
    st.markdown(f"**{INDUSTRY_CASE['pregunta']}**")

    eleccion = st.radio(
        t("industria.case_radio", lang),
        INDUSTRY_CASE["opciones"],
        index=None,
        key="case_radio",
    )
    if st.button(t("industria.case_btn", lang), type="primary"):
        st.session_state.case_answered = True

    if st.session_state.case_answered:
        if eleccion is None:
            st.warning(t("industria.case_no_selection", lang), icon="✋")
        elif eleccion == INDUSTRY_CASE["correcta"]:
            st.success(t("industria.case_correct", lang) + INDUSTRY_CASE["explicacion"], icon="✅")
        else:
            st.error(t("industria.case_wrong", lang) + INDUSTRY_CASE["explicacion"], icon="⚠️")

# ---- Tab 3: Checklist de cumplimiento ---------------------------------
with tab_check:
    st.markdown(f"#### {t('industria.checklist_header', lang)}")
    st.caption(t("industria.checklist_caption", lang))

    marcados = []
    for i, item in enumerate(COMPLIANCE_CHECKLIST):
        if st.checkbox(item, key=f"chk_{i}"):
            marcados.append(item)

    pct = int(len(marcados) / len(COMPLIANCE_CHECKLIST) * 100)
    st.session_state.checklist_done = marcados
    divider()
    st.progress(pct / 100, text=f"{t('industria.checklist_progress', lang)} {pct}%")
    if pct == 100:
        st.success(t("industria.checklist_ok", lang), icon="🏅")
    elif pct >= 60:
        st.info(t("industria.checklist_mid", lang), icon="📈")
    else:
        st.warning(t("industria.checklist_low", lang), icon="🚧")
