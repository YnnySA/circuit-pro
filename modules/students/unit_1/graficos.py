"""
Modulo de simuladores interactivos - Unidad 1: Circuitos Electricos
Basado en las aplicaciones de simulacion del Dr. Maykop Perez Martinez,
Departamento de Ingenieria Electrica, Universidad de Concepcion.

Optimizaciones aplicadas:
- Fondo blanco/neutral (sin dark theme) para menor carga de render
- Puntos de muestreo reducidos (800 -> 300)
- Trazos simplificados: sin scatter de cuadricula, menos annotations
- @st.cache_data en calculos de onda para evitar recomputo innecesario
- key fijo en plotly_chart para evitar re-mounts del DOM
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Layout base: fondo limpio, sin colores innecesarios
_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="#f8f9fa",
    font=dict(color="#333333", family="Segoe UI, sans-serif", size=12),
    margin=dict(l=48, r=24, t=36, b=40),
    hoverlabel=dict(bgcolor="white", font_size=12),
)

# Paleta reducida y clara
_C = {
    "R":   "#e63946",
    "X":   "#457b9d",
    "XL":  "#6d28d9",
    "XC":  "#059669",
    "Z":   "#1d3557",
    "phi": "#f4a261",
    "P":   "#e63946",
    "Q":   "#6d28d9",
    "S":   "#1d3557",
    "sin": "#1d6aa5",
    "rms": "#e63946",
    "grid": "#e0e0e0",
}


# ===========================================================================
# 1. SIMULADOR RLC
# ===========================================================================
def _sim_rlc():
    st.markdown("### Simulador de Circuito RLC Serie")
    st.caption(
        "Ajusta los parametros para observar como cambia la impedancia, "
        "el angulo de fase y el diagrama fasorial."
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        V  = st.slider("Tension V (V)",        1.0,  220.0, 100.0, 1.0,  key="rlc_V")
        R  = st.slider("Resistencia R (Ohm)",  1.0,  500.0, 100.0, 1.0,  key="rlc_R")
        L  = st.slider("Inductancia L (mH)",   1.0,  500.0, 100.0, 1.0,  key="rlc_L")
        C  = st.slider("Capacitancia C (uF)",  1.0,  500.0, 100.0, 1.0,  key="rlc_C")
        f  = st.slider("Frecuencia f (Hz)",     1.0,  500.0,  50.0, 1.0,  key="rlc_f")
        mostrar_construccion = st.checkbox("Mostrar lineas de construccion", value=True, key="rlc_constr")

    # Calculos
    w   = 2 * np.pi * f
    XL  = w * L * 1e-3
    XC  = 1 / (w * C * 1e-6)
    X   = XL - XC
    Z   = np.sqrt(R**2 + X**2)
    phi = np.degrees(np.arctan2(X, R))
    I   = V / Z
    f0  = 1 / (2 * np.pi * np.sqrt(L * 1e-3 * C * 1e-6))

    with c2:
        m1, m2, m3 = st.columns(3)
        m1.metric("Impedancia |Z|", f"{Z:.2f} Ohm")
        m2.metric("Corriente I",    f"{I*1000:.2f} mA" if I < 0.1 else f"{I:.3f} A")
        m3.metric("Angulo phi",     f"{phi:.1f} deg")
        m4, m5, m6 = st.columns(3)
        m4.metric("X_L", f"{XL:.2f} Ohm")
        m5.metric("X_C", f"{XC:.2f} Ohm")
        m6.metric("X neta", f"{X:+.2f} Ohm")

        if abs(X) < 0.5:
            st.success(f"Resonancia - f0 = {f0:.1f} Hz", icon="\u26a1")
        elif X > 0:
            st.info(f"Inductivo (phi = {phi:.1f} deg) | f0 = {f0:.1f} Hz")
        else:
            st.info(f"Capacitivo (phi = {phi:.1f} deg) | f0 = {f0:.1f} Hz")

    # Diagrama fasorial
    fig = go.Figure()
    margin = Z * 0.35

    if mostrar_construccion:
        fig.add_shape(type="line", x0=R, y0=0, x1=R, y1=X,
                      line=dict(color="#cccccc", dash="dot", width=1))
        fig.add_shape(type="line", x0=0, y0=X, x1=R, y1=X,
                      line=dict(color="#cccccc", dash="dot", width=1))

    fig.add_annotation(ax=0, ay=0, x=R, y=0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=_C["R"],
                       text=f"R={R:.0f} Ohm", font=dict(color=_C["R"], size=11))

    if abs(X) > 0.1:
        x_col = _C["XL"] if X > 0 else _C["XC"]
        fig.add_annotation(ax=R, ay=0, x=R, y=X, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=x_col,
                           text=f"X={X:+.1f} Ohm", font=dict(color=x_col, size=11))

    fig.add_annotation(ax=0, ay=0, x=R, y=X, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=_C["Z"],
                       text=f"Z={Z:.2f} Ohm", font=dict(color=_C["Z"], size=12))

    if abs(phi) > 1:
        t_arc = np.linspace(0, np.radians(phi), 30)
        r_arc = Z * 0.25
        fig.add_trace(go.Scatter(
            x=r_arc * np.cos(t_arc), y=r_arc * np.sin(t_arc),
            mode="lines", line=dict(color=_C["phi"], dash="dash", width=1.5),
            name=f"phi = {phi:.1f} deg",
        ))

    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Diagrama Fasorial de Impedancia", font=dict(size=13)),
        xaxis=dict(range=[-margin * 0.2, R + margin], zeroline=True, zerolinecolor="#aaa",
                   gridcolor=_C["grid"], title="R (Ohm)"),
        yaxis=dict(range=[min(-margin, X - margin * 0.5), max(margin, X + margin * 0.5)],
                   zeroline=True, zerolinecolor="#aaa", gridcolor=_C["grid"],
                   title="X (Ohm)", scaleanchor="x"),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True, key="chart_rlc")


# ===========================================================================
# 2. SIMULADOR DE POTENCIAS
# ===========================================================================
def _sim_potencias():
    st.markdown("### Simulador de Triangulo de Potencias")
    st.caption(
        "Modifica la potencia activa y reactiva para visualizar "
        "el triangulo de potencias y el factor de potencia."
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        P = st.slider("Potencia Activa P (kW)",    0.1, 10.0, 3.0, 0.1, key="pot_P")
        Q = st.slider("Potencia Reactiva Q (kVAR)", 0.0, 10.0, 4.0, 0.1, key="pot_Q")
        tipo_Q = st.radio("Naturaleza de Q:",
                          ["Inductiva (Q > 0)", "Capacitiva (Q < 0)"],
                          horizontal=True, key="pot_tipo")
        if "Capacitiva" in tipo_Q:
            Q = -Q

    S   = np.sqrt(P**2 + Q**2)
    fp  = P / S if S > 0 else 1.0
    phi = np.degrees(np.arctan2(Q, P))

    with c2:
        m1, m2 = st.columns(2)
        m1.metric("Potencia Aparente S", f"{S:.3f} kVA")
        m2.metric("Factor de Potencia",  f"{fp:.4f}")
        m3, m4 = st.columns(2)
        m3.metric("Angulo phi",          f"{phi:.2f} deg")
        m4.metric("|Q|",                 f"{abs(Q):.2f} kVAR")

        estado_fp = "Bueno" if fp > 0.9 else ("Mejorable" if fp > 0.7 else "Bajo")
        color_fp  = "#059669" if fp > 0.9 else ("#d97706" if fp > 0.7 else "#dc2626")
        st.markdown(f"""
        <div style='margin-top:8px;'>
          <div style='display:flex;justify-content:space-between;font-size:0.82em;color:#555;'>
            <span>fp = {fp:.3f}</span><span>{estado_fp}</span>
          </div>
          <div style='background:#e5e7eb;border-radius:8px;height:12px;margin-top:4px;overflow:hidden;'>
            <div style='width:{fp*100:.1f}%;height:100%;background:{color_fp};border-radius:8px;'></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    fig = go.Figure()
    m   = S * 0.3

    fig.add_trace(go.Scatter(
        x=[0, P, P, 0], y=[0, 0, Q, 0],
        fill="toself", fillcolor="rgba(29,53,87,0.06)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip",
    ))

    fig.add_annotation(ax=0, ay=0, x=P, y=0, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=_C["P"],
                       text=f"P={P:.2f} kW", font=dict(color=_C["P"], size=11))

    if abs(Q) > 0.01:
        fig.add_annotation(ax=P, ay=0, x=P, y=Q, xref="x", yref="y", axref="x", ayref="y",
                           showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor=_C["Q"],
                           text=f"Q={abs(Q):.2f} kVAR", font=dict(color=_C["Q"], size=11))

    fig.add_annotation(ax=0, ay=0, x=P, y=Q, xref="x", yref="y", axref="x", ayref="y",
                       showarrow=True, arrowhead=2, arrowwidth=2.5, arrowcolor=_C["S"],
                       text=f"S={S:.3f} kVA", font=dict(color=_C["S"], size=12))

    if abs(phi) > 0.5:
        t_arc = np.linspace(0, np.radians(phi), 30)
        r_arc = S * 0.22
        fig.add_trace(go.Scatter(
            x=r_arc * np.cos(t_arc), y=r_arc * np.sin(t_arc),
            mode="lines", line=dict(color=_C["phi"], dash="dash", width=1.5),
            name=f"phi = {phi:.1f} deg",
        ))

    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Triangulo de Potencias", font=dict(size=13)),
        xaxis=dict(range=[-m * 0.2, P + m], zeroline=True, zerolinecolor="#aaa",
                   gridcolor=_C["grid"], title="P (kW)"),
        yaxis=dict(range=[min(-m, Q - m * 0.3), max(m, Q + m * 0.3)],
                   zeroline=True, zerolinecolor="#aaa", gridcolor=_C["grid"],
                   title="Q (kVAR)", scaleanchor="x"),
        height=360,
    )
    st.plotly_chart(fig, use_container_width=True, key="chart_pot")


