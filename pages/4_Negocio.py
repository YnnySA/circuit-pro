"""Sección de impacto y propuesta de negocio para el pitch."""
import pandas as pd
import streamlit as st

from components.ui import section_header, metric_card, feature_card, divider
from data.mock_data import (
    REVENUE_PROJECTION, MARKET_SEGMENTS, DIFFERENTIATORS, BUSINESS_METRICS
)
from data.i18n import t, get_language

lang = get_language()

section_header(
    t("negocio.section_eyebrow", lang),
    t("negocio.section_title", lang),
    t("negocio.section_desc", lang),
)

# --- Métricas clave -----------------------------------------------------
METRIC_LABELS = [
    t("inicio.metric_label_0", lang),
    t("inicio.metric_label_1", lang),
    t("inicio.metric_label_2", lang),
    t("inicio.metric_label_3", lang),
]
METRIC_VALUES = [item[0] for item in BUSINESS_METRICS]
cols = st.columns(4)
for col, num, label in zip(cols, METRIC_VALUES, METRIC_LABELS):
    with col:
        metric_card(num, label)

divider()

# --- Proyección de ingresos y mercado ----------------------------------
c1, c2 = st.columns([1.4, 1])

with c1:
    st.markdown(f"#### {t('negocio.revenue_header', lang)}")
    st.caption(t("negocio.revenue_caption", lang))
    df_rev = pd.DataFrame(
        {
            t("negocio.revenue_b2c", lang): REVENUE_PROJECTION["b2c"],
            t("negocio.revenue_b2b", lang): REVENUE_PROJECTION["b2b"],
        },
        index=REVENUE_PROJECTION["anios"],
    )
    st.bar_chart(df_rev, height=320, color=["#00C2D1", "#0B5FFF"])
    total_a4 = REVENUE_PROJECTION["b2c"][-1] + REVENUE_PROJECTION["b2b"][-1]
    st.caption(
        f"{t('negocio.revenue_total', lang)} **{total_a4} {t('negocio.revenue_suffix', lang)}**"
    )

with c2:
    st.markdown(f"#### {t('negocio.market_header', lang)}")
    st.caption(t("negocio.market_caption", lang))
    df_mkt = pd.DataFrame(
        {
            t("negocio.market_col_segment", lang): [s[0] for s in MARKET_SEGMENTS],
            t("negocio.market_col_weight", lang): [s[1] for s in MARKET_SEGMENTS],
        }
    ).set_index(t("negocio.market_col_segment", lang))
    st.bar_chart(df_mkt, height=320, color="#FFB020", horizontal=True)

divider()

# --- Diferenciación -----------------------------------------------------
section_header(
    t("negocio.diff_eyebrow", lang),
    t("negocio.diff_title", lang),
)
cols = st.columns(2)
for i, (titulo, desc) in enumerate(DIFFERENTIATORS):
    with cols[i % 2]:
        feature_card("✨", titulo, desc)
        st.write("")

divider()

# --- Modelo de negocio y escalabilidad ---------------------------------
section_header(
    t("negocio.model_eyebrow", lang),
    t("negocio.model_title", lang),
)
b1, b2, b3 = st.columns(3)
with b1:
    feature_card(
        "💳",
        t("negocio.model_b2c_title", lang),
        t("negocio.model_b2c_text", lang),
    )
with b2:
    feature_card(
        "🤝",
        t("negocio.model_b2b_title", lang),
        t("negocio.model_b2b_text", lang),
    )
with b3:
    feature_card(
        "🌎",
        t("negocio.model_expand_title", lang),
        t("negocio.model_expand_text", lang),
    )

st.write("")
st.success(t("negocio.cta", lang), icon="🚀")
