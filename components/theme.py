"""
Tema visual y estilos globales de CircuitProIA.
Centraliza paleta, tipografía y CSS para mantener coherencia entre módulos.
"""
import streamlit as st

# ---------------------------------------------------------------------------
# Paleta de marca
# ---------------------------------------------------------------------------
COLORS = {
    "primary": "#0B5FFF",     # Azul eléctrico
    "secondary": "#00C2D1",   # Cian energético
    "accent": "#FFB020",      # Ámbar
    "ink": "#0E1726",         # Texto principal
    "muted": "#5B6B82",       # Texto secundario
    "bg": "#F6F8FC",          # Fondo general
    "card": "#FFFFFF",        # Tarjetas
    "success": "#16A34A",
    "danger": "#DC2626",
    "border": "#E4E9F2",
}


def inject_global_css():
    """Inyecta CSS global. Llamar una vez por página."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}
        .stApp {{
            background: {COLORS['bg']};
        }}
        /* Oculta el menú/footer por defecto para una vista más limpia */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Encabezado de sección */
        .vq-eyebrow {{
            color: {COLORS['primary']};
            font-weight: 700;
            font-size: 0.8rem;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.3rem;
        }}
        .vq-title {{
            color: {COLORS['ink']};
            font-weight: 800;
            font-size: 2.0rem;
            line-height: 1.15;
            margin: 0 0 0.4rem 0;
        }}
        .vq-subtitle {{
            color: {COLORS['muted']};
            font-size: 1.02rem;
            line-height: 1.5;
            margin-bottom: 1.2rem;
        }}

        /* Tarjetas */
        .vq-card {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 1.4rem 1.5rem;
            box-shadow: 0 1px 2px rgba(14,23,38,0.04);
            height: 100%;
        }}
        .vq-card h3 {{
            color: {COLORS['ink']};
            font-size: 1.15rem;
            font-weight: 700;
            margin: 0.4rem 0 0.5rem 0;
        }}
        .vq-card p {{
            color: {COLORS['muted']};
            font-size: 0.94rem;
            line-height: 1.55;
            margin: 0;
        }}
        .vq-icon {{
            font-size: 1.8rem;
        }}

        /* Chips / badges */
        .vq-chip {{
            display: inline-block;
            background: rgba(11,95,255,0.08);
            color: {COLORS['primary']};
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            margin: 0.15rem 0.2rem 0.15rem 0;
        }}
        .vq-chip.cyan {{ background: rgba(0,194,209,0.10); color: #0891a0; }}
        .vq-chip.amber {{ background: rgba(255,176,32,0.14); color: #B57400; }}
        .vq-chip.green {{ background: rgba(22,163,74,0.10); color: {COLORS['success']}; }}

        /* Métrica grande */
        .vq-metric {{
            background: {COLORS['card']};
            border: 1px solid {COLORS['border']};
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            text-align: left;
        }}
        .vq-metric .num {{
            font-size: 1.9rem;
            font-weight: 800;
            color: {COLORS['primary']};
            line-height: 1;
        }}
        .vq-metric .lbl {{
            font-size: 0.85rem;
            color: {COLORS['muted']};
            margin-top: 0.35rem;
        }}

        /* Hero */
        .vq-hero {{
            background: linear-gradient(135deg, {COLORS['primary']} 0%, #1E40AF 55%, #083B9A 100%);
            border-radius: 22px;
            padding: 2.6rem 2.4rem;
            color: white;
        }}
        .vq-hero h1 {{
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.1;
            margin: 0 0 0.6rem 0;
            color: white;
        }}
        .vq-hero p {{
            font-size: 1.12rem;
            color: rgba(255,255,255,0.88);
            max-width: 640px;
            line-height: 1.55;
            margin: 0;
        }}
        .vq-hero .pill {{
            display:inline-block;
            background: rgba(255,255,255,0.16);
            color: #fff;
            font-weight:600;
            font-size:0.8rem;
            padding:0.3rem 0.8rem;
            border-radius:999px;
            margin-bottom:1rem;
        }}

        /* Botones */
        .stButton > button {{
            border-radius: 10px;
            font-weight: 600;
            border: 1px solid {COLORS['border']};
            padding: 0.5rem 1.1rem;
        }}
        .stButton > button[kind="primary"] {{
            background: {COLORS['primary']};
            border-color: {COLORS['primary']};
        }}

        /* Pasos del flujo */
        .vq-step {{
            background:{COLORS['card']};
            border:1px solid {COLORS['border']};
            border-radius:14px;
            padding:1.1rem 1.2rem;
            height:100%;
        }}
        .vq-step .n {{
            width:34px; height:34px; border-radius:50%;
            background:{COLORS['primary']}; color:#fff;
            display:flex; align-items:center; justify-content:center;
            font-weight:700; font-size:0.95rem; margin-bottom:0.6rem;
        }}
        .vq-step h4 {{ margin:0 0 0.3rem 0; color:{COLORS['ink']}; font-size:1.0rem; }}
        .vq-step p {{ margin:0; color:{COLORS['muted']}; font-size:0.88rem; line-height:1.5; }}

        .vq-divider {{ height:1px; background:{COLORS['border']}; margin:1.6rem 0; border:0; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_setup(title: str, icon: str = "None"):
    """Configuración estándar de página + CSS."""
    st.set_page_config(
        page_title=f"CircuitProIA · {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    inject_global_css()
