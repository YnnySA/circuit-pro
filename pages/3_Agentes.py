"""Módulo 3 — Agentes tutores personalizados (línea de negocio B2B)."""
import streamlit as st

from components.ui import section_header, step_card, feature_card, metric_card, divider
from data.mock_data import AGENT_PIPELINE, AGENT_BENEFITS, AGENT_CASES

section_header(
    "Módulo · B2B",
    "🤖 Agentes tutores personalizados",
    "Desarrollamos asistentes de IA especializados en el conocimiento de cada institución, "
    "con técnicas RAG y despliegue privado para proteger sus datos.",
)

# --- Métricas de propuesta de valor ------------------------------------
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card("RAG", "Recuperación aumentada")
with m2:
    metric_card("On-prem", "Despliegue privado")
with m3:
    metric_card("70%", "Menos carga de soporte")
with m4:
    metric_card("24/7", "Disponibilidad")

divider()

tab_flujo, tab_beneficios, tab_demo, tab_casos = st.tabs(
    ["🔄 Flujo de servicio", "⭐ Beneficios", "💬 Demo del agente", "🏢 Casos de uso"]
)

# ---- Tab 1: Flujo de servicio (pipeline) ------------------------------
with tab_flujo:
    st.markdown("#### Del conocimiento del cliente a un agente operativo")
    st.caption("Proceso de implementación en 5 etapas.")
    cols = st.columns(5)
    for i, (col, (titulo, desc)) in enumerate(zip(cols, AGENT_PIPELINE), start=1):
        with col:
            step_card(i, titulo, desc)
    st.write("")
    st.info(
        "El flujo es repetible y configurable: incorporar un nuevo cliente no requiere "
        "reconstruir la plataforma, solo cargar su base de conocimiento.",
        icon="♻️",
    )

# ---- Tab 2: Beneficios ------------------------------------------------
with tab_beneficios:
    st.markdown("#### Propuesta de valor para instituciones y empresas")
    cols = st.columns(2)
    for i, (icon, titulo, desc) in enumerate(AGENT_BENEFITS):
        with cols[i % 2]:
            feature_card(icon, titulo, desc)
            st.write("")

# ---- Tab 3: Demo simulada del agente ----------------------------------
with tab_demo:
    st.markdown("#### Demostración: agente especializado con RAG")
    st.caption(
        "Simulación: el agente responde usando los manuales internos del cliente. "
        "Las respuestas son demostrativas para el pitch."
    )

    cliente = st.selectbox(
        "Base de conocimiento del agente:",
        ["Manual de seguridad eléctrica · SEC", "Guía de mantenimiento de motores", "Apuntes de Circuitos I"],
    )

    pregunta = st.text_input(
        "Escribe una pregunta para el agente:",
        placeholder="Ej: ¿Cuál es el procedimiento antes de intervenir un tablero energizado?",
    )

    if st.button("Consultar al agente", type="primary"):
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(f"**Fuente consultada:** _{cliente}_")
            st.markdown(
                "Según los procedimientos cargados, antes de intervenir un tablero se debe "
                "aplicar **bloqueo y etiquetado (LOTO)**, verificar la **ausencia de tensión** "
                "con instrumento certificado y usar el **EPP** correspondiente. "
                "\n\n_Esta respuesta se genera recuperando los fragmentos relevantes del "
                "documento mediante RAG, citando la fuente interna._"
            )
            st.caption("📎 Referencia: Sección 4.2 — Procedimientos de intervención segura")
    else:
        st.markdown(
            "<div class='vq-card'><p>👋 Hola, soy el agente especializado de tu institución. "
            "Pregúntame sobre los manuales y procedimientos cargados.</p></div>",
            unsafe_allow_html=True,
        )

# ---- Tab 4: Casos de uso ----------------------------------------------
with tab_casos:
    st.markdown("#### Agentes desplegados (ejemplos)")
    for c in AGENT_CASES:
        with st.container(border=True):
            cols = st.columns([1.2, 1.2, 1.6])
            cols[0].markdown(f"**Cliente**\n\n{c['cliente']}")
            cols[1].markdown(f"**Agente**\n\n{c['agente']}")
            cols[2].markdown(f"**Base de conocimiento**\n\n{c['base']}")
