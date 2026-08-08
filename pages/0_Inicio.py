"""Página de inicio / landing principal de CircuitProIA."""
import streamlit as st

from components.ui import (
    hero, section_header, feature_card, metric_card, chips, divider
)
from data.mock_data import BUSINESS_METRICS
from data.i18n import t, get_language

lang = get_language()

# --- Hero ---------------------------------------------------------------
hero(
    pill=t("inicio.pill", lang),
    title=t("inicio.hero_title", lang),
    subtitle=t("inicio.hero_subtitle", lang),
    icon_size=120,
    icon_position="left",
)

st.write("")

# --- Métricas de cabecera (4 columnas) ----------------------------------
# Valores numéricos desde mock_data; labels traducidos desde i18n
METRIC_VALUES = [item[0] for item in BUSINESS_METRICS]
METRIC_LABELS = [
    t("inicio.metric_label_0", lang),
    t("inicio.metric_label_1", lang),
    t("inicio.metric_label_2", lang),
    t("inicio.metric_label_3", lang),
]

cols = st.columns(4)
for col, num, label in zip(cols, METRIC_VALUES, METRIC_LABELS):
    with col:
        metric_card(num, label)

divider()

# --- Resumen de los tres módulos ---------------------------------------
section_header(
    t("inicio.modules_eyebrow", lang),
    t("inicio.modules_title", lang),
    t("inicio.modules_subtitle", lang),
)

c1, c2, c3 = st.columns(3)
with c1:
    feature_card(
        "🎓",
        t("inicio.students_title", lang),
        t("inicio.students_text", lang),
    )
with c2:
    feature_card(
        "🏭",
        t("inicio.industry_title", lang),
        t("inicio.industry_text", lang),
    )
with c3:
    feature_card(
        "🤖",
        t("inicio.agents_title", lang),
        t("inicio.agents_text", lang),
    )

st.write("")
st.info(
    t("inicio.info", lang),
    icon="🧭",
)

divider()

# --- Propuesta de valor en bloques -------------------------------------
section_header(
    t("inicio.why_title", lang),
    t("inicio.why_subtitle", lang),
)

v1, v2, v3 = st.columns(3)
with v1:
    feature_card(
        "🎯",
        t("inicio.value_specialization", lang),
        t("inicio.value_specialization_text", lang),
    )
with v2:
    feature_card(
        "🔒",
        t("inicio.value_privacy", lang),
        t("inicio.value_privacy_text", lang),
    )
with v3:
    feature_card(
        "🚀",
        t("inicio.value_scalability", lang),
        t("inicio.value_scalability_text", lang),
    )

st.write("")
st.markdown(f"##### {t('inicio.tech_section', lang)}")
tech_items = [
    ("Python", "Python"),
    ("Streamlit", "Streamlit"),
    ("RAG", "RAG"),
    ("LLM especializados", "Specialized LLMs"),
    ("Despliegue privado", "Private Deployment"),
    ("Analítica de aprendizaje", "Learning Analytics"),
    ("Gamificación", "Gamification"),
]
if lang == "es":
    tech_display = [item[0] for item in tech_items]
else:
    tech_display = [item[1] for item in tech_items]
chips(tech_display, variant="cyan")
