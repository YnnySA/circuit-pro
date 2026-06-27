"""Módulo 1 — Laboratorio digital para estudiantes de ingeniería eléctrica."""
import numpy as np
import pandas as pd
import streamlit as st

from components.ui import section_header, metric_card, chips, divider
from data.mock_data import STUDENT_UNITS, QUIZ_OHM, RESISTANCE_OHMS
from modules.students.unit_1 import teoria, glosario, ejercicios, graficos

section_header(
    "Módulo · Estudiantes",
    "🎓 Laboratorio digital de circuitos y máquinas eléctricas",
    "Aprendizaje guiado por unidades, con ejercicios interactivos, gráficos explicativos "
    "y retroalimentación inmediata.",
)

# --- Indicadores de avance general -------------------------------------
prom = int(np.mean([u["progreso"] for u in STUDENT_UNITS]))
completadas = sum(1 for u in STUDENT_UNITS if u["estado"] == "Completada")

# Última respuesta correcta: se deriva del quiz si ya fue respondido correctamente
if st.session_state.get("quiz_ohm_answered") and st.session_state.get("quiz_ohm_correct", False):
    ultima_respuesta = QUIZ_OHM["correcta"]
else:
    ultima_respuesta = "—"

m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card(f"{prom}%", "Progreso global del curso")
with m2:
    metric_card(f"{completadas}/{len(STUDENT_UNITS)}", "Unidades completadas")
with m3:
    metric_card(ultima_respuesta, "Última respuesta correcta")
with m4:
    metric_card("🔥 7", "Días de racha de estudio")

divider()

# --- Pestañas del módulo ------------------------------------------------
tab_guia, tab_glosario, tab_ejercicio, tab_grafico = st.tabs([
    "📚 Guías de aprendizaje",
    "📖 Glosario",
    "🧪 Ejercicio interactivo",
    "📈 Visualización",
])
# ---- Tab 1: Guías por unidad ------------------------------------------
with tab_guia:
    for i, u in enumerate(STUDENT_UNITS):
        with st.expander(f"{u['titulo']}  ·  {u['estado']}", expanded=False):

            if u["estado"] == "Bloqueada":
                st.warning("Completa la unidad anterior para desbloquear este contenido.", icon="🔒")

            elif u["estado"] == "Completada":
                st.success("Unidad completada. ¡Buen trabajo!", icon="✅")
                if i == 0:                    # ← solo Unidad 1
                    teoria.render()

            elif u["estado"] == "En curso":
                if i == 0:                    # ← solo Unidad 1
                    teoria.render()
                else:                         # ← Unidades 2, 3... en construcción
                    st.info(
                        "🚧 Contenido en construcción. "
                        "Esta unidad estará disponible próximamente.",
                        icon="🔨",
                    )
# ---- Tab 2: Glosario ──────────────────────────────────────────────────
with tab_glosario:
    glosario.render()

# ---- Tab 3: Ejercicios interactivos --------------------------------------
with tab_ejercicio:
    ejercicios.render()

# ---- Tab 4: Gráficos explicativos --------------------------------------
with tab_grafico:
    graficos.render()
