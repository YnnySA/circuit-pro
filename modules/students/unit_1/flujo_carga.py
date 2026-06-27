"""
Simulador de Flujo de Carga — Red de 2 Buses
Método de Gauss-Seidel | V₁ = V₂ + Z·I | Sistema en valores por unidad [pu]
Desarrollado por Dr. Maykop Pérez Martínez — Universidad de Concepción (UdeC)
Departamento de Ingeniería Eléctrica

Replica fiel a la aplicación de referencia:
- Layout: columna izquierda parámetros / columna derecha diagramas
- Diagrama del Circuito: Nodo2(izq) → Z_línea → Nodo1(der) con tierra, capacitor, carga
- Diagrama Fasorial: fondo oscuro, 4 vectores V₁, V₂, ΔV=Z·I, I
- Resultados: tabla completa con forma polar + rectangular
- Relaciones Fundamentales al pie
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ── PALETA OSCURA (fiel a la referencia) ────────────────────────────────────
BG      = "#0d1b2a"
PANEL   = "#112240"
BORDER  = "#1e3a5f"
YELLOW  = "#f5c518"
CYAN    = "#00d4d4"
ORANGE  = "#ff6b35"
GREEN   = "#2ecc71"
PURPLE  = "#9b59b6"
SALMON  = "#e07b7b"
WHITE   = "#e8eaf6"
GRAY    = "#7f8c8d"
RED     = "#e74c3c"

# Colores de vectores fasorial (exactos de la referencia)
COL_V1  = "#e74c3c"   # rojo
COL_V2  = "#e07b7b"   # salmón
COL_DV  = "#00d4d4"   # turquesa
COL_I   = "#00bfff"   # cian

# ── CSS GLOBAL ───────────────────────────────────────────────────────────────
def _inject_css():
    st.markdown(f"""
    <style>
    .stApp, [data-testid="stAppViewContainer"] {{
        background-color: {BG};
        color: {WHITE};
    }}
    [data-testid="stSidebar"] {{ background-color: {PANEL}; }}
    .fc-panel {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }}
    .fc-panel-title {{
        color: {YELLOW};
        font-size: 1rem;
        font-weight: 700;
        margin-bottom: 10px;
        display: flex; align-items: center; gap: 6px;
    }}
    .fc-result-row {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-bottom: 6px;
    }}
    .fc-result-cell {{
        background: #0d1b2a;
        border-radius: 6px;
        padding: 8px 10px;
        border-left: 3px solid {CYAN};
    }}
    .fc-result-label {{
        font-size: 0.7rem; color: {GRAY}; margin-bottom: 2px;
    }}
    .fc-result-polar {{
        font-size: 0.92rem; font-weight: 700; color: {YELLOW};
    }}
    .fc-result-rect {{
        font-size: 0.78rem; color: {CYAN};
    }}
    .fc-rel-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
    }}
    @media (max-width:700px) {{ .fc-rel-grid {{ grid-template-columns: 1fr 1fr; }} }}
    .fc-rel-card {{
        background: {PANEL};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }}
    .fc-rel-name  {{ font-size:0.72rem; color:{GRAY}; margin-bottom:4px; }}
    .fc-rel-eq    {{ font-size:0.95rem; font-weight:700; color:{YELLOW}; }}
    label, .stSlider label, .stRadio label {{
        color: {WHITE} !important;
        font-size: 0.82rem !important;
    }}
    .fc-badge-ok  {{ background:#1a4731; color:#2ecc71;
                     border-radius:20px; padding:3px 14px;
                     font-weight:700; font-size:0.82rem; display:inline-block; }}
    .fc-badge-err {{ background:#4a1a1a; color:#e74c3c;
                     border-radius:20px; padding:3px 14px;
                     font-weight:700; font-size:0.82rem; display:inline-block; }}
    .fc-main-title {{
        text-align:center; font-size:1.6rem; font-weight:800;
        color:{YELLOW}; margin-bottom:2px;
    }}
    .fc-subtitle {{ text-align:center; color:{GRAY}; font-size:0.8rem; margin-bottom:16px; }}
    </style>
    """, unsafe_allow_html=True)


# ── MATEMÁTICA ───────────────────────────────────────────────────────────────
def _cpolar(r, deg):
    return complex(r * np.cos(np.radians(deg)), r * np.sin(np.radians(deg)))

def _fPol(c, d=4):
    return f"{abs(c):.{d}f} ∠ {np.degrees(np.angle(c)):.2f}°"

def _fRect(c, d=4):
    s = "+" if c.imag >= 0 else "−"
    return f"{c.real:.{d}f} {s} j{abs(c.imag):.{d}f} pu"

def solve(R, X, Pload, Qload, Qcap, V2mag, V2ang):
    S1 = complex(-Pload, Qcap - Qload)
    V2 = _cpolar(V2mag, V2ang)
    Z  = complex(R, X)
    if abs(Z) < 1e-9:
        I  = np.conj(S1) / np.conj(V2) if abs(V2) > 1e-9 else 0+0j
        S2 = V2 * np.conj(I)
        return dict(ok=True, iters=0, V1=V2, I=I, S2=S2,
                    Sloss=0+0j, V2=V2, dV=0+0j, Z=Z,
                    S_from=S2, S_to=S2)
    Y  = 1 / Z; Yn = -Y
    V1 = _cpolar(V2mag, 0)
    ok = False; iters = 0
    for k in range(3000):
        rhs    = np.conj(S1) / np.conj(V1) - Yn * V2
        V1_new = rhs / Y
        err    = abs(V1_new - V1)
        V1     = V1_new; iters = k + 1
        if err < 1e-10:
            ok = True; break
    I      = (V1 - V2) / Z
    dV     = Z * I
    S2     = V2 * np.conj(I)
    I2     = abs(I) ** 2
    Sloss  = complex(I2 * R, I2 * X)
    S_from = V2 * np.conj(I)
    S_to   = V1 * np.conj(I)
    return dict(ok=ok, iters=iters, V1=V1, I=I, S2=S2,
                Sloss=Sloss, V2=V2, dV=dV, Z=Z,
                S_from=S_from, S_to=S_to)


# ── DIAGRAMA DEL CIRCUITO ────────────────────────────────────────────────────
def _fig_circuito(r, R, X, Qcap):
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    dV = r["dV"]; S_from = r["S_from"]; S_to = r["S_to"]

    fig = go.Figure()
    N2x, N1x, Cy = 1.5, 8.5, 4.0
    ht = 1.8

    def ann(x, y, text, color=WHITE, size=11, xsh=0, ysh=0, anchor="center"):
        fig.add_annotation(x=x, y=y, text=text, showarrow=False,
                           font=dict(color=color, size=size),
                           xanchor=anchor, yanchor="middle",
                           xshift=xsh, yshift=ysh,
                           bgcolor="rgba(0,0,0,0)")

    def line(x0, y0, x1, y1, color=GRAY, width=2):
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=color, width=width))

    # Cable
    line(N2x, Cy, N1x, Cy, color="#4a6fa5", width=3)

    # Barras
    line(N2x, Cy-ht, N2x, Cy+ht, color=ORANGE, width=6)
    line(N1x, Cy-ht, N1x, Cy+ht, color=RED,    width=6)

    # Títulos nodos
    ann(N2x, Cy+ht+0.5, "<b>Nodo 2</b>", ORANGE, size=13)
    ann(N1x, Cy+ht+0.5, "<b>Nodo 1</b>", RED,    size=13)

    # Generador
    theta = np.linspace(0, 2*np.pi, 60)
    Gx, Gy, Gr = N2x-1.6, Cy, 0.5
    fig.add_trace(go.Scatter(
        x=Gx+Gr*np.cos(theta), y=Gy+Gr*np.sin(theta),
        fill="toself", fillcolor=PANEL,
        line=dict(color=YELLOW, width=2.5),
        mode="lines", showlegend=False, hoverinfo="skip",
    ))
    ann(Gx, Gy+0.15, "<b>~</b>", YELLOW, size=20)
    ann(Gx-0.15, Gy-0.25, "+", WHITE, size=11)
    ann(Gx-0.15, Gy+0.25, "−", WHITE, size=11)
    line(Gx+Gr, Gy, N2x, Cy, color=YELLOW, width=2)

    # Tierra Nodo2
    line(N2x, Cy-ht, N2x, Cy-ht-0.3, color=CYAN, width=2)
    for w, yy in [(0.5,0),(0.35,-0.18),(0.2,-0.34)]:
        yb = Cy-ht-0.3-yy
        line(N2x-w/2, yb, N2x+w/2, yb, color=CYAN, width=2)

    # Caja Z_línea
    Zmx = (N2x+N1x)/2; Zmy = Cy; Zw, Zh = 1.3, 0.9
    fig.add_shape(type="rect", x0=Zmx-Zw, y0=Zmy-Zh, x1=Zmx+Zw, y1=Zmy+Zh,
                  fillcolor="#1a2f4a", line=dict(color=YELLOW, width=2))
    ann(Zmx, Zmy+0.35, "Z<sub>línea</sub> = R + jX", YELLOW, size=11)
    sign = "+" if X >= 0 else "−"
    ann(Zmx, Zmy-0.25, f"<b>{R:.2f} {sign} j{abs(X):.2f} pu</b>", CYAN, size=13)
    ann(Zmx, Zmy-Zh-0.4, "ΔV<sub>línea</sub> = <i>I</i> · Z", GRAY, size=10)
    ann(Zmx, Zmy-Zh-0.85, f"{_fPol(dV, 4)}", GREEN, size=10)

    # Corriente I
    fig.add_annotation(
        ax=N2x+0.3, ay=Cy+0.55, x=N1x-0.3, y=Cy+0.55,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=CYAN,
        text=f"<b><i>I</i> = {_fPol(I, 4)}</b>",
        font=dict(color=CYAN, size=11),
        xanchor="center", yanchor="bottom", yshift=4,
    )

    # Flujos S₂ y S₂₁
    S2s = "+" if S_from.imag >= 0 else "−"
    ann((N2x+Zmx)/2, Cy+0.18, "S₂ =", GRAY, size=9)
    ann((N2x+Zmx)/2, Cy-0.18,
        f"{S_from.real:.3f} {S2s} j{abs(S_from.imag):.3f} pu", WHITE, size=9)
    fig.add_annotation(
        ax=N2x+0.2, ay=Cy+0.05, x=Zmx-Zw-0.1, y=Cy+0.05,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor=WHITE, text="",
    )
    S21s = "+" if S_to.imag >= 0 else "−"
    ann((Zmx+N1x)/2, Cy+0.18, "S₂₁ =", GRAY, size=9)
    ann((Zmx+N1x)/2, Cy-0.18,
        f"{S_to.real:.3f} {S21s} j{abs(S_to.imag):.3f} pu", WHITE, size=9)
    fig.add_annotation(
        ax=Zmx+Zw+0.1, ay=Cy+0.05, x=N1x-0.2, y=Cy+0.05,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor=WHITE, text="",
    )

    # Tensiones debajo de barras
    ann(N2x, Cy-ht-1.2, "V₂ =", GRAY, size=10)
    ann(N2x, Cy-ht-1.65, f"<b>{_fPol(V2, 2)}</b>", ORANGE, size=11)
    ann(N1x, Cy-ht-1.2, "V₁ =", GRAY, size=10)
    ann(N1x, Cy-ht-1.65, f"<b>{_fPol(V1, 4)}</b>", RED, size=11)

    # Capacitor Qc (Nodo1, arriba-derecha)
    Ccx = N1x+1.2; Ccy = Cy+ht+0.6
    line(N1x, Cy+ht, N1x, Ccy-0.25, color=CYAN, width=2)
    line(N1x, Ccy-0.25, Ccx, Ccy-0.25, color=CYAN, width=2)
    line(Ccx, Ccy-0.25, Ccx, Ccy+0.05, color=CYAN, width=2)
    for dy in [0.05, 0.25]:
        line(Ccx-0.4, Ccy+dy, Ccx+0.4, Ccy+dy, color=CYAN, width=3)
    ann(Ccx, Ccy+0.65, f"Q<sub>C</sub> = {Qcap:.2f} pu", CYAN, size=11)
    line(Ccx, Ccy+0.3, Ccx, Ccy+0.6, color=CYAN, width=2)
    for w, dy in [(0.4,0),(0.28,0.15),(0.16,0.3)]:
        line(Ccx-w/2, Ccy+0.6+dy, Ccx+w/2, Ccy+0.6+dy, color=CYAN, width=2)

    # Carga PL+jQL (Nodo1, derecha)
    Lx0, Lx1 = N1x+0.2, N1x+1.7
    Ly0, Ly1 = Cy-0.8, Cy+0.45
    line(N1x, Cy, Lx0, Cy, color=PURPLE, width=2)
    fig.add_shape(type="rect", x0=Lx0, y0=Ly0, x1=Lx1, y1=Ly1,
                  fillcolor="#1a1040", line=dict(color=PURPLE, width=2))
    ann((Lx0+Lx1)/2, (Ly0+Ly1)/2+0.18,
        "P<sub>L</sub> + jQ<sub>L</sub>", PURPLE, size=11)
    ann((Lx0+Lx1)/2, (Ly0+Ly1)/2-0.2,
        f"<b>{r['S2'].real:.2f} + j{r['S2'].imag:.2f} pu</b>", WHITE, size=11)

    # Tierra Nodo1
    line(N1x, Cy-ht, N1x, Cy-ht-0.3, color=CYAN, width=2)
    for w, yy in [(0.5,0),(0.35,-0.18),(0.2,-0.34)]:
        yb = Cy-ht-0.3-yy
        line(N1x-w/2, yb, N1x+w/2, yb, color=CYAN, width=2)

    fig.update_layout(
        paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        xaxis=dict(range=[-0.5, 11], showgrid=False, zeroline=False,
                   showticklabels=False),
        yaxis=dict(range=[0.5, 7.2], showgrid=False, zeroline=False,
                   showticklabels=False, scaleanchor="x", scaleratio=0.9),
        margin=dict(l=10, r=10, t=10, b=10),
        height=420, showlegend=False,
    )
    return fig


# ── DIAGRAMA FASORIAL ────────────────────────────────────────────────────────
def _fig_fasorial(r):
    V1 = r["V1"]; V2 = r["V2"]; dV = r["dV"]; I = r["I"]
    fig = go.Figure()

    Iscale = max(abs(V1), abs(V2)) * 0.7 / (abs(I) + 1e-9)
    Iplot  = I * Iscale

    def vec(x0, y0, x1, y1, color):
        fig.add_annotation(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowwidth=2.5,
            arrowcolor=color, arrowsize=1.1, text="",
        )
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(color=color, width=2),
            showlegend=False, hoverinfo="skip",
        ))

    vec(0, 0, V2.real, V2.imag, COL_V2)
    vec(0, 0, V1.real, V1.imag, COL_V1)
    vec(V2.real, V2.imag, V1.real, V1.imag, COL_DV)
    vec(0, 0, Iplot.real, Iplot.imag, COL_I)

    def label(x, y, text, color, xsh=10, ysh=0):
        fig.add_annotation(x=x, y=y, text=f"<b>{text}</b>",
                           showarrow=False, font=dict(color=color, size=12),
                           xshift=xsh, yshift=ysh)

    label(V2.real, V2.imag, "V₂", COL_V2)
    label(V1.real, V1.imag, "V₁", COL_V1)
    label((V2.real+V1.real)/2, (V2.imag+V1.imag)/2, "ΔV", COL_DV, xsh=10, ysh=8)
    label(Iplot.real, Iplot.imag, "I", COL_I)

    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers",
        marker=dict(size=8, color=WHITE),
        showlegend=False, hoverinfo="skip",
    ))

    for col, name in [(COL_V1,"V₁"),(COL_V2,"V₂"),(COL_DV,"ΔV = Z·I"),(COL_I,"I")]:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=col),
            name=name, showlegend=True,
        ))

    m = max(abs(V1), abs(V2), abs(Iplot)) * 1.4 + 0.05
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG,
        xaxis=dict(range=[-m, m], zeroline=True, zerolinecolor="#2a4a7f",
                   zerolinewidth=1.5, showgrid=True, gridcolor="#1a3050",
                   tickfont=dict(color=GRAY),
                   title=dict(text="Re", font=dict(color=WHITE, size=12))),
        yaxis=dict(range=[-m*0.8, m*0.8], zeroline=True, zerolinecolor="#2a4a7f",
                   zerolinewidth=1.5, showgrid=True, gridcolor="#1a3050",
                   tickfont=dict(color=GRAY),
                   title=dict(text="Im", font=dict(color=WHITE, size=12)),
                   scaleanchor="x", scaleratio=1),
        margin=dict(l=40, r=20, t=20, b=40),
        height=360, showlegend=True,
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(color=WHITE, size=12),
                    bgcolor="rgba(0,0,0,0)"),
        font=dict(color=WHITE),
    )
    return fig


# ── RESULTADOS ───────────────────────────────────────────────────────────────
def _resultados_html(r):
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    S2 = r["S2"]; Sl = r["Sloss"]; dV = r["dV"]
    eta = S2.real / (S2.real + Sl.real + 1e-12) * 100

    badge = (f'<span class="fc-badge-ok">✓ Gauss-Seidel — {r["iters"]} iter</span>'
             if r["ok"] else
             '<span class="fc-badge-err">✗ No convergió</span>')

    def row(label, polar, rect, accent=CYAN):
        return f"""
        <div class="fc-result-cell" style="border-left-color:{accent}">
          <div class="fc-result-label">{label}</div>
          <div class="fc-result-polar">{polar}</div>
          <div class="fc-result-rect">{rect}</div>
        </div>"""

    html = f"""
    <div style="margin-bottom:8px">{badge}</div>
    <div class="fc-result-row">
      {row("Tensión Bus 1 (Slack) — V₁", _fPol(V1,4), _fRect(V1,4), RED)}
      {row("Corriente de línea — I", _fPol(I,4), _fRect(I,4), CYAN)}
    </div>
    <div class="fc-result-row">
      {row("Pot. Activa Bus 2→1 — P₂₁", f"{S2.real:.5f} pu", "Re(V₁·I*)", ORANGE)}
      {row("Pot. Reactiva Bus 2→1 — Q₂₁", f"{S2.imag:.5f} pu", "Im(V₁·I*)", PURPLE)}
    </div>
    <div class="fc-result-row">
      {row("Pot. Aparente — S₂", _fPol(S2,4), _fRect(S2,4), YELLOW)}
      {row("Caída de tensión — ΔV = Z·I", _fPol(dV,4), _fRect(dV,4), GREEN)}
    </div>
    <div class="fc-result-row">
      {row("Pérdidas activas — P_loss = |I|²·R", f"{Sl.real:.6f} pu", f"|I|²={abs(I)**2:.5f}", SALMON)}
      {row("Pérdidas reactivas — Q_loss = |I|²·X", f"{Sl.imag:.6f} pu", f"η = {eta:.2f}%", SALMON)}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ── RELACIONES FUNDAMENTALES ─────────────────────────────────────────────────
