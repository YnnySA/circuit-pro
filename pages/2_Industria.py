"""Módulo 2 — Capacitación aplicada para profesionales de la industria."""
import streamlit as st

from components.ui import section_header, metric_card, chips, divider
from data.mock_data import INDUSTRY_TRACKS, INDUSTRY_CASE, COMPLIANCE_CHECKLIST

section_header(
    "Módulo · Industria",
    "🏭 Capacitación aplicada por competencias",
    "Formación aterrizada a escenarios reales de planta: rutas por competencias, casos "
    "prácticos, simulaciones y checklists de cumplimiento.",
)

# --- Métricas ejecutivas -----------------------------------------------
prom = int(sum(t["progreso"] for t in INDUSTRY_TRACKS) / len(INDUSTRY_TRACKS))
m1, m2, m3, m4 = st.columns(4)
with m1:
    metric_card(f"{len(INDUSTRY_TRACKS)}", "Rutas de capacitación activas")
with m2:
    metric_card(f"{prom}%", "Avance promedio del equipo")
with m3:
    metric_card("24 h", "Horas de contenido")
with m4:
    metric_card("98%", "Cumplimiento de seguridad")

divider()

tab_rutas, tab_caso, tab_check = st.tabs(
    ["🧭 Rutas por competencias", "🛠️ Caso práctico", "✅ Checklist de cumplimiento"]
)

# ---- Tab 1: Rutas de capacitación -------------------------------------
with tab_rutas:
    st.markdown("#### Programas de formación por competencias")
    for t in INDUSTRY_TRACKS:
        with st.container(border=True):
            top = st.columns([3, 1, 1])
            with top[0]:
                st.markdown(f"**{t['nombre']}**")
            with top[1]:
                st.caption(f"Nivel: {t['nivel']}")
            with top[2]:
                st.caption(f"Duración: {t['duracion']}")
            st.progress(t["progreso"] / 100, text=f"Avance: {t['progreso']}%")
            chips(t["competencias"], variant="amber")

# ---- Tab 2: Caso práctico ---------------------------------------------
with tab_caso:
    st.markdown(f"#### {INDUSTRY_CASE['titulo']}")
    st.info(INDUSTRY_CASE["contexto"], icon="📋")
    st.markdown(f"**{INDUSTRY_CASE['pregunta']}**")

    eleccion = st.radio(
        "Selecciona la acción correcta:",
        INDUSTRY_CASE["opciones"],
        index=None,
        key="case_radio",
    )
    if st.button("Evaluar decisión", type="primary"):
        st.session_state.case_answered = True

    if st.session_state.case_answered:
        if eleccion is None:
            st.warning("Selecciona una opción antes de evaluar.", icon="✋")
        elif eleccion == INDUSTRY_CASE["correcta"]:
            st.success("Decisión correcta. " + INDUSTRY_CASE["explicacion"], icon="✅")
        else:
            st.error("Decisión riesgosa. " + INDUSTRY_CASE["explicacion"], icon="⚠️")

# ---- Tab 3: Checklist de cumplimiento ---------------------------------
with tab_check:
    st.markdown("#### Checklist de inspección y cumplimiento")
    st.caption("Marca cada ítem completado. El progreso se actualiza en tiempo real.")

    marcados = []
    for i, item in enumerate(COMPLIANCE_CHECKLIST):
        if st.checkbox(item, key=f"chk_{i}"):
            marcados.append(item)

    pct = int(len(marcados) / len(COMPLIANCE_CHECKLIST) * 100)
    st.session_state.checklist_done = marcados
    divider()
    st.progress(pct / 100, text=f"Cumplimiento: {pct}%")
    if pct == 100:
        st.success("Checklist completo. Equipo apto para operación.", icon="🏅")
    elif pct >= 60:
        st.info("Avance aceptable. Completa los ítems restantes.", icon="📈")
    else:
        st.warning("Cumplimiento insuficiente para autorizar la operación.", icon="🚧")
