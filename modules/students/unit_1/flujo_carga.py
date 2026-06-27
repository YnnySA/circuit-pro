"""
Simulador de Flujo de Carga — Red de 2 Buses
Método de Gauss-Seidel | Valores por unidad [pu]
Desarrollado por Dr. Maykop Perez Martinez
Universidad de Concepción - Depto. Ingeniería Eléctrica

100% Python + Streamlit + Plotly (sin HTML embebido)
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# COLORES Y LAYOUT BASE (consistente con graficos.py)
# ---------------------------------------------------------------------------
_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="#f8f9fa",
    font=dict(color="#333333", family="Segoe UI, sans-serif", size=12),
    margin=dict(l=48, r=24, t=40, b=40),
)
_C = {
    "V1":     "#1d3557",
    "V2":     "#457b9d",
    "I":      "#e63946",
    "Z":      "#2d6a4f",
    "P":      "#e63946",
    "Q":      "#6d28d9",
    "S":      "#1d3557",
    "loss":   "#f4a261",
    "grid":   "#e0e0e0",
    "arrow":  "#1d3557",
    "bus1":   "#1d3557",
    "bus2":   "#457b9d",
    "gen":    "#2d6a4f",
    "load":   "#e63946",
    "cap":    "#059669",
    "wire":   "#555555",
}


# ---------------------------------------------------------------------------
# TARJETAS DE MÉTRICAS (igual que graficos.py)
# ---------------------------------------------------------------------------
def _metric_cards(items, accent="#1d3557"):
    cards_html = ""
    for label, value, unit in items:
        cards_html += f"""
        <div class="mc">
          <div class="mc-label">{label}</div>
          <div class="mc-value">{value}<span class="mc-unit"> {unit}</span></div>
        </div>"""
    html = f"""
    <style>
      .mc-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px; margin-bottom: 10px;
      }}
      @media (max-width: 600px) {{ .mc-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
      .mc {{
        background: #f0f2f6; border-radius: 8px;
        padding: 10px 12px 8px;
        border-left: 3px solid {accent};
      }}
      .mc-label {{
        font-size: 0.72rem; color: #6b7280; font-weight: 500;
        text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 3px;
      }}
      .mc-value {{
        font-size: 1.05rem; font-weight: 700; color: #1f2937;
        white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
      }}
      .mc-unit {{
        font-size: 0.78rem; font-weight: 400; color: #6b7280; margin-left: 3px;
      }}
    </style>
    <div class="mc-grid">{cards_html}</div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# MATEMÁTICA DE NÚMEROS COMPLEJOS (numpy)
# ---------------------------------------------------------------------------
def _cpolar(r, deg):
    """Complejo desde módulo y ángulo en grados."""
    return complex(r * np.cos(np.radians(deg)), r * np.sin(np.radians(deg)))


def _fN(x, d=4):
    if not np.isfinite(x):
        return "∞"
    return f"{x:.{d}f}"


def _fPol(c, d=4):
    return f"{abs(c):.{d}f} ∠ {np.degrees(np.angle(c)):.2f}°"


def _fC(c, d=4):
    s = "+" if c.imag >= 0 else "−"
    return f"{c.real:.{d}f} {s} j{abs(c.imag):.{d}f}"


# ---------------------------------------------------------------------------
# SOLUCIONADOR GAUSS-SEIDEL
# ---------------------------------------------------------------------------
def solve(R, X, Pload, Qload, Qcap, V2mag, V2ang):
    """
    Red de 2 buses:
      Bus 1: slack (V1 = incógnita)
      Bus 2: PQ  (V2 = dato, carga P+jQ, compensación jQcap)

    Retorna dict con todos los resultados.
    """
    S1 = complex(-Pload, Qcap - Qload)   # potencia inyectada en bus 2
    V2 = _cpolar(V2mag, V2ang)
    Z  = complex(R, X)

    if abs(Z) < 1e-6:
        I     = np.conj(S1) / np.conj(V2)
        S2    = V2 * np.conj(I)
        return dict(ok=True, iters=0, V1=V2, I=I, S2=S2,
                    Sloss=0+0j, V2=V2, dV=0+0j)

    Y  = 1 / Z
    Yn = -Y

    V1 = _cpolar(V2mag, 0)
    ok = False
    iters = 0
    for k in range(3000):
        rhs  = np.conj(S1) / np.conj(V1) - Yn * V2
        V1_new = rhs / Y
        err  = abs(V1_new - V1)
        V1   = V1_new
        iters = k + 1
        if err < 1e-10:
            ok = True
            break

    I     = (V1 - V2) / Z
    dV    = Z * I
    S2    = V2 * np.conj(I)
    I2    = abs(I) ** 2
    Sloss = complex(I2 * R, I2 * X)
    return dict(ok=ok, iters=iters, V1=V1, I=I, S2=S2,
                Sloss=Sloss, V2=V2, dV=dV)


# ---------------------------------------------------------------------------
# GRÁFICO 1: DIAGRAMA UNIFILAR (SVG vía Plotly shapes + annotations)
# ---------------------------------------------------------------------------
def _grafico_unifilar(r):
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    V1m = abs(V1); V1a = np.degrees(np.angle(V1))
    V2m = abs(V2); V2a = np.degrees(np.angle(V2))
    Im  = abs(I);  Ia  = np.degrees(np.angle(I))

    fig = go.Figure()

    # Línea de transmisión (cable)
    fig.add_shape(type="line", x0=2.2, y0=2, x1=5.8, y1=2,
                  line=dict(color=_C["wire"], width=4))

    # Generador (Bus 1) - círculo izquierdo
    theta = np.linspace(0, 2 * np.pi, 60)
    fig.add_trace(go.Scatter(
        x=1.0 + 0.55 * np.cos(theta), y=2.0 + 0.55 * np.sin(theta),
        fill="toself", fillcolor="#e8f4f8",
        line=dict(color=_C["gen"], width=2.5),
        mode="lines", showlegend=False, hoverinfo="skip",
    ))
    fig.add_annotation(x=1.0, y=2.0, text="~", showarrow=False,
                       font=dict(size=22, color=_C["gen"], weight="bold"))
    # Bus 1 vertical
    fig.add_shape(type="line", x0=2.2, y0=0.9, x1=2.2, y1=3.1,
                  line=dict(color=_C["bus1"], width=6))

    # Carga (Bus 2) - rectángulo derecho
    fig.add_shape(type="rect", x0=5.8, y0=1.4, x1=6.8, y1=2.6,
                  fillcolor="#fff3e0", line=dict(color=_C["load"], width=2))
    fig.add_annotation(x=6.3, y=2.0, text="P+jQ", showarrow=False,
                       font=dict(size=11, color=_C["load"], weight="bold"))
    # Bus 2 vertical
    fig.add_shape(type="line", x0=5.8, y0=0.9, x1=5.8, y1=3.1,
                  line=dict(color=_C["bus2"], width=6))

    # Banco de capacitores (Bus 2, abajo)
    fig.add_shape(type="line", x0=5.8, y0=0.9, x1=5.8, y1=0.5,
                  line=dict(color=_C["cap"], width=2))
    for yy in [0.38, 0.28]:
        fig.add_shape(type="line", x0=5.4, y0=yy, x1=6.2, y1=yy,
                      line=dict(color=_C["cap"], width=3))

    # Etiquetas de tensión sobre las barras
    fig.add_annotation(
        x=2.2, y=3.3,
        text=f"<b>Bus 1 (Slack)</b><br>V₁={_fN(V1m,4)} ∠{V1a:.2f}° pu",
        showarrow=False, font=dict(color=_C["bus1"], size=11),
        align="center", bgcolor="rgba(240,248,255,0.85)",
        bordercolor=_C["bus1"], borderwidth=1, borderpad=4,
    )
    fig.add_annotation(
        x=5.8, y=3.3,
        text=f"<b>Bus 2 (PQ)</b><br>V₂={_fN(V2m,4)} ∠{V2a:.2f}° pu",
        showarrow=False, font=dict(color=_C["bus2"], size=11),
        align="center", bgcolor="rgba(232,244,253,0.85)",
        bordercolor=_C["bus2"], borderwidth=1, borderpad=4,
    )

    # Corriente sobre el cable
    fig.add_annotation(
        x=4.0, y=2.35,
        text=f"I = {_fN(Im,4)} ∠{Ia:.2f}° pu",
        showarrow=True, arrowhead=2, arrowcolor=_C["I"],
        ax=3.2, ay=2.35, axref="x", ayref="y",
        font=dict(color=_C["I"], size=11, weight="bold"),
        bgcolor="rgba(255,255,255,0.85)",
    )

    # Impedancia Z sobre el cable
    fig.add_annotation(
        x=4.0, y=1.6,
        text=f"Z = {_fN(abs(complex(r.get('R', 0), r.get('X', 0))),3)} pu",
        showarrow=False, font=dict(color=_C["Z"], size=11),
        bgcolor="rgba(255,255,255,0.75)",
    )

    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Diagrama Unifilar — Red de 2 Buses", font=dict(size=13)),
        xaxis=dict(range=[0, 8], showgrid=False, zeroline=False,
                   showticklabels=False),
        yaxis=dict(range=[0, 4], showgrid=False, zeroline=False,
                   showticklabels=False, scaleanchor="x", scaleratio=1),
        height=320,
    )
    return fig


# ---------------------------------------------------------------------------
# GRÁFICO 2: DIAGRAMA FASORIAL (V1, V2, dV, I)
# ---------------------------------------------------------------------------
def _grafico_fasorial(r):
    V1 = r["V1"]; V2 = r["V2"]; dV = r["dV"]; I = r["I"]
    fig = go.Figure()

    def _arrow(x0, y0, x1, y1, color, label, xsh=0, ysh=8):
        fig.add_annotation(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowwidth=2.2,
            arrowcolor=color, arrowsize=1.0,
            text=label, font=dict(color=color, size=11),
            xanchor="center", yanchor="bottom",
            xshift=xsh, yshift=ysh,
        )

    _arrow(0, 0, V2.real, V2.imag, _C["V2"],
           f"V₂={abs(V2):.4f}∠{np.degrees(np.angle(V2)):.2f}°")
    _arrow(0, 0, V1.real, V1.imag, _C["V1"],
           f"V₁={abs(V1):.4f}∠{np.degrees(np.angle(V1)):.2f}°")
    _arrow(V2.real, V2.imag, V1.real, V1.imag, _C["Z"],
           f"ΔV={abs(dV):.4f}∠{np.degrees(np.angle(dV)):.2f}°")

    # Corriente escalada para visibilidad
    Iscale = max(abs(V1), abs(V2)) * 0.6 / (abs(I) + 1e-9)
    Iplot  = I * Iscale
    _arrow(0, 0, Iplot.real, Iplot.imag, _C["I"],
           "I (escalado)", ysh=-14)

    m = max(abs(V1), abs(V2)) * 1.35 + 0.02
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Diagrama Fasorial — Tensiones y Corriente", font=dict(size=13)),
        xaxis=dict(range=[-m * 0.15, m], zeroline=True, zerolinecolor="#aaa",
                   gridcolor=_C["grid"], title="Real [pu]"),
        yaxis=dict(range=[-m * 0.5, m * 0.5], zeroline=True, zerolinecolor="#aaa",
                   gridcolor=_C["grid"], title="Imag [pu]", scaleanchor="x"),
        height=340,
        showlegend=False,
    )
    return fig