def _relaciones_html():
    rels = [
        ("TENSIÓN DE ENVÍO",     "V₁ = V₂ + Z · I"),
        ("POTENCIA RECIBIDA",    "S₂₁ = V₁ · I* = P₂₁ + jQ₂₁"),
        ("CORRIENTE DE LÍNEA",   "I = S₂₁* / V₁* = (V₂−V₁) / Z"),
        ("PÉRDIDAS EN LA LÍNEA", "S loss = |I|² · Z = P loss + jQ loss"),
        ("ADMITANCIA DE LÍNEA",  "Y = 1/Z = G + jB"),
        ("BALANCE DE POTENCIA",  "S gen = S carga + S loss"),
    ]
    cards = "".join(f"""
        <div class="fc-rel-card">
          <div class="fc-rel-name">{name}</div>
          <div class="fc-rel-eq">{eq}</div>
        </div>""" for name, eq in rels)
    st.markdown(f'<div class="fc-rel-grid">{cards}</div>', unsafe_allow_html=True)


# ── RENDER PRINCIPAL ─────────────────────────────────────────────────────────
def render():
    _inject_css()

    st.markdown('<div class="fc-main-title">⚡ Flujo de Carga — Red de 2 Buses</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="fc-subtitle">'
        'Método de Gauss Seidel &nbsp;|&nbsp; <b>V₁ = V₂ + Z·I</b> &nbsp;|&nbsp; '
        'Sistema en valores por unidad [pu]'
        '</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="fc-panel" style="display:flex;align-items:center;gap:16px;padding:12px 16px">
      <div>
        <div style="color:{WHITE};font-size:0.82rem;margin-bottom:2px">Desarrollado por:</div>
        <div style="color:{WHITE};font-weight:700;font-size:1rem">Dr. Maykop Pérez Martínez</div>
        <div style="color:{CYAN};font-size:0.85rem">Universidad de Concepción (UdeC)</div>
        <div style="color:{GRAY};font-size:0.78rem">Departamento de Ingeniería Eléctrica</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Presets pendientes
    for src, dst in [
        ("_fc_R_p","fc_R"),("_fc_X_p","fc_X"),("_fc_P_p","fc_P"),
        ("_fc_Q_p","fc_Q"),("_fc_Qc_p","fc_Qc"),("_fc_V_p","fc_V"),("_fc_A_p","fc_A"),
    ]:
        if src in st.session_state:
            st.session_state[dst] = st.session_state.pop(src)

    col_left, col_right = st.columns([1, 2], gap="medium")

    with col_left:
        st.markdown(f'<div class="fc-panel-title">🔧 Parámetros de la Red</div>',
                    unsafe_allow_html=True)
        st.markdown(f"<span style='color:{CYAN};font-size:0.8rem'>"
                    "Línea de transmisión:<br>Z = R + jX [pu] &nbsp;|&nbsp; Caída de tensión: ΔV = Z · I"
                    "</span>", unsafe_allow_html=True)
        R = st.slider("R — Resistencia [pu]", 0.00, 0.50,
                      float(st.session_state.get("fc_R", 0.20)), 0.01, key="fc_R")
        X = st.slider("X — Reactancia [pu]",  0.00, 1.00,
                      float(st.session_state.get("fc_X", 0.74)), 0.01, key="fc_X")

        st.markdown(f"<span style='color:{CYAN};font-size:0.8rem'>"
                    "Carga en Bus 1:<br>S<sub>carga</sub> = P<sub>L</sub> + jQ<sub>L</sub> [pu]"
                    "<br>Compensación: Q<sub>C</sub> (banco capacitivo)"
                    "</span>", unsafe_allow_html=True)
        Pload = st.slider("Pₗ — Potencia activa [pu]",   0.00, 2.00,
                          float(st.session_state.get("fc_P", 1.35)), 0.01, key="fc_P")
        Qload = st.slider("Qₗ — Potencia reactiva [pu]", -1.00, 2.00,
                          float(st.session_state.get("fc_Q", 1.00)), 0.01, key="fc_Q")
        Qcap  = st.slider("Qc — Banco capacitivo [pu]",  0.00, 2.00,
                          float(st.session_state.get("fc_Qc", 1.00)), 0.01, key="fc_Qc")

        st.markdown(f"<span style='color:{CYAN};font-size:0.8rem'>"
                    "Bus 2 (barra slack):<br>V₂ = |V₂| ∠ δ₂ [pu]"
                    "<br>Referencia angular del sistema"
                    "</span>", unsafe_allow_html=True)
        V2mag = st.slider("|V₂| — Módulo [pu]", 0.80, 1.20,
                          float(st.session_state.get("fc_V", 0.98)), 0.01, key="fc_V")
        V2ang = st.slider("δ₂ — Ángulo [°]",   -30.0, 10.0,
                          float(st.session_state.get("fc_A", 0.00)), 0.5,  key="fc_A")

        st.markdown("---")
        st.markdown(f"<span style='color:{YELLOW};font-size:0.8rem;font-weight:700'>"
                    "Casos predefinidos:</span>", unsafe_allow_html=True)
        presets = {
            "Resistivo":  dict(R=0.00,X=0.50,P=0.50,Q=1.00,Qc=1.00,V=1.00,A=0.0),
            "Inductivo":  dict(R=0.05,X=0.30,P=0.80,Q=0.60,Qc=0.00,V=0.95,A=0.0),
            "Referencia": dict(R=0.20,X=0.74,P=1.35,Q=1.00,Qc=1.00,V=0.98,A=0.0),
            "Alta carga": dict(R=0.10,X=0.60,P=1.20,Q=0.90,Qc=0.80,V=0.90,A=-5.0),
            "Capacitivo": dict(R=0.02,X=0.40,P=0.40,Q=-0.30,Qc=0.50,V=1.00,A=0.0),
        }
        c1, c2 = st.columns(2)
        for i, (name, vals) in enumerate(presets.items()):
            col = c1 if i % 2 == 0 else c2
            if col.button(name, key=f"fc_pre_{i}", use_container_width=True):
                for k2, v2 in [("R",vals["R"]),("X",vals["X"]),("P",vals["P"]),
                               ("Q",vals["Q"]),("Qc",vals["Qc"]),("V",vals["V"]),("A",vals["A"])]:
                    st.session_state[f"_fc_{k2}_p"] = float(v2)
                st.rerun()

    r = solve(R, X, Pload, Qload, Qcap, V2mag, V2ang)

    with col_right:
        st.markdown(f'<div class="fc-panel-title">🔌 Diagrama del Circuito</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(_fig_circuito(r, R, X, Qcap),
                        use_container_width=True, key="fc_circ")
        st.markdown(f'<div class="fc-panel-title">📐 Diagrama Fasorial</div>',
                    unsafe_allow_html=True)
        st.plotly_chart(_fig_fasorial(r),
                        use_container_width=True, key="fc_fas")

    st.markdown("---")
    st.markdown(f'<div class="fc-panel-title">📊 Resultados</div>',
                unsafe_allow_html=True)
    _resultados_html(r)

    st.markdown("---")
    st.markdown(f'<div class="fc-panel-title">📐 Relaciones Fundamentales</div>',
                unsafe_allow_html=True)
    _relaciones_html()