# ===========================================================================
# 3. SIMULADOR DE ONDA SENOIDAL
# ===========================================================================
@st.cache_data(show_spinner=False)
def _calcular_onda(Am, f, phi_deg, dos_ciclos):
    """Calculo cacheado de la onda - solo se recomputa si cambian los parametros."""
    T      = 1 / f
    ciclos = 2 if dos_ciclos else 1
    t      = np.linspace(0, ciclos * T, 300)
    v      = Am * np.sin(2 * np.pi * f * t + np.radians(phi_deg))
    Vrms   = Am / np.sqrt(2)
    return t, v, T, Vrms


def _sim_onda():
    st.markdown("### Visualizador de Onda Senoidal")
    st.caption("Observa como la amplitud, frecuencia y fase modifican la forma de la senal.")

    c1, c2 = st.columns([1, 2])
    with c1:
        Am  = st.slider("Amplitud maxima Vm (V)", 10.0, 400.0, 141.4, 0.5,    key="onda_Am")
        f   = st.slider("Frecuencia f (Hz)",        1.0, 200.0,  50.0, 1.0,    key="onda_f")
        phi = st.slider("Fase inicial phi (deg)", -180.0, 180.0,   0.0, 5.0,   key="onda_phi")
        st.markdown("---")
        mostrar_rms     = st.checkbox("Mostrar linea V_rms",    value=True,  key="onda_rms")
        mostrar_periodo = st.checkbox("Mostrar periodo T",       value=True,  key="onda_T")
        mostrar_pico    = st.checkbox("Mostrar valor pico",      value=True,  key="onda_pk")
        dos_ciclos      = st.checkbox("Ver 2 ciclos completos",  value=False, key="onda_2c")

    t, v, T, Vrms = _calcular_onda(Am, f, phi, dos_ciclos)

    with c1:
        st.markdown("**Resultados:**")
        st.metric("V_rms",     f"{Vrms:.2f} V")
        st.metric("Periodo T", f"{T*1000:.3f} ms")
        st.metric("V pico",    f"{Am:.1f} V")

    with c2:
        fig = go.Figure()

        if mostrar_periodo:
            fig.add_vrect(x0=0, x1=T * 1000,
                          fillcolor="rgba(29,106,165,0.05)", layer="below", line_width=0)
            fig.add_vline(x=T * 1000, line_dash="dot", line_color="#457b9d", opacity=0.6,
                          annotation_text=f"T={T*1000:.2f} ms",
                          annotation_font=dict(color="#457b9d", size=11))

        if mostrar_rms:
            fig.add_hline(y=Vrms, line_dash="dash", line_color=_C["rms"], line_width=1.5,
                          annotation_text=f"V_rms={Vrms:.1f} V",
                          annotation_font=dict(color=_C["rms"], size=11))
            fig.add_hline(y=-Vrms, line_dash="dash", line_color=_C["rms"],
                          line_width=1, opacity=0.4)

        if mostrar_pico:
            fig.add_hline(y=Am, line_dash="dot", line_color="#d97706", line_width=1,
                          annotation_text=f"Vm={Am:.1f} V",
                          annotation_font=dict(color="#d97706", size=11),
                          annotation_position="bottom right")

        fig.add_trace(go.Scatter(
            x=t * 1000, y=v,
            mode="lines",
            line=dict(color=_C["sin"], width=2),
            name=f"v(t)={Am:.1f}*sin(2pi*{f:.0f}t+{phi:.0f}deg)",
            hovertemplate="t=%{x:.2f} ms<br>v=%{y:.2f} V<extra></extra>",
        ))

        fig.add_hline(y=0, line_color="#aaa", line_width=1)

        fig.update_layout(
            **_LAYOUT,
            title=dict(text="Senal de Tension Alterna", font=dict(size=13)),
            xaxis=dict(title="Tiempo (ms)", gridcolor=_C["grid"], zeroline=False),
            yaxis=dict(title="Tension (V)", gridcolor=_C["grid"], zeroline=False,
                       range=[-Am * 1.25, Am * 1.25]),
            height=360,
            legend=dict(orientation="h", yanchor="top", y=-0.18),
        )
        st.plotly_chart(fig, use_container_width=True, key="chart_onda")


# ===========================================================================
# RENDER PRINCIPAL
# ===========================================================================
def render():
    """Renderiza los simuladores interactivos de la Unidad 1."""
    st.markdown("## Simuladores Interactivos - Unidad 1")
    st.markdown(
        "Experimenta con los parametros de cada circuito y observa "
        "como los valores y diagramas se actualizan al instante."
    )

    tab_rlc, tab_pot, tab_onda = st.tabs([
        "Circuito RLC",
        "Triangulo de Potencias",
        "Onda Senoidal",
    ])
    with tab_rlc:
        _sim_rlc()
    with tab_pot:
        _sim_potencias()
    with tab_onda:
        _sim_onda()
