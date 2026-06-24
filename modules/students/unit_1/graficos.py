"""
Módulo de simuladores interactivos — Unidad 1: Circuitos Eléctricos
Basado en las aplicaciones de simulación del Dr. Maykop Pérez Martínez,
Departamento de Ingeniería Eléctrica, Universidad de Concepción.
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st


# ── Paleta de colores coherente con el proyecto ───────────────────────────────
_C = {
    "V":    "#ff6b6b",
    "R":    "#ffd700",
    "X":    "#fdcb6e",
    "XL":   "#a29bfe",
    "XC":   "#55efc4",
    "Z":    "#00d4ff",
    "phi":  "#fd79a8",
    "P":    "#ffd700",
    "Q":    "#a29bfe",
    "S":    "#00d4ff",
    "sin":  "#00d4ff",
    "rms":  "#ff6b6b",
    "grid": "rgba(255,255,255,0.08)",
    "bg":   "#0d1b2a",
    "paper":"#16213e",
}

_LAYOUT = dict(
    paper_bgcolor=_C["paper"],
    plot_bgcolor=_C["bg"],
    font=dict(color="#cccccc", family="Segoe UI, sans-serif"),
    margin=dict(l=48, r=48, t=40, b=40),
)


# ════════════════════════════════════════════════════════════════════════════
# 1. SIMULADOR RLC — Impedancia y diagrama fasorial
# ════════════════════════════════════════════════════════════════════════════
def _sim_rlc():
    st.markdown("### ⚡ Simulador de Circuito RLC Serie")
    st.caption(
        "Ajusta los parámetros para observar cómo cambia la impedancia, "
        "el ángulo de fase y el diagrama fasorial en tiempo real."
    )

    c1, c2 = st.columns([1, 1])

    with c1:
        V  = st.slider("Tensión V (V)",          min_value=1.0,  max_value=220.0, value=100.0, step=1.0)
        R  = st.slider("Resistencia R (Ω)",       min_value=1.0,  max_value=500.0, value=100.0, step=1.0)
        L  = st.slider("Inductancia L (mH)",       min_value=1.0,  max_value=500.0, value=100.0, step=1.0)
        C  = st.slider("Capacitancia C (μF)",      min_value=1.0,  max_value=500.0, value=100.0, step=1.0)
        f  = st.slider("Frecuencia f (Hz)",         min_value=1.0,  max_value=500.0, value=50.0,  step=1.0)

        mostrar_construccion = st.checkbox("Mostrar líneas de construcción", value=True)

    # ── Cálculos ─────────────────────────────────────────────────────────────
    w   = 2 * np.pi * f
    XL  = w * L * 1e-3
    XC  = 1 / (w * C * 1e-6)
    X   = XL - XC
    Z   = np.sqrt(R**2 + X**2)
    phi = np.degrees(np.arctan2(X, R))
    I   = V / Z
    f0  = 1 / (2 * np.pi * np.sqrt(L * 1e-3 * C * 1e-6))

    with c2:
        # ── Métricas ─────────────────────────────────────────────────────────
        m1, m2, m3 = st.columns(3)
        m1.metric("Impedancia |Z|", f"{Z:.2f} Ω")
        m2.metric("Corriente I",    f"{I*1000:.2f} mA" if I < 0.1 else f"{I:.3f} A")
        m3.metric("Ángulo φ",       f"{phi:.1f}°")

        m4, m5, m6 = st.columns(3)
        m4.metric("X_L", f"{XL:.2f} Ω")
        m5.metric("X_C", f"{XC:.2f} Ω")
        m6.metric("X neta", f"{X:+.2f} Ω")

        # Naturaleza del circuito
        if abs(X) < 0.5:
            st.success(f"🎯 **Resonancia** — Z = R mínimo | f₀ = {f0:.1f} Hz", icon="⚡")
        elif X > 0:
            st.info(f"🔵 Circuito **Inductivo** (φ = {phi:.1f}°) | f₀ = {f0:.1f} Hz", icon="🔌")
        else:
            st.info(f"🟢 Circuito **Capacitivo** (φ = {phi:.1f}°) | f₀ = {f0:.1f} Hz", icon="🔋")

    # ── Diagrama fasorial de impedancia ──────────────────────────────────────
    fig = go.Figure()

    # Cuadrícula extra (puntos)
    for xi in np.linspace(0, R * 1.3, 6):
        for yi in np.linspace(-abs(X) * 1.5, abs(X) * 1.5, 8):
            fig.add_trace(go.Scatter(
                x=[xi], y=[yi], mode="markers",
                marker=dict(color=_C["grid"], size=3), showlegend=False, hoverinfo="skip"
            ))

    if mostrar_construccion:
        # Líneas de construcción (triángulo)
        fig.add_shape(type="line", x0=R, y0=0, x1=R, y1=X,
                      line=dict(color="#2d4a6e", dash="dot", width=1.5))
        fig.add_shape(type="line", x0=0, y0=X, x1=R, y1=X,
                      line=dict(color="#2d4a6e", dash="dot", width=1.5))

    # Vector R (horizontal)
    fig.add_annotation(
        ax=0, ay=0, x=R, y=0, xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
        arrowcolor=_C["R"],
    )
    fig.add_trace(go.Scatter(
        x=[R / 2], y=[-abs(X) * 0.12 - 2],
        mode="text", text=[f"R = {R:.0f} Ω"],
        textfont=dict(color=_C["R"], size=12), showlegend=False, hoverinfo="skip"
    ))

    # Vector X (vertical desde tip de R)
    if abs(X) > 0.1:
        x_col = _C["XL"] if X > 0 else _C["XC"]
        x_lbl = f"X_L–X_C = {X:+.1f} Ω"
        fig.add_annotation(
            ax=R, ay=0, x=R, y=X, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
            arrowcolor=x_col,
        )
        fig.add_trace(go.Scatter(
            x=[R + Z * 0.08], y=[X / 2],
            mode="text", text=[x_lbl],
            textfont=dict(color=x_col, size=11), showlegend=False, hoverinfo="skip"
        ))

    # Vector Z (hipotenusa)
    fig.add_annotation(
        ax=0, ay=0, x=R, y=X, xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
        arrowcolor=_C["Z"],
    )
    fig.add_trace(go.Scatter(
        x=[R / 2 - Z * 0.06], y=[X / 2 + Z * 0.06],
        mode="text", text=[f"Z = {Z:.2f} Ω"],
        textfont=dict(color=_C["Z"], size=13, family="Segoe UI bold"),
        showlegend=False, hoverinfo="skip"
    ))

    # Arco de φ
    if abs(phi) > 1:
        t_arc = np.linspace(0, np.radians(phi), 40)
        r_arc = Z * 0.25
        fig.add_trace(go.Scatter(
            x=r_arc * np.cos(t_arc), y=r_arc * np.sin(t_arc),
            mode="lines", line=dict(color=_C["phi"], dash="dash", width=1.5),
            name=f"φ = {phi:.1f}°", showlegend=True,
        ))

    margin = Z * 0.35
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Diagrama Fasorial de Impedancia", font=dict(size=14, color="#aaa")),
        xaxis=dict(
            range=[-margin * 0.3, R + margin],
            zeroline=True, zerolinecolor="#2d4a6e",
            gridcolor=_C["grid"], title="R (Ω)",
        ),
        yaxis=dict(
            range=[min(-margin, X - margin * 0.5), max(margin, X + margin * 0.5)],
            zeroline=True, zerolinecolor="#2d4a6e",
            gridcolor=_C["grid"], title="X (Ω)", scaleanchor="x",
        ),
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# 2. SIMULADOR DE POTENCIAS — Triángulo de potencias
# ════════════════════════════════════════════════════════════════════════════
def _sim_potencias():
    st.markdown("### 🔺 Simulador de Triángulo de Potencias")
    st.caption(
        "Modifica la potencia activa y reactiva para visualizar "
        "el triángulo de potencias y el factor de potencia resultante."
    )

    c1, c2 = st.columns([1, 1])

    with c1:
        P = st.slider("Potencia Activa P (kW)",    min_value=0.1,  max_value=10.0, value=3.0, step=0.1)
        Q = st.slider("Potencia Reactiva Q (kVAR)", min_value=0.0,  max_value=10.0, value=4.0, step=0.1)
        tipo_Q = st.radio(
            "Naturaleza de Q:",
            ["Inductiva (Q > 0)", "Capacitiva (Q < 0)"],
            horizontal=True,
        )
        if "Capacitiva" in tipo_Q:
            Q = -Q

    # ── Cálculos ─────────────────────────────────────────────────────────────
    S   = np.sqrt(P**2 + Q**2)
    fp  = P / S if S > 0 else 1.0
    phi = np.degrees(np.arctan2(Q, P))

    with c2:
        m1, m2 = st.columns(2)
        m1.metric("Potencia Aparente S", f"{S:.3f} kVA")
        m2.metric("Factor de Potencia",  f"{fp:.4f}")
        m3, m4 = st.columns(2)
        m3.metric("Ángulo φ",            f"{phi:.2f}°")
        m4.metric("|Q|",                 f"{abs(Q):.2f} kVAR")

        # Barra de factor de potencia
        color_fp = "#55efc4" if fp > 0.9 else ("#ffd700" if fp > 0.7 else "#ff6b6b")
        st.markdown(f"""
        <div style='margin-top:8px;'>
          <div style='display:flex;justify-content:space-between;font-size:0.82em;color:#aaa;'>
            <span>fp = {fp:.3f}</span><span>{'✅ Bueno' if fp>0.9 else '⚠️ Mejorable' if fp>0.7 else '❌ Bajo'}</span>
          </div>
          <div style='background:#1a2a4a;border-radius:8px;height:14px;margin-top:4px;overflow:hidden;'>
            <div style='width:{fp*100:.1f}%;height:100%;background:{color_fp};border-radius:8px;
                        transition:width 0.3s;'></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Triángulo de potencias ────────────────────────────────────────────────
    fig = go.Figure()

    # Lados del triángulo
    vertices_x = [0, P, P, 0]
    vertices_y = [0, 0, Q, 0]

    # Relleno
    fig.add_trace(go.Scatter(
        x=vertices_x, y=vertices_y, fill="toself",
        fillcolor="rgba(0,212,255,0.07)", line=dict(color="rgba(0,0,0,0)"),
        showlegend=False, hoverinfo="skip",
    ))

    # Vector P (horizontal)
    fig.add_annotation(
        ax=0, ay=0, x=P, y=0, xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
        arrowcolor=_C["P"],
    )
    fig.add_trace(go.Scatter(
        x=[P / 2], y=[-S * 0.08],
        mode="text", text=[f"P = {P:.2f} kW"],
        textfont=dict(color=_C["P"], size=12), showlegend=False, hoverinfo="skip",
    ))

    # Vector Q (vertical)
    if abs(Q) > 0.01:
        fig.add_annotation(
            ax=P, ay=0, x=P, y=Q, xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
            arrowcolor=_C["Q"],
        )
        fig.add_trace(go.Scatter(
            x=[P + S * 0.06], y=[Q / 2],
            mode="text", text=[f"Q = {abs(Q):.2f} kVAR"],
            textfont=dict(color=_C["Q"], size=12), showlegend=False, hoverinfo="skip",
        ))

    # Vector S (hipotenusa)
    fig.add_annotation(
        ax=0, ay=0, x=P, y=Q, xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=2,
        arrowcolor=_C["S"],
    )
    fig.add_trace(go.Scatter(
        x=[P / 2 - S * 0.05], y=[Q / 2 + S * 0.05],
        mode="text", text=[f"S = {S:.3f} kVA"],
        textfont=dict(color=_C["S"], size=13, family="Segoe UI bold"),
        showlegend=False, hoverinfo="skip",
    ))

    # Arco φ
    if abs(phi) > 0.5:
        t_arc = np.linspace(0, np.radians(phi), 50)
        r_arc = S * 0.22
        fig.add_trace(go.Scatter(
            x=r_arc * np.cos(t_arc), y=r_arc * np.sin(t_arc),
            mode="lines", line=dict(color=_C["phi"], dash="dash", width=1.5),
            name=f"φ = {phi:.1f}°", showlegend=True,
        ))

    m = S * 0.3
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Triángulo de Potencias", font=dict(size=14, color="#aaa")),
        xaxis=dict(
            range=[-m * 0.3, P + m],
            zeroline=True, zerolinecolor="#2d4a6e",
            gridcolor=_C["grid"], title="P (kW)",
        ),
        yaxis=dict(
            range=[min(-m, Q - m * 0.3), max(m, Q + m * 0.3)],
            zeroline=True, zerolinecolor="#2d4a6e",
            gridcolor=_C["grid"], title="Q (kVAR)", scaleanchor="x",
        ),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# 3. SIMULADOR DE ONDA SENOIDAL