# ---------------------------------------------------------------------------
# GRÁFICO 3: TRIÁNGULO DE POTENCIAS (Bus 2)
# ---------------------------------------------------------------------------
def _grafico_potencias(r):
    S2 = r["S2"]; Sl = r["Sloss"]
    P  = S2.real; Q = S2.imag; S = abs(S2)
    Pl = Sl.real; Ql = Sl.imag

    fig = go.Figure()

    # Fondo del triángulo
    fig.add_trace(go.Scatter(
        x=[0, P, P, 0], y=[0, 0, Q, 0],
        fill="toself", fillcolor="rgba(29,53,87,0.06)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip",
    ))

    def _arrow(x0, y0, x1, y1, color, label, xsh=0, ysh=8):
        fig.add_annotation(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowwidth=2,
            arrowcolor=color,
            text=label, font=dict(color=color, size=11),
            xanchor="center", yanchor="bottom",
            xshift=xsh, yshift=ysh,
        )

    _arrow(0, 0, P, 0, _C["P"], f"P={P:.5f} pu")
    if abs(Q) > 1e-4:
        _arrow(P, 0, P, Q, _C["Q"], f"Q={Q:.5f} pu", xsh=8)

    # Vector S
    fig.add_annotation(
        ax=0, ay=0, x=P, y=Q,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2.5,
        arrowcolor=_C["S"], text="",
    )
    fig.add_annotation(
        x=P / 2, y=Q / 2, showarrow=False,
        text=f"S={S:.5f} pu",
        font=dict(color=_C["S"], size=12, weight="bold"),
        xshift=-12, yshift=10, xanchor="right", yanchor="bottom",
    )

    # Pérdidas
    if abs(Pl) > 1e-6:
        fig.add_annotation(
            x=Pl / 2, y=-0.05 * S, showarrow=False,
            text=f"Pₗₒₛₛ={Pl:.6f} pu  |  Qₗₒₛₛ={Ql:.6f} pu",
            font=dict(color=_C["loss"], size=10),
        )

    m = S * 0.3 + 0.01
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Triángulo de Potencias — Bus 2", font=dict(size=13)),
        xaxis=dict(range=[-m * 0.15, P + m], zeroline=True,
                   zerolinecolor="#aaa", gridcolor=_C["grid"], title="P [pu]"),
        yaxis=dict(range=[min(-m, Q - m * 0.3), max(m, Q + m * 0.3)],
                   zeroline=True, zerolinecolor="#aaa",
                   gridcolor=_C["grid"], title="Q [pu]", scaleanchor="x"),
        height=320,
    )
    return fig


