"""Módulo 1 — Laboratorio digital para estudiantes de ingeniería eléctrica."""
import numpy as np
import pandas as pd
import streamlit as st

from components.ui import section_header, metric_card, chips, divider
from data.mock_data import STUDENT_UNITS, QUIZ_OHM, RESISTANCE_OHMS

section_header(
    "Módulo · Estudiantes",
    "🎓 Laboratorio digital de circuitos y máquinas eléctricas",
    "Aprendizaje guiado por unidades, con ejercicios interactivos, gráficos explicativos "
    "y retroalimentación inmediata.",
)

# --- Indicadores de avance general -------------------------------------
prom = int(np.mean([u["progreso"] for u in STUDENT_UNITS]))
completadas = sum(1 for u in STUDENT_UNITS if u["estado"] == "Completada")
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card(f"{prom}%", "Progreso global del curso")
with m2:
    metric_card(f"{completadas}/{len(STUDENT_UNITS)}", "Unidades completadas")
with m3:
    metric_card("1.0 A", "Última respuesta correcta")
with m4:
    metric_card("🔥 7", "Días de racha de estudio")

divider()

# --- Pestañas del módulo ------------------------------------------------
tab_guia, tab_ejercicio, tab_grafico = st.tabs(
    ["📚 Guías de aprendizaje", "🧪 Ejercicio interactivo", "📈 Visualización"]
)

# ---- Tab 1: Guías por unidad ------------------------------------------
with tab_guia:
    st.markdown("#### Plan de estudios por unidades")
    for u in STUDENT_UNITS:
        with st.expander(f"{u['titulo']}  ·  {u['estado']}", expanded=(u["estado"] == "En curso")):
            st.progress(u["progreso"] / 100, text=f"Avance: {u['progreso']}%")
            st.caption("Temas de la unidad:")
            chips(u["temas"], variant="cyan")
            if u["estado"] == "Bloqueada":
                st.warning("Completa la unidad anterior para desbloquear este contenido.", icon="🔒")
            elif u["estado"] == "Completada":
                st.success("Unidad completada. ¡Buen trabajo!", icon="✅")

# ---- Tab 2: Ejercicio interactivo con feedback ------------------------
with tab_ejercicio:
    st.markdown("#### Ejercicio: Ley de Ohm en circuito serie")
    st.markdown(QUIZ_OHM["enunciado"])
    st.write("")

    eleccion = st.radio(
        "Selecciona tu respuesta:",
        QUIZ_OHM["opciones"],
        index=None,
        key="quiz_ohm_radio",
    )

    col_a, col_b = st.columns([1, 3])
    with col_a:
        verificar = st.button("Verificar respuesta", type="primary", use_container_width=True)

    if verificar:
        st.session_state.quiz_ohm_answered = True

    if st.session_state.quiz_ohm_answered:
        if eleccion is None:
            st.warning("Selecciona una opción antes de verificar.", icon="✋")
        elif eleccion == QUIZ_OHM["correcta"]:
            st.success("¡Correcto! " + QUIZ_OHM["explicacion"], icon="🎉")
            st.balloons()
        else:
            st.error(
                f"No es correcto. Tu respuesta: **{eleccion}**.\n\n"
                + QUIZ_OHM["explicacion"],
                icon="❌",
            )

    st.caption("La retroalimentación es inmediata e incluye el desarrollo paso a paso.")

# ---- Tab 3: Visualización dinámica ------------------------------------
with tab_grafico:
    st.markdown("#### Curva característica V–I de una resistencia")
    st.caption(
        "Mueve el control para cambiar la resistencia y observa cómo varía la corriente "
        "según la Ley de Ohm (I = V / R)."
    )
    r = st.slider("Resistencia R (Ω)", min_value=2, max_value=24, value=RESISTANCE_OHMS, step=1)

    voltajes = np.linspace(0, 24, 50)
    corrientes = voltajes / r
    df = pd.DataFrame({"Tensión (V)": voltajes, "Corriente (A)": corrientes}).set_index("Tensión (V)")

    st.line_chart(df, height=320, color="#0B5FFF")

    c1, c2 = st.columns(2)
    with c1:
        metric_card(f"{r} Ω", "Resistencia seleccionada")
    with c2:
        metric_card(f"{24 / r:.2f} A", "Corriente máxima (a 24 V)")
    st.caption("Gráfico generado en tiempo real para apoyar la comprensión visual del concepto.")
