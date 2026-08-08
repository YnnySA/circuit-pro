"""Módulo 3 — Agentes tutores personalizados (línea de negocio B2B)."""
import streamlit as st

from components.ui import section_header, step_card, feature_card, metric_card, divider
from data.mock_data import AGENT_PIPELINE, AGENT_BENEFITS, AGENT_CASES
from data.i18n import t, get_language

lang = get_language()

section_header(
    t("agentes.section_eyebrow", lang),
    t("agentes.section_title", lang),
    t("agentes.section_desc", lang),
)

# --- Métricas de propuesta de valor ------------------------------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("RAG", t("agentes.metric_rag", lang))
with m2:
    metric_card("On-prem", t("agentes.metric_onprem", lang))
with m3:
    metric_card("70%", t("agentes.metric_support", lang))
with m4:
    metric_card("24/7", t("agentes.metric_availability", lang))

divider()

tab_flujo, tab_beneficios, tab_demo, tab_casos = st.tabs([
    t("agentes.tab_pipeline", lang),
    t("agentes.tab_beneficios", lang),
    t("agentes.tab_demo", lang),
    t("agentes.tab_casos", lang),
])

# ---- Tab 1: Flujo de servicio (pipeline) ------------------------------
with tab_flujo:
    st.markdown(f"#### {t('agentes.pipeline_header', lang)}")
    st.caption(t("agentes.pipeline_caption", lang))
    cols = st.columns(5)
    for i, (col, (titulo, desc)) in enumerate(zip(cols, AGENT_PIPELINE), start=1):
        with col:
            step_card(i, titulo, desc)
    st.write("")
    st.info(t("agentes.pipeline_info", lang), icon="♻️")

# ---- Tab 2: Beneficios ------------------------------------------------
with tab_beneficios:
    st.markdown(f"#### {t('agentes.benefits_header', lang)}")
    cols = st.columns(2)
    for i, (icon, titulo, desc) in enumerate(AGENT_BENEFITS):
        with cols[i % 2]:
            feature_card(icon, titulo, desc)
            st.write("")

# ---- Tab 3: Demo simulada del agente ----------------------------------
with tab_demo:
    st.markdown(f"#### {t('agentes.demo_header', lang)}")
    st.caption(t("agentes.demo_caption", lang))

    cliente = st.selectbox(
        t("agentes.demo_select", lang),
        ["Manual de seguridad eléctrica · SEC", "Guía de mantenimiento de motores", "Apuntes de Circuitos I"],
    )

    pregunta = st.text_input(
        t("agentes.demo_input", lang),
        placeholder=t("agentes.demo_placeholder", lang),
    )

    if st.button(t("agentes.demo_btn", lang), type="primary"):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**{t('agentes.demo_source', lang)}** _{cliente}_")
            st.markdown(t("agentes.demo_response", lang))
            st.caption(t("agentes.demo_ref", lang))
    else:
        st.markdown(
            f"<div class='vq-card'><p>{t('agentes.demo_greeting', lang)}</p></div>",
            unsafe_allow_html=True,
        )

# ---- Tab 4: Casos de uso ----------------------------------------------
with tab_casos:
    st.markdown(f"#### {t('agentes.cases_header', lang)}")
    for c in AGENT_CASES:
        with st.container(border=True):
            cols = st.columns([1.2, 1.2, 1.6])
            cols[0].markdown(f"**{t('agentes.cases_col_client', lang)}**\n\n{c['cliente']}")
            cols[1].markdown(f"**{t('agentes.cases_col_agent', lang)}**\n\n{c['agente']}")
            cols[2].markdown(f"**{t('agentes.cases_col_base', lang)}**\n\n{c['base']}")