# ---------------------------------------------------------------------------
# GRÁFICO 4: CONVERGENCIA GAUSS-SEIDEL
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _convergencia_data(R, X, Pload, Qload, Qcap, V2mag, V2ang):
    """Registra el error por iteración para visualizar la convergencia."""
    S1 = complex(-Pload, Qcap - Qload)
    V2 = _cpolar(V2mag, V2ang)
    Z  = complex(R, X)
    if abs(Z) < 1e-6:
        return [0.0], True

    Y  = 1 / Z
    Yn = -Y
    V1 = _cpolar(V2mag, 0)
    errors = []
    ok = False
    for k in range(200):
        rhs    = np.conj(S1) / np.conj(V1) - Yn * V2
        V1_new = rhs / Y
        err    = abs(V1_new - V1)
        errors.append(float(err))
        V1     = V1_new
        if err < 1e-10:
            ok = True
            break
    return errors, ok


def _grafico_convergencia(errors, ok):
    iters = list(range(1, len(errors) + 1))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=iters, y=errors, mode="lines+markers",
        line=dict(color="#1d3557", width=2),
        marker=dict(size=5, color="#e63946"),
        name="Error ‖ΔV‖",
        hovertemplate="Iter %{x}: error=%{y:.2e}<extra></extra>",
    ))
    fig.add_hline(y=1e-10, line_dash="dot", line_color="#059669",
                  annotation_text="ε = 1e-10", annotation_position="right")
    conv_str = "✓ Convergió" if ok else "✗ No convergió"
    fig.update_layout(
        **_LAYOUT,
        title=dict(text=f"Convergencia Gauss-Seidel — {conv_str}", font=dict(size=13)),
        xaxis=dict(title="Iteración", gridcolor=_C["grid"]),
        yaxis=dict(title="‖ΔV‖ [pu]", type="log", gridcolor=_C["grid"]),
        height=300,
    )
    return fig