# ════════════════════════════════════════════════════════════════════════════
def _sim_onda():
    st.markdown("### 〰️ Visualizador de Onda Senoidal")
    st.caption(
        "Observa cómo la amplitud, frecuencia y fase modifican la forma de la señal. "
        "Activa la opción RMS para comparar con la continua equivalente."
    )

    c1, c2 = st.columns([1, 2])

    with c1:
        Am  = st.slider("Amplitud máxima Vm (V)", min_value=10.0,  max_value=400.0, value=141.4, step=0.1)
        f   = st.slider("Frecuencia f (Hz)",       min_value=1.0,   max_value=200.0, value=50.0,  step=1.0)
        phi = st.slider("Fase inicial φ (°)",       min_value=-180.0, max_value=180.0, value=0.0,  step=5.0)

        st.markdown("---")
        mostrar_rms     = st.checkbox("Mostrar línea V_rms",  value=True)
        mostrar_periodo = st.checkbox("Mostrar período T",     value=True)
        mostrar_pico    = st.checkbox("Mostrar valor pico",    value=True)
        dos_ciclos      = st.checkbox("Ver 2 ciclos completos", value=False)

    # ── Cálculos ─────────────────────────────────────────────────────────────
    Vrms = Am / np.sqrt(2)
    T    = 1 / f
    ciclos = 2 if dos_ciclos else 1
    t    = np.linspace(0, ciclos * T, 800)
    v    = Am * np.sin(2 * np.pi * f * t + np.radians(phi))

    with c1:
        st.markdown("**Resultados:**")
        st.metric("V_rms",     f"{Vrms:.2f} V")
        st.metric("Período T", f"{T*1000:.3f} ms")
        st.metric("V pico",    f"{Am:.1f} V")

    with c2:
        fig = go.Figure()

        # Zona de un período (fondo sombreado)
        if mostrar_periodo:
            fig.add_vrect(
                x0=0, x1=T * 1000,
                fillcolor="rgba(0,212,255,0.04)", layer="below", line_width=0,
            )
            fig.add_vline(
                x=T * 1000, line_dash="dot",
                line_color="#00d4ff", opacity=0.4,
                annotation_text=f"T = {T*1000:.2f} ms",
                annotation_font=dict(color="#00d4ff", size=11),
            )

        # Línea RMS
        if mostrar_rms:
            fig.add_hline(
                y=Vrms, line_dash="dash", line_color=_C["rms"], line_width=1.5,
                annotation_text=f"V_rms = {Vrms:.1f} V",
                annotation_font=dict(color=_C["rms"], size=11),
            )
            fig.add_hline(
                y=-Vrms, line_dash="dash", line_color=_C["rms"], line_width=1.5,
                opacity=0.5,
            )

        # Línea pico
        if mostrar_pico:
            fig.add_hline(
                y=Am, line_dash="dot", line_color="#ffd700", line_width=1,
                annotation_text=f"Vm = {Am:.1f} V",
                annotation_font=dict(color="#ffd700", size=11),
                annotation_position="bottom right",
            )

        # Onda principal
        fig.add_trace(go.Scatter(
            x=t * 1000, y=v,
            mode="lines",
            line=dict(color=_C["sin"], width=2.5),
            name=f"v(t) = {Am:.1f}·sin(2π·{f:.0f}t + {phi:.0f}°)",
            hovertemplate="t = %{x:.2f} ms<br>v = %{y:.2f} V<extra></extra>",
        ))

        # Eje de ceros
        fig.add_hline(y=0, line_color="#2d4a6e", line_width=1)

        fig.update_layout(
            **_LAYOUT,
            title=dict(text="Señal de Tensión Alterna", font=dict(size=14, color="#aaa")),
            xaxis=dict(
                title="Tiempo (ms)", gridcolor=_C["grid"],
                zeroline=False,
            ),
            yaxis=dict(
                title="Tensión (V)", gridcolor=_C["grid"],
                zeroline=False,
                range=[-Am * 1.25, Am * 1.25],
            ),
            height=380,
            legend=dict(orientation="h", yanchor="top", y=-0.15),
        )
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════
# RENDER PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════
def render():
    """Renderiza los simuladores interactivos de la Unidad 1."""

    st.markdown("## 📈 Simuladores Interactivos — Unidad 1")
    st.markdown(
        "Experimenta con los parámetros de cada circuito y observa "
        "cómo los valores y diagramas se actualizan al instante."
    )

    tab_rlc, tab_pot, tab_onda = st.tabs([
        "⚡ Circuito RLC",
        "🔺 Triángulo de Potencias",
        "〰️ Onda Senoidal",
    ])

    with tab_rlc:
        _sim_rlc()

    with tab_pot:
        _sim_potencias()

    with tab_onda:
        _sim_onda()