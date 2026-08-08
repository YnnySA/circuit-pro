"""Módulo 1 — Laboratorio digital para estudiantes de ingeniería eléctrica."""
import numpy as np
import pandas as pd
import streamlit as st

from components.ui import section_header, metric_card, chips, divider
from data.mock_data import STUDENT_UNITS, QUIZ_OHM, RESISTANCE_OHMS
from data.i18n import t, get_language
from modules.students.unit_1 import teoria, glosario, ejercicios, graficos, flujo_carga, factor_potencia, sistema6

lang = get_language()

section_header(
    t("estudiantes.section_title", lang),
    t("estudiantes.section_subtitle", lang),
    t("estudiantes.section_description", lang),
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
    metric_card(f"{prom}%", t("estudiantes.metric_progress", lang))
with m2:
    metric_card(f"{completadas}/{len(STUDENT_UNITS)}", t("estudiantes.metric_units", lang))
with m3:
    metric_card(ultima_respuesta, t("estudiantes.metric_last_answer", lang))
with m4:
    metric_card("🔥 7", t("estudiantes.metric_streak", lang))

divider()

# --- Pestañas del módulo ------------------------------------------------
tab_guia, tab_glosario, tab_ejercicio, tab_grafico = st.tabs([
    t("estudiantes.tab_guides", lang),
    t("estudiantes.tab_glossary", lang),
    t("estudiantes.tab_exercise", lang),
    t("estudiantes.tab_graphics", lang),
])
# ---- Tab 1: Guías por unidad ------------------------------------------
with tab_guia:
    for i, u in enumerate(STUDENT_UNITS):
        with st.expander(f"{u['titulo']}  ·  {u['estado']}", expanded=False):

            if u["estado"] == "Bloqueada":
                st.warning(t("estudiantes.unit_locked", lang), icon="🔒")

            elif u["estado"] == "Completada":
                st.success(t("estudiantes.unit_completed", lang), icon="✅")
                if i == 0:                    # ← solo Unidad 1
                    teoria.render(lang)

            elif u["estado"] == "En curso":
                if i == 0:                    # ← solo Unidad 1
                    teoria.render(lang)
                else:                         # ← Unidades 2, 3... en construcción
                    st.info(
                        t("estudiantes.unit_building", lang),
                        icon="🔨",
                    )
# ---- Tab 2: Glosario ──────────────────────────────────────────────────
with tab_glosario:
    glosario.render(lang)

# ---- Tab 3: Ejercicios interactivos --------------------------------------
with tab_ejercicio:
    ejercicios.render(lang)

# ---- Tab 4: Visualización — sub-pestañas por simulador ----------------
with tab_grafico:
    sim_ohm, sim_flujo, sim_fp, sim_s6 = st.tabs([
        t("estudiantes.sim_ohm", lang),
        t("estudiantes.sim_flow", lang),
        t("estudiantes.sim_power_factor", lang),
        t("estudiantes.sim_harmonics", lang),
    ])
    with sim_ohm:
        graficos.render(lang)
    with sim_flujo:
        flujo_carga.render(lang)
    with sim_fp:
        factor_potencia.render(lang)
    with sim_s6:
        sistema6.render(lang)