# ---------------------------------------------------------------------------
# RENDER PRINCIPAL
# ---------------------------------------------------------------------------
def render():
    st.markdown("## ⚡ Flujo de Carga — Red de 2 Buses")
    st.caption(
        "Método de Gauss-Seidel  |  Sistema en valores por unidad [pu]  |  "
        "Desarrollado por Dr. Maykop Perez Martinez · Universidad de Concepción"
    )

    # Aplicar presets pendientes (mismo patrón anti-doble-trigger de graficos.py)
    for src, dst in [
        ("_fc_R_pending",  "fc_R"),
        ("_fc_X_pending",  "fc_X"),
        ("_fc_P_pending",  "fc_P"),
        ("_fc_Q_pending",  "fc_Q"),
        ("_fc_Qc_pending", "fc_Qc"),
        ("_fc_V_pending",  "fc_V"),
        ("_fc_A_pending",  "fc_A"),
    ]:
        if src in st.session_state:
            st.session_state[dst] = st.session_state.pop(src)

    # ------------------------------------------------------------------
    # CONFIGURACIÓN DEL CIRCUITO
    # ------------------------------------------------------------------
    with st.expander("⚙️ Configuración del circuito", expanded=True):
        st.markdown("**Casos predefinidos:**")
        presets = {
            "Resistivo puro": dict(R=0.00, X=0.50, P=0.50, Q=1.00, Qc=1.00, V=1.00, A=0.0),
            "Inductivo":      dict(R=0.05, X=0.30, P=0.80, Q=0.60, Qc=0.00, V=0.95, A=0.0),
            "Capacitivo":     dict(R=0.02, X=0.40, P=0.40, Q=-0.30, Qc=0.50, V=1.00, A=0.0),
            "Alta carga":     dict(R=0.10, X=0.60, P=1.20, Q=0.90, Qc=0.80, V=0.90, A=-5.0),
            "Sin pérdidas":   dict(R=0.00, X=0.50, P=0.60, Q=0.40, Qc=0.40, V=1.00, A=0.0),
        }
        cols_p = st.columns(len(presets))
        for i, (name, vals) in enumerate(presets.items()):
            if cols_p[i].button(name, key=f"fc_preset_{i}", use_container_width=True):
                for k2, v2 in [("R", vals["R"]), ("X", vals["X"]),
                               ("P", vals["P"]), ("Q", vals["Q"]),
                               ("Qc", vals["Qc"]), ("V", vals["V"]),
                               ("A", vals["A"])]:
                    st.session_state[f"_fc_{k2}_pending"] = float(v2)
                st.rerun()

        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Parámetros de la línea Z = R + jX**")
            R = st.slider("Resistencia R [pu]", 0.00, 0.50,
                          float(st.session_state.get("fc_R", 0.00)), 0.01, key="fc_R")
            X = st.slider("Reactancia X [pu]", 0.00, 1.00,
                          float(st.session_state.get("fc_X", 0.50)), 0.01, key="fc_X")
        with col2:
            st.markdown("**Carga en Bus 2**")
            Pload = st.slider("Potencia activa P [pu]", 0.00, 2.00,
                              float(st.session_state.get("fc_P", 0.50)), 0.01, key="fc_P")
            Qload = st.slider("Potencia reactiva Q [pu]", -1.00, 2.00,
                              float(st.session_state.get("fc_Q", 1.00)), 0.01, key="fc_Q")
            Qcap  = st.slider("Compensación capacitiva Qc [pu]", 0.00, 2.00,
                              float(st.session_state.get("fc_Qc", 1.00)), 0.01, key="fc_Qc")

        st.markdown("**Bus 2 — Condición inicial**")
        ca, cb = st.columns(2)
        with ca:
            V2mag = st.slider("|V₂| [pu]", 0.80, 1.20,
                              float(st.session_state.get("fc_V", 1.00)), 0.01, key="fc_V")
        with cb:
            V2ang = st.slider("∠V₂ [°]", -30.0, 10.0,
                              float(st.session_state.get("fc_A", 0.00)), 0.5, key="fc_A")

    # ------------------------------------------------------------------
    # CÁLCULO
    # ------------------------------------------------------------------
    r = solve(R, X, Pload, Qload, Qcap, V2mag, V2ang)
    r["R"] = R; r["X"] = X; r["Qcap"] = Qcap

    V1 = r["V1"]; V2 = r["V2"]
    I  = r["I"];  S2 = r["S2"]
    Sl = r["Sloss"]; dV = r["dV"]

    # Badge de convergencia
    if r["ok"]:
        st.success(f"✓ Convergió en {r['iters']} iteraciones", icon="✅")
    else:
        st.error("✗ No convergió — verifica los parámetros", icon="⚠️")

    st.markdown("---")
    st.markdown("### Resultados")

    _metric_cards([
        ("V₁ (módulo)", f"{abs(V1):.4f}", "pu"),
        ("V₁ (ángulo)", f"{np.degrees(np.angle(V1)):.3f}", "°"),
        ("|ΔV|",        f"{abs(dV):.4f}", "pu"),
    ], accent=_C["bus1"])

    _metric_cards([
        ("|I|",         f"{abs(I):.4f}", "pu"),
        ("∠I",          f"{np.degrees(np.angle(I)):.3f}", "°"),
        ("Iteraciones", str(r["iters"]), ""),
    ], accent=_C["I"])

    _metric_cards([
        ("P entregada",  f"{S2.real:.5f}", "pu"),
        ("Q entregada",  f"{S2.imag:.5f}", "pu"),
        ("|S|",          f"{abs(S2):.5f}", "pu"),
    ], accent=_C["P"])

    _metric_cards([
        ("Pₗₒₛₛ",        f"{Sl.real:.6f}", "pu"),
        ("Qₗₒₛₛ",        f"{Sl.imag:.6f}", "pu"),
        ("η = P/(P+Pₗ)", f"{S2.real / (S2.real + Sl.real + 1e-12) * 100:.2f}", "%"),
    ], accent=_C["loss"])

    # Valores completos
    with st.expander("📐 Valores completos en forma polar y rectangular"):
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("**Tensión V₁ (Slack)**")
            st.code(f"Polar:  {_fPol(V1, 4)}\nRect:   {_fC(V1, 4)} pu")
            st.markdown("**Corriente I**")
            st.code(f"Polar:  {_fPol(I, 4)}\nRect:   {_fC(I, 4)} pu")
        with col_b:
            st.markdown("**Caída de tensión ΔV = Z·I**")
            st.code(f"Polar:  {_fPol(dV, 5)}\nRect:   {_fC(dV, 4)} pu")
            st.markdown("**Potencia aparente S₂**")
            st.code(f"Polar:  {_fPol(S2, 4)}\nRect:   {_fC(S2, 4)} pu")

    # ------------------------------------------------------------------
    # GRÁFICOS
    # ------------------------------------------------------------------
    st.markdown("---")
    tab_unif, tab_fas, tab_pot, tab_conv = st.tabs([
        "🔌 Diagrama Unifilar",
        "📐 Diagrama Fasorial",
        "⚡ Triángulo de Potencias",
        "📈 Convergencia G-S",
    ])

    with tab_unif:
        st.plotly_chart(_grafico_unifilar(r), use_container_width=True, key="fc_unif")

    with tab_fas:
        st.plotly_chart(_grafico_fasorial(r), use_container_width=True, key="fc_fas")

    with tab_pot:
        st.plotly_chart(_grafico_potencias(r), use_container_width=True, key="fc_pot")

    with tab_conv:
        errors, ok_conv = _convergencia_data(R, X, Pload, Qload, Qcap, V2mag, V2ang)
        st.plotly_chart(_grafico_convergencia(errors, ok_conv),
                        use_container_width=True, key="fc_conv")

    # ------------------------------------------------------------------
    # ZONA DE PRÁCTICA PEDAGÓGICA
    # ------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### 🎓 Practica: verifica tu comprensión")
    st.caption(
        "Resuelve con lápiz y papel usando los parámetros configurados. "
        "Tienes 2 intentos por pregunta antes de ver el procedimiento completo."
    )

    for k, v in [
        ("fc_attempts", {"V1": 0, "I": 0, "P": 0}),
        ("fc_show_fb",  False),
        ("fc_user_V1",  ""),
        ("fc_user_I",   ""),
        ("fc_user_P",   ""),
    ]:
        if k not in st.session_state:
            st.session_state[k] = v

    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        user_V1 = st.text_input("|V₁| (pu):", value=st.session_state["fc_user_V1"],
                                placeholder="Ej: 1.0500", key="fc_ui_V1")
    with pc2:
        user_I  = st.text_input("|I| (pu):", value=st.session_state["fc_user_I"],
                                placeholder="Ej: 0.7200", key="fc_ui_I")
    with pc3:
        user_P  = st.text_input("P entregada (pu):", value=st.session_state["fc_user_P"],
                                placeholder="Ej: 0.5000", key="fc_ui_P")

    pb1, pb2 = st.columns([1, 1])
    with pb1:
        verificar = st.button("Verificar respuestas", type="primary",
                              use_container_width=True, key="fc_verificar")
    with pb2:
        if st.button("Reiniciar práctica", use_container_width=True, key="fc_reset"):
            st.session_state["fc_attempts"] = {"V1": 0, "I": 0, "P": 0}
            st.session_state["fc_show_fb"]  = False
            for k in ["fc_user_V1", "fc_user_I", "fc_user_P"]:
                st.session_state[k] = ""
            st.rerun()

    if verificar:
        att = st.session_state["fc_attempts"]
        if user_V1:
            att["V1"] += 1
            st.session_state["fc_user_V1"] = user_V1
        if user_I:
            att["I"] += 1
            st.session_state["fc_user_I"] = user_I
        if user_P:
            att["P"] += 1
            st.session_state["fc_user_P"] = user_P
        st.session_state["fc_attempts"] = att
        st.session_state["fc_show_fb"]  = True
        st.rerun()

    if st.session_state["fc_show_fb"]:
        att      = st.session_state["fc_attempts"]
        corr_V1  = abs(V1)
        corr_I   = abs(I)
        corr_P   = S2.real

        def _chk(user_str, correct, att_count, label, formula_steps):
            try:
                uval = float(user_str)
            except (ValueError, TypeError):
                return
            tol = max(0.005 * abs(correct), 1e-4)
            ok_ = abs(uval - correct) < tol
            if ok_:
                st.success(f"✓ Correcto — {label}")
                with st.expander("Ver procedimiento"):
                    for paso, det in formula_steps:
                        st.markdown(f"**{paso}:** {det}")
            else:
                st.error(f"✗ Incorrecto — {label}")
                if att_count <= 1:
                    st.caption("Intento 1/2 — reflexiona antes de reintentar:")
                    if label == "|V₁|":
                        st.markdown("- Recuerda: V₁ se calcula por Gauss-Seidel a partir de V₂ y la carga")
                        st.markdown("- ¿Calculaste la corriente I = (V₁−V₂)/Z primero?")
                    elif label == "|I|":
                        st.markdown("- La corriente fluye por la impedancia Z = R + jX")
                        st.markdown("- I = (V₁ − V₂) / Z  (número complejo)")
                    else:
                        st.markdown("- P = Re(V₂ · I*) — fasor de tensión por conjugado de corriente")
                        st.markdown("- ¿Usaste los valores en pu?")
                else:
                    st.caption("Intento 2/2 — procedimiento correcto:")
                    for paso, det in formula_steps:
                        st.markdown(f"**{paso}:** {det}")
                    st.info(f"Respuesta correcta: {correct:.5f} pu")

        u_V1 = st.session_state["fc_user_V1"]
        u_I  = st.session_state["fc_user_I"]
        u_P  = st.session_state["fc_user_P"]

        if u_V1:
            _chk(u_V1, corr_V1, att["V1"], "|V₁|", [
                ("Ecuación", "V₁ = V₂ + Z·I"),
                ("Z",        f"({R:.2f} + j{X:.2f}) pu"),
                ("V₂",       f"{_fPol(V2, 4)}"),
                ("I",        f"{_fPol(I, 4)}"),
                ("|V₁|",     f"{corr_V1:.5f} pu"),
            ])
        if u_I:
            _chk(u_I, corr_I, att["I"], "|I|", [
                ("Ecuación",  "I = (V₁ − V₂) / Z"),
                ("Numerador", f"{_fPol(V1 - V2, 4)}"),
                ("Z",         f"{_fPol(complex(R, X), 4)}"),
                ("|I|",       f"{corr_I:.5f} pu"),
            ])
        if u_P:
            _chk(u_P, corr_P, att["P"], "P entregada", [
                ("Ecuación",  "P = Re(V₂ · I*)"),
                ("V₂",        f"{_fPol(V2, 4)}"),
                ("I*",        f"{_fPol(np.conj(I), 4)}"),
                ("S₂ = V₂·I*", f"{_fC(S2, 5)} pu"),
                ("P = Re(S₂)", f"{corr_P:.5f} pu"),
            ])
