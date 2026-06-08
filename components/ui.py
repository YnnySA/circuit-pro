"""
Componentes de interfaz reutilizables para CircuitProIA.
Funciones pequeñas y declarativas para mantener las páginas limpias.
"""
import streamlit as st
from components.theme import COLORS
import base64
import os


def section_header(eyebrow: str, title: str, subtitle: str = ""):
    """Encabezado de sección con kicker, título y bajada."""
    html = f"<div class='vq-eyebrow'>{eyebrow}</div><div class='vq-title'>{title}</div>"
    if subtitle:
        html += f"<div class='vq-subtitle'>{subtitle}</div>"
    st.markdown(html, unsafe_allow_html=True)


def feature_card(icon: str, title: str, text: str):
    """Tarjeta de característica con ícono."""
    st.markdown(
        f"""
        <div class='vq-card'>
            <div class='vq-icon'>{icon}</div>
            <h3>{title}</h3>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(num: str, label: str):
    """Métrica visual destacada."""
    st.markdown(
        f"<div class='vq-metric'><div class='num'>{num}</div><div class='lbl'>{label}</div></div>",
        unsafe_allow_html=True,
    )


def chip(text: str, variant: str = ""):
    """Devuelve HTML de un chip/badge. variant: '', 'cyan', 'amber', 'green'."""
    cls = f"vq-chip {variant}".strip()
    return f"<span class='{cls}'>{text}</span>"


def chips(items, variant: str = ""):
    """Renderiza una fila de chips."""
    st.markdown("".join(chip(i, variant) for i in items), unsafe_allow_html=True)


def step_card(n: int, title: str, text: str):
    """Tarjeta de paso numerado para flujos."""
    st.markdown(
        f"""
        <div class='vq-step'>
            <div class='n'>{n}</div>
            <h4>{title}</h4>
            <p>{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def divider():
    st.markdown("<hr class='vq-divider'/>", unsafe_allow_html=True)

def _logo_b64():
    """Lee el logo y lo devuelve como base64 para incrustarlo en HTML."""
    with open("assets/icon_192.png", "rb") as f:
        return base64.b64encode(f.read()).decode()
    
def sidebar_brand():
    """Marca y navegación contextual en la barra lateral."""
    logo = _logo_b64()
    st.sidebar.markdown(
        f"""
        <div style='display:flex; align-items:flex-start; gap:0.5rem; padding:0.4rem 0 0.8rem 0;'>
            <img src='data:image/png;base64,{logo}' style='width:32px; height:32px; object-fit:contain;'/>
            <div>
                <span style='font-size:1.5rem; font-weight:800; color:{COLORS['primary']};'>CircuitProIA</span><br/>
                <span style='font-size:0.78rem; color:{COLORS['muted']};'>IA aplicada a educación e industria</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.sidebar.markdown("---")


def hero(pill: str, title: str, subtitle: str):
    st.markdown(
        f"""
        <div class='vq-hero'>
            <span class='pill'>{pill}</span>
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
