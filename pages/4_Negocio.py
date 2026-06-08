"""Sección de impacto y propuesta de negocio para el pitch."""
import pandas as pd
import streamlit as st

from components.ui import section_header, metric_card, feature_card, divider
from data.mock_data import (
    REVENUE_PROJECTION, MARKET_SEGMENTS, DIFFERENTIATORS, BUSINESS_METRICS
)

section_header(
    "Impacto y negocio",
    "📈 Una visión clara de crecimiento",
    "Modelo de negocio dual (B2C + B2B), mercado objetivo definido y escalabilidad basada "
    "en agentes inteligentes.",
)

# --- Métricas clave -----------------------------------------------------
cols = st.columns(4)
for col, (num, label) in zip(cols, BUSINESS_METRICS):
    with col:
        metric_card(num, label)

divider()

# --- Proyección de ingresos y mercado ----------------------------------
c1, c2 = st.columns([1.4, 1])

with c1:
    st.markdown("#### Proyección de ingresos (MM CLP)")
    st.caption("Escenario base a 4 años, combinando suscripciones B2C y contratos B2B.")
    df_rev = pd.DataFrame(
        {
            "B2C · Estudiantes": REVENUE_PROJECTION["b2c"],
            "B2B · Instituciones": REVENUE_PROJECTION["b2b"],
        },
        index=REVENUE_PROJECTION["anios"],
    )
    st.bar_chart(df_rev, height=320, color=["#00C2D1", "#0B5FFF"])
    total_a4 = REVENUE_PROJECTION["b2c"][-1] + REVENUE_PROJECTION["b2b"][-1]
    st.caption(f"Ingreso proyectado Año 4: **{total_a4} MM CLP** combinando ambas líneas.")

with c2:
    st.markdown("#### Mercado objetivo")
    st.caption("Distribución del mercado direccionable por segmento.")
    df_mkt = pd.DataFrame(
        {"Segmento": [s[0] for s in MARKET_SEGMENTS], "Peso (%)": [s[1] for s in MARKET_SEGMENTS]}
    ).set_index("Segmento")
    st.bar_chart(df_mkt, height=320, color="#FFB020", horizontal=True)

divider()

# --- Diferenciación -----------------------------------------------------
section_header(
    "Ventaja competitiva",
    "Qué nos hace diferentes",
)
cols = st.columns(2)
for i, (titulo, desc) in enumerate(DIFFERENTIATORS):
    with cols[i % 2]:
        feature_card("✨", titulo, desc)
        st.write("")

divider()

# --- Modelo de negocio y escalabilidad ---------------------------------
section_header(
    "Modelo y escalabilidad",
    "Cómo crece CircuitProIA",
)
b1, b2, b3 = st.columns(3)
with b1:
    feature_card(
        "💳",
        "B2C — Suscripción",
        "Estudiantes y profesionales acceden por suscripción mensual a guías, ejercicios "
        "y tutoría con IA.",
    )
with b2:
    feature_card(
        "🤝",
        "B2B — Licencias y servicios",
        "Universidades y empresas contratan agentes personalizados, despliegue privado "
        "y capacitación a medida.",
    )
with b3:
    feature_card(
        "🌎",
        "Expansión",
        "El mismo motor se replica a nuevos dominios técnicos y países de LATAM por "
        "configuración, no por reconstrucción.",
    )

st.write("")
st.success(
    "CircuitProIA combina valor educativo inmediato con un motor B2B escalable: un producto en "
    "etapa temprana con una ruta clara hacia el crecimiento.",
    icon="🚀",
)
