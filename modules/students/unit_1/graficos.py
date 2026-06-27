"""
Simulador de la Ley de Ohm - Unidad 1
Basado en la aplicacion del Dr. Maykop Perez Martinez
Universidad de Concepcion - Depto. Ingenieria Electrica

Replica completa en Streamlit puro:
- Corriente continua (DC) y alterna (AC)
- Configuraciones: serie, paralelo, mixto (3 sub-tipos)
- Diagrama fasorial interactivo
- Triangulo de potencias
- Forma de onda senoidal
- Sistema de feedback pedagogico (2 intentos + procedimiento)
- Casos predefinidos
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ---------------------------------------------------------------------------
# LAYOUT BASE
# ---------------------------------------------------------------------------
_LAYOUT = dict(
    paper_bgcolor="white",
    plot_bgcolor="#f8f9fa",
    font=dict(color="#333333", family="Segoe UI, sans-serif", size=12),
    margin=dict(l=48, r=24, t=36, b=40),
)
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
    "cos": "#e63946",
    "rms": "#e63946",
    "grid": "#e0e0e0",
}


# ---------------------------------------------------------------------------
# TARJETAS DE METRICAS RESPONSIVE
# ---------------------------------------------------------------------------
def _metric_cards(items, accent="#1d3557"):
    """
    items: lista de (label, value, unit)  -- unit puede ser "" si ya va en value
    Renderiza tarjetas en grid: 3 por fila en desktop, 2 en mobile.
    Fuente pequena para evitar truncamiento.
    """
    cards_html = ""
    for label, value, unit in items:
        cards_html += f"""
        <div class="mc">
          <div class="mc-label">{label}</div>
          <div class="mc-value">{value}<span class="mc-unit">{unit}</span></div>
        </div>"""

    html = f"""
    <style>
      .mc-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
        margin-bottom: 10px;
      }}
      @media (max-width: 600px) {{
        .mc-grid {{ grid-template-columns: repeat(2, 1fr); }}
      }}
      .mc {{
        background: #f0f2f6;
        border-radius: 8px;
        padding: 10px 12px 8px;
        border-left: 3px solid {accent};
      }}
      .mc-label {{
        font-size: 0.72rem;
        color: #6b7280;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 3px;
      }}
      .mc-value {{
        font-size: 1.05rem;
        font-weight: 700;
        color: #1f2937;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      .mc-unit {{
        font-size: 0.78rem;
        font-weight: 400;
        color: #6b7280;
        margin-left: 3px;
      }}
    </style>
    <div class="mc-grid">{cards_html}</div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# CALCULOS
# ---------------------------------------------------------------------------
def calcular_dc(V, R):
    I = V / R if R > 0 else 0
    P = V * I
    return dict(current=I, power=P, impedance=R, xl=0, xc=0,
                reactance=0, phase=0, power_factor=1,
                apparent_power=P, reactive_power=0, r_equiv=R)


def calcular_ac(V, R, f, L_mH, C_uF, config, mixed_config):
    w  = 2 * np.pi * f
    xl = w * L_mH / 1000
    xc = 1 / (w * C_uF / 1e6) if C_uF > 0 else 0

    if config == "serie":
        reactance = xl - xc
        Z = np.sqrt(R**2 + reactance**2)
        r_equiv = R

    elif config == "paralelo":
        gR = 1 / R if R > 0 else 0
        bL = -1 / xl if xl > 0 else 0
        bC =  1 / xc if xc > 0 else 0
        G  = gR
        B  = bL + bC
        Y  = np.sqrt(G**2 + B**2)
        Z  = 1 / Y if Y > 0 else R
        Y2 = G**2 + B**2
        r_equiv   = G / Y2 if Y2 > 0 else R
        reactance = -B / Y2 if Y2 > 0 else 0

    else:  # mixto
        if mixed_config == "R-parallel-LC":
            xs = xl - xc
            if abs(xs) > 0.001:
                denom = np.sqrt(R**2 + xs**2)
                Z = R * abs(xs) / denom
                r_equiv   = R * xs**2 / (R**2 + xs**2)
                reactance = R**2 * xs / (R**2 + xs**2)
            else:
                Z = R; r_equiv = R; reactance = 0
        elif mixed_config == "L-parallel-RC":
            zsr = R; zsx = -xc
            zsm = np.sqrt(zsr**2 + zsx**2)
            if xl > 0.001 and zsm > 0.001:
                yLb  = -1 / xl
                yRCg = zsr / zsm**2
                yRCb = -zsx / zsm**2
                G = yRCg; B = yLb + yRCb
                Y = np.sqrt(G**2 + B**2)
                Z = 1 / Y if Y > 0 else zsm
                Y2 = G**2 + B**2
                r_equiv   = G / Y2 if Y2 > 0 else zsr
                reactance = -B / Y2 if Y2 > 0 else zsx
            elif xl <= 0.001:
                Z = zsm; r_equiv = zsr; reactance = zsx
            else:
                Z = xl; r_equiv = 0; reactance = xl
        else:  # C-parallel-RL
            zsr = R; zsx = xl
            zsm = np.sqrt(zsr**2 + zsx**2)
            if xc > 0.001 and zsm > 0.001:
                yCb  = 1 / xc
                yRLg = zsr / zsm**2
                yRLb = -zsx / zsm**2
                G = yRLg; B = yCb + yRLb
                Y = np.sqrt(G**2 + B**2)
                Z = 1 / Y if Y > 0 else zsm
                Y2 = G**2 + B**2
                r_equiv   = G / Y2 if Y2 > 0 else zsr
                reactance = -B / Y2 if Y2 > 0 else zsx
            elif xc <= 0.001:
                Z = zsm; r_equiv = zsr; reactance = zsx
            else:
                Z = xc; r_equiv = 0; reactance = -xc

    I  = V / Z if Z > 0 else 0
    ph = np.degrees(np.arctan2(reactance, r_equiv))
    fp = r_equiv / Z if Z > 0 else 1
    Sa = V * I
    Pa = Sa * fp
    Qa = Sa * np.sin(np.radians(ph))
    return dict(current=I, power=Pa, impedance=Z, xl=xl, xc=xc,
                reactance=reactance, phase=ph, power_factor=fp,
                apparent_power=Sa, reactive_power=Qa, r_equiv=r_equiv)


def fmt(n, dec=3):
    if abs(n) >= 1000 or (abs(n) < 0.01 and n != 0):
        return f"{n:.2e}"
    return f"{n:.{dec}f}"


# ---------------------------------------------------------------------------
# GRAFICOS
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _onda_data(V, I, f, phase_deg, n_pts=300):
    T = 1 / f
    t = np.linspace(0, 2 * T, n_pts)
    v = V * np.sqrt(2) * np.sin(2 * np.pi * f * t)
    i = I * np.sqrt(2) * np.sin(2 * np.pi * f * t - np.radians(phase_deg))
    return t * 1000, v, i


def _grafico_fasorial(R_val, X_val, Z_val, phi):
    fig = go.Figure()
    m = Z_val * 0.35 + 5

    fig.add_shape(type="line", x0=R_val, y0=0, x1=R_val, y1=X_val,
                  line=dict(color="#cccccc", dash="dot", width=1))
    fig.add_shape(type="line", x0=0, y0=X_val, x1=R_val, y1=X_val,
                  line=dict(color="#cccccc", dash="dot", width=1))

    # Vector R: desde (0,0) hasta (R_val,0)
    fig.add_annotation(
        ax=0, ay=0, x=R_val, y=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2,
        arrowcolor=_C["R"],
        text=f"R={fmt(R_val, 1)} Ohm",
        font=dict(color=_C["R"], size=11),
        xanchor="center", yanchor="top",
        yshift=-8,
    )

    if abs(X_val) > 0.01:
        xc = _C["XL"] if X_val > 0 else _C["XC"]
        lbl = "XL" if X_val > 0 else "XC"
        # Vector XL/XC: desde (R_val,0) hasta (R_val,X_val)
        fig.add_annotation(
            ax=R_val, ay=0, x=R_val, y=X_val,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowwidth=2,
            arrowcolor=xc,
            text=f"{lbl}={fmt(abs(X_val), 1)} Ohm",
            font=dict(color=xc, size=11),
            xanchor="left", yanchor="middle",
            xshift=8,
        )

    # Vector Z: flecha desde (0,0) hasta (R_val,X_val)
    fig.add_annotation(
        ax=0, ay=0, x=R_val, y=X_val,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2.5,
        arrowcolor=_C["Z"],
        text="",
    )
    # Etiqueta Z posicionada en el punto medio del vector
    fig.add_annotation(
        x=R_val / 2, y=X_val / 2,
        xref="x", yref="y",
        showarrow=False,
        text=f"Z={fmt(Z_val, 2)} Ohm",
        font=dict(color=_C["Z"], size=12, weight="bold"),
        xshift=-14 if R_val > 0 else 14,
        yshift=10,
        xanchor="right" if R_val > 0 else "left",
        yanchor="bottom",
    )

    if abs(phi) > 0.5:
        t_arc = np.linspace(0, np.radians(phi), 30)
        r_arc = Z_val * 0.25
        fig.add_trace(go.Scatter(
            x=r_arc * np.cos(t_arc), y=r_arc * np.sin(t_arc),
            mode="lines", line=dict(color=_C["phi"], dash="dash", width=1.5),
            name=f"phi={phi:.1f} deg", showlegend=True,
        ))

    ymin = min(-m, X_val - m * 0.5)
    ymax = max(m, X_val + m * 0.5)
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Diagrama Fasorial de Impedancia", font=dict(size=13)),
        xaxis=dict(range=[-m * 0.15, R_val + m], zeroline=True,
                   zerolinecolor="#aaa", gridcolor=_C["grid"], title="R (Ohm)"),
        yaxis=dict(range=[ymin, ymax], zeroline=True, zerolinecolor="#aaa",
                   gridcolor=_C["grid"], title="X (Ohm)", scaleanchor="x"),
        height=340, legend=dict(orientation="h", y=-0.18),
    )
    return fig


def _grafico_potencias(P, Q, S):
    fig = go.Figure()
    m = S * 0.3 + 0.1

    fig.add_trace(go.Scatter(
        x=[0, P, P, 0], y=[0, 0, Q, 0],
        fill="toself", fillcolor="rgba(29,53,87,0.06)",
        line=dict(color="rgba(0,0,0,0)"), showlegend=False, hoverinfo="skip",
    ))

    # Vector P: desde (0,0) hasta (P,0)
    fig.add_annotation(
        ax=0, ay=0, x=P, y=0,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2,
        arrowcolor=_C["P"],
        text=f"P={fmt(P, 2)} W",
        font=dict(color=_C["P"], size=11),
        xanchor="center", yanchor="top",
        yshift=-8,
    )

    if abs(Q) > 0.01:
        # Vector Q: desde (P,0) hasta (P,Q)
        fig.add_annotation(
            ax=P, ay=0, x=P, y=Q,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=2, arrowwidth=2,
            arrowcolor=_C["Q"],
            text=f"Q={fmt(abs(Q), 2)} VAR",
            font=dict(color=_C["Q"], size=11),
            xanchor="left", yanchor="middle",
            xshift=8,
        )

    # Vector S: flecha desde (0,0) hasta (P,Q)
    fig.add_annotation(
        ax=0, ay=0, x=P, y=Q,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2.5,
        arrowcolor=_C["S"],
        text="",
    )
    # Etiqueta S posicionada en el punto medio del vector
    fig.add_annotation(
        x=P / 2, y=Q / 2,
        xref="x", yref="y",
        showarrow=False,
        text=f"S={fmt(S, 2)} VA",
        font=dict(color=_C["S"], size=12, weight="bold"),
        xshift=-14 if P > 0 else 14,
        yshift=10,
        xanchor="right" if P > 0 else "left",
        yanchor="bottom",
    )

    phi = np.degrees(np.arctan2(Q, P))
    if abs(phi) > 0.5:
        t_arc = np.linspace(0, np.radians(phi), 30)
        r_arc = S * 0.22
        fig.add_trace(go.Scatter(
            x=r_arc * np.cos(t_arc), y=r_arc * np.sin(t_arc),
            mode="lines", line=dict(color=_C["phi"], dash="dash", width=1.5),
            name=f"phi={phi:.1f} deg",
        ))
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Triangulo de Potencias", font=dict(size=13)),
        xaxis=dict(range=[-m * 0.15, P + m], zeroline=True,
                   zerolinecolor="#aaa", gridcolor=_C["grid"], title="P (W)"),
        yaxis=dict(range=[min(-m, Q - m * 0.3), max(m, Q + m * 0.3)],
                   zeroline=True, zerolinecolor="#aaa", gridcolor=_C["grid"],
                   title="Q (VAR)", scaleanchor="x"),
        height=320,
    )
    return fig


def _grafico_onda(t_ms, v, i, current_type):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_ms, y=v, mode="lines",
        line=dict(color=_C["sin"], width=2), name="v(t)",
        hovertemplate="t=%{x:.2f} ms<br>v=%{y:.2f} V<extra></extra>",
    ))
    if current_type == "AC":
        fig.add_trace(go.Scatter(
            x=t_ms, y=i * 50, mode="lines",
            line=dict(color=_C["cos"], width=1.8, dash="dash"),
            name="i(t) x50",
            hovertemplate="t=%{x:.2f} ms<br>i=%{y:.4f} A<extra></extra>",
        ))
    fig.add_hline(y=0, line_color="#aaa", line_width=1)
    fig.update_layout(
        **_LAYOUT,
        title=dict(text="Forma de Onda", font=dict(size=13)),
        xaxis=dict(title="Tiempo (ms)", gridcolor=_C["grid"]),
        yaxis=dict(title="Amplitud", gridcolor=_C["grid"]),
        height=300,
        legend=dict(orientation="h", y=-0.22),
    )
    return fig


# ---------------------------------------------------------------------------
# FEEDBACK PEDAGOGICO
# ---------------------------------------------------------------------------
def _feedback_corriente(user_val, res, current_type, config, attempt, V, R, f, L, C, xl, xc):
    correct = res["current"]
    is_ok   = abs(user_val - correct) < max(0.01 * correct, 0.001)

    if is_ok:
        if current_type == "DC":
            proc = [
                ("Datos",       f"V = {V} V, R = {R} Ohm"),
                ("Formula",     "Ley de Ohm: I = V / R"),
                ("Sustitucion", f"I = {V} / {R}"),
                ("Resultado",   f"I = {fmt(correct)} A"),
            ]
        else:
            proc = [
                ("Datos",       f"V={V} V, R={R} Ohm, f={f} Hz, L={L} mH, C={C} uF"),
                ("XL",          f"XL = 2*pi*f*L = {fmt(xl,3)} Ohm"),
                ("XC",          f"XC = 1/(2*pi*f*C) = {fmt(xc,3)} Ohm" if C > 0 else "XC = 0 Ohm (sin capacitor)"),
                ("Impedancia",  f"|Z| = {fmt(res['impedance'],3)} Ohm"),
                ("Corriente",   f"I = V / |Z| = {V} / {fmt(res['impedance'],3)} = {fmt(correct)} A"),
            ]
        return dict(ok=True, proc=proc)

    if attempt == 1:
        qs = (["Que relacion establece la Ley de Ohm entre voltaje, corriente y resistencia?",
               "Como despejas I de la formula V = I x R?",
               "Estas usando los valores correctos de V y R?"]
              if current_type == "DC" else
              ["En CA, la corriente depende de R o de la impedancia total |Z|?",
               "Has calculado primero la impedancia del circuito?",
               "Recuerdas que I = V / |Z|, no V / R?"])
        return dict(ok=False, attempt=1, questions=qs)

    if current_type == "DC":
        proc = [("Formula", "I = V / R"), ("Resultado", f"I = {fmt(correct)} A")]
    else:
        proc = [
            ("XL", f"{fmt(xl,3)} Ohm"),
            ("XC", f"{fmt(xc,3)} Ohm"),
            ("|Z|", f"{fmt(res['impedance'],3)} Ohm"),
            ("I = V/|Z|", f"{fmt(correct)} A"),
        ]
    return dict(ok=False, attempt=2, proc=proc, correct=fmt(correct) + " A")


def _feedback_impedancia(user_val, res, config, attempt, R, f, L, C, xl, xc):
    correct = res["impedance"]
    is_ok   = abs(user_val - correct) < max(0.1 * correct, 0.01)

    if is_ok:
        if config == "serie":
            proc = [
                ("XL",    f"XL = 2*pi*{f}*{L}/1000 = {fmt(xl,3)} Ohm"),
                ("XC",    f"XC = 1/(2*pi*{f}*{C}/1e6) = {fmt(xc,3)} Ohm" if C > 0 else "XC = 0"),
                ("X neta",f"X = XL - XC = {fmt(xl-xc,3)} Ohm"),
                ("|Z|",   f"Z = sqrt(R^2 + X^2) = {fmt(correct,3)} Ohm"),
            ]
        elif config == "paralelo":
            proc = [
                ("Admitancias", f"G=1/R={fmt(1/R,4)}, BL={fmt(-1/xl,4) if xl>0 else '0'}, BC={fmt(1/xc,4) if xc>0 else '0'}"),
                ("Y total",    "Y = sqrt(G^2 + B^2)"),
                ("|Z|",        f"Z = 1/Y = {fmt(correct,3)} Ohm"),
            ]
        else:
            proc = [
                ("Configuracion", f"Mixto {config}"),
                ("XL", f"{fmt(xl,3)} Ohm"),
                ("XC", f"{fmt(xc,3)} Ohm"),
                ("|Z|", f"{fmt(correct,3)} Ohm"),
            ]
        return dict(ok=True, proc=proc)

    if attempt == 1:
        qs = (["Como se combinan XL y XC en serie?",
               "Formula: |Z| = sqrt(R^2 + X^2) donde X = XL - XC",
               "Verificaste XL = 2*pi*f*L y XC = 1/(2*pi*f*C)?"]
              if config == "serie" else
              ["En paralelo se suman admitancias: Y = G + jB",
               "G = 1/R, BL = -1/XL, BC = 1/XC",
               "|Z| = 1/Y"])
        return dict(ok=False, attempt=1, questions=qs)

    proc = [("XL", fmt(xl,3)+" Ohm"), ("XC", fmt(xc,3)+" Ohm"), ("|Z|", fmt(correct,3)+" Ohm")]
    return dict(ok=False, attempt=2, proc=proc, correct=fmt(correct,3)+" Ohm")


def _feedback_fase(user_val, res, attempt):
    correct = res["phase"]
    is_ok   = abs(user_val - correct) < 0.5

    if is_ok:
        proc = [
            ("Reactancia neta", f"X = {fmt(res['reactance'],3)} Ohm"),
            ("R equiv",         f"Req = {fmt(res['r_equiv'],3)} Ohm"),
            ("Fase",            f"phi = arctan(X/R) = {fmt(correct,2)} deg"),
        ]
        return dict(ok=True, proc=proc)

    if attempt == 1:
        qs = ["La fase phi = arctan(X / R). Que valores estas usando?",
              "Recuerdas que phi > 0 es inductivo y phi < 0 es capacitivo?",
              "Para circuito paralelo, usa la reactancia equivalente vista desde los terminales."]
        return dict(ok=False, attempt=1, questions=qs)

    proc = [
        ("X neta", fmt(res["reactance"],3)+" Ohm"),
        ("R equiv", fmt(res["r_equiv"],3)+" Ohm"),
        ("phi", fmt(correct,2)+" deg"),
    ]
    return dict(ok=False, attempt=2, proc=proc, correct=fmt(correct,2)+" deg")


def _feedback_potencia(user_val, res, attempt, V, current_type):
    correct = res["power"]
    is_ok   = abs(user_val - correct) < max(0.1 * correct, 0.01)

    if is_ok:
        if current_type == "DC":
            proc = [("P = V * I", f"{V} * {fmt(res['current'],3)} = {fmt(correct,2)} W")]
        else:
            proc = [
                ("S = V * I",     f"{fmt(res['apparent_power'],3)} VA"),
                ("fp = cos(phi)", f"{fmt(res['power_factor'],4)}"),
                ("P = S * fp",    f"{fmt(correct,3)} W"),
            ]
        return dict(ok=True, proc=proc)

    if attempt == 1:
        qs = (["P = V * I para DC. Calculaste I correctamente?",
               "Recuerda que la potencia es el producto de voltaje por corriente."]
              if current_type == "DC" else
              ["En CA, la potencia activa P = S * fp = S * cos(phi)",
               "Calculaste primero S = V * I y luego fp = cos(phi)?",
               "Verificaste el angulo de fase phi?"])
        return dict(ok=False, attempt=1, questions=qs)

    proc = [("Respuesta correcta", fmt(correct,3)+" W")]
    return dict(ok=False, attempt=2, proc=proc, correct=fmt(correct,3)+" W")


# ---------------------------------------------------------------------------
# RENDER DE FEEDBACK
# ---------------------------------------------------------------------------
def _mostrar_feedback(fb, label):
    if fb is None:
        return
    if fb["ok"]:
        st.success(f"Correcto - {label}")
        with st.expander("Ver procedimiento completo"):
            for paso, detalle in fb["proc"]:
                st.markdown(f"**{paso}:** {detalle}")
    else:
        st.error(f"Incorrecto - {label}")
        if fb["attempt"] == 1:
            st.caption("Intento 1/2 - Reflexiona con estas preguntas antes de volver a intentar:")
            for q in fb["questions"]:
                st.markdown(f"- {q}")
        else:
            st.caption("Intento 2/2 - Procedimiento correcto:")
            for paso, detalle in fb["proc"]:
                st.markdown(f"**{paso}:** {detalle}")
            st.info(f"Respuesta correcta: {fb['correct']}")


# ---------------------------------------------------------------------------
# RENDER PRINCIPAL
# ---------------------------------------------------------------------------
def render():
    st.markdown("## Simulador de la Ley de Ohm")
    st.caption(
        "Desarrollado por Dr. Maykop Perez Martinez | "
        "Universidad de Concepcion - Depto. Ingenieria Electrica"
    )

    # Inicializar estado
    for k, v in [
        ("ohm_attempts", {"current": 0, "power": 0, "impedance": 0, "phase": 0}),
        ("ohm_show_fb", False),
        ("ohm_user_I", ""), ("ohm_user_P", ""),
        ("ohm_user_Z", ""), ("ohm_user_phi", ""),
    ]:
        if k not in st.session_state:
            st.session_state[k] = v

    # Panel de configuracion
    with st.expander("Configuracion del circuito", expanded=True):
        col_tipo, col_config = st.columns([1, 1])
        with col_tipo:
            current_type = st.radio("Tipo de corriente", ["DC", "AC"],
                                    horizontal=True, key="ohm_type")
        with col_config:
            if current_type == "AC":
                config = st.radio("Configuracion AC",
                                  ["serie", "paralelo", "mixto"],
                                  horizontal=True, key="ohm_config")
                if config == "mixto":
                    mixed_config = st.selectbox(
                        "Sub-tipo mixto",
                        ["R-parallel-LC", "L-parallel-RC", "C-parallel-RL"],
                        key="ohm_mixed"
                    )
                else:
                    mixed_config = "R-parallel-LC"
            else:
                config = "serie"
                mixed_config = "R-parallel-LC"

        # Casos predefinidos
        st.markdown("**Casos predefinidos:**")
        presets = {
            "Resistivo puro":    dict(V=120, R=50,  f=60, L=0,   C=0,    t="AC"),
            "Inductivo (motor)": dict(V=120, R=30,  f=60, L=100, C=0,    t="AC"),
            "Capacitivo":        dict(V=120, R=30,  f=60, L=0,   C=100,  t="AC"),
            "Resonancia":        dict(V=120, R=50,  f=60, L=265, C=26.5, t="AC"),
            "DC basico":         dict(V=12,  R=100, f=60, L=0,   C=0,    t="DC"),
        }
        cols_p = st.columns(len(presets))
        for i, (name, vals) in enumerate(presets.items()):
            if cols_p[i].button(name, key=f"ohm_preset_{i}", use_container_width=True):
                st.session_state["ohm_V"] = float(vals["V"])
                st.session_state["ohm_R"] = float(vals["R"])
                st.session_state["ohm_f"] = float(vals["f"])
                st.session_state["ohm_L"] = float(vals["L"])
                st.session_state["ohm_C"] = float(vals["C"])
                st.session_state["ohm_type"] = vals["t"]
                st.session_state["ohm_attempts"] = {"current": 0, "power": 0, "impedance": 0, "phase": 0}
                st.session_state["ohm_show_fb"] = False
                for k in ["ohm_user_I", "ohm_user_P", "ohm_user_Z", "ohm_user_phi"]:
                    st.session_state[k] = ""
                st.rerun()

    # Sliders de parametros
    c1, c2 = st.columns(2)
    with c1:
        V = st.slider("Voltaje V (V)",       1.0, 220.0,
                      float(st.session_state.get("ohm_V", 12.0)), 1.0, key="ohm_V")
        R = st.slider("Resistencia R (Ohm)", 1.0, 500.0,
                      float(st.session_state.get("ohm_R", 100.0)), 1.0, key="ohm_R")
    with c2:
        if current_type == "AC":
            f = st.slider("Frecuencia f (Hz)",   1.0, 200.0,
                          float(st.session_state.get("ohm_f", 60.0)), 1.0, key="ohm_f")
            L = st.slider("Inductancia L (mH)",  0.0, 500.0,
                          float(st.session_state.get("ohm_L", 0.0)),  1.0, key="ohm_L")
            C = st.slider("Capacitancia C (uF)", 0.0, 500.0,
                          float(st.session_state.get("ohm_C", 0.0)),  1.0, key="ohm_C")
        else:
            f = 60.0; L = 0.0; C = 0.0

    # Calculos
    if current_type == "DC":
        res = calcular_dc(V, R)
    else:
        res = calcular_ac(V, R, f, L, C, config, mixed_config)

    xl  = res["xl"]
    xc  = res["xc"]
    I   = res["current"]
    Z   = res["impedance"]
    ph  = res["phase"]
    P   = res["power"]
    Q   = res["reactive_power"]
    S   = res["apparent_power"]
    fp  = res["power_factor"]

    # ------------------------------------------------------------------
    # METRICAS: tarjetas HTML responsive en lugar de st.metric 6 columnas
    # ------------------------------------------------------------------
    st.markdown("---")
    st.markdown("### Resultados")

    if current_type == "DC":
        _metric_cards([
            ("Corriente I",  fmt(I),        " A"),
            ("Potencia P",   fmt(P, 2),     " W"),
            ("Resistencia",  f"{R:.1f}",    " Ohm"),
        ], accent="#1d3557")
    else:
        # Fila 1: magnitudes principales
        _metric_cards([
            ("|Z|",       fmt(Z, 2),          " Ohm"),
            ("I",         fmt(I, 4),          " A"),
            ("phi",       f"{ph:.2f}",        " deg"),
            ("fp",        f"{fp:.4f}",        ""),
            ("P activa",  fmt(P, 2),          " W"),
            ("Q reactiva",fmt(Q, 2),          " VAR"),
        ], accent="#1d3557")
        # Fila 2: reactancias
        _metric_cards([
            ("XL",    fmt(xl, 3),          " Ohm"),
            ("XC",    fmt(xc, 3) if C > 0 else "0",    " Ohm"),
            ("X neta",fmt(xl - xc, 3),    " Ohm"),
        ], accent="#457b9d")

        if abs(ph) < 1:
            st.success("Resonancia: XL = XC - Z minima, corriente maxima")
        elif ph > 0:
            st.info(f"Circuito Inductivo: corriente se atrasa {abs(ph):.1f} deg respecto al voltaje")
        else:
            st.info(f"Circuito Capacitivo: corriente adelanta {abs(ph):.1f} deg respecto al voltaje")

    # Graficos
    st.markdown("---")
    if current_type == "AC":
        tab_fas, tab_pot, tab_onda = st.tabs([
            "Diagrama Fasorial", "Triangulo de Potencias", "Forma de Onda"
        ])
        with tab_fas:
            st.plotly_chart(
                _grafico_fasorial(res["r_equiv"], res["reactance"], Z, ph),
                use_container_width=True, key="ohm_fasorial"
            )
        with tab_pot:
            st.plotly_chart(
                _grafico_potencias(P, Q, S),
                use_container_width=True, key="ohm_pot"
            )
        with tab_onda:
            t_ms, v_w, i_w = _onda_data(V, I, f, ph)
            st.plotly_chart(
                _grafico_onda(t_ms, v_w, i_w, current_type),
                use_container_width=True, key="ohm_onda"
            )
    else:
        t_ms, v_w, i_w = _onda_data(V, I, 60, 0)
        st.plotly_chart(
            _grafico_onda(t_ms, v_w, i_w, "DC"),
            use_container_width=True, key="ohm_onda_dc"
        )

    # Zona de practica
    st.markdown("---")
    st.markdown("### Practica: verifica tu comprension")
    st.caption(
        "Calcula los valores con lapiz y papel usando los parametros del circuito. "
        "Tienes 2 intentos por pregunta antes de ver el procedimiento completo."
    )

    prac_c1, prac_c2 = st.columns(2)
    with prac_c1:
        user_I = st.text_input("Tu respuesta para I (A):",
                               value=st.session_state["ohm_user_I"],
                               placeholder="Ej: 0.120", key="ohm_ui_I")
        user_P = st.text_input("Tu respuesta para P (W):",
                               value=st.session_state["ohm_user_P"],
                               placeholder="Ej: 14.4", key="ohm_ui_P")
    with prac_c2:
        if current_type == "AC":
            user_Z   = st.text_input("Tu respuesta para |Z| (Ohm):",
                                     value=st.session_state["ohm_user_Z"],
                                     placeholder="Ej: 100.0", key="ohm_ui_Z")
            user_phi = st.text_input("Tu respuesta para phi (deg):",
                                     value=st.session_state["ohm_user_phi"],
                                     placeholder="Ej: 45.0", key="ohm_ui_phi")
        else:
            user_Z = ""; user_phi = ""

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        verificar = st.button("Verificar respuestas", type="primary",
                              use_container_width=True, key="ohm_verificar")
    with col_btn2:
        if st.button("Reiniciar practica", use_container_width=True, key="ohm_reset"):
            st.session_state["ohm_attempts"] = {"current": 0, "power": 0, "impedance": 0, "phase": 0}
            st.session_state["ohm_show_fb"] = False
            for k in ["ohm_user_I", "ohm_user_P", "ohm_user_Z", "ohm_user_phi"]:
                st.session_state[k] = ""
            st.rerun()

    if verificar:
        att = st.session_state["ohm_attempts"]
        if user_I:   att["current"]   += 1; st.session_state["ohm_user_I"] = user_I
        if user_P:   att["power"]     += 1; st.session_state["ohm_user_P"] = user_P
        if current_type == "AC" and user_Z:
            att["impedance"] += 1; st.session_state["ohm_user_Z"] = user_Z
        if current_type == "AC" and user_phi:
            att["phase"] += 1; st.session_state["ohm_user_phi"] = user_phi
        st.session_state["ohm_attempts"] = att
        st.session_state["ohm_show_fb"] = True
        st.rerun()

    if st.session_state["ohm_show_fb"]:
        att   = st.session_state["ohm_attempts"]
        u_I   = st.session_state["ohm_user_I"]
        u_P   = st.session_state["ohm_user_P"]
        u_Z   = st.session_state["ohm_user_Z"]
        u_phi = st.session_state["ohm_user_phi"]

        if u_I:
            try:
                fb = _feedback_corriente(float(u_I), res, current_type, config,
                                         att["current"], V, R, f, L, C, xl, xc)
                _mostrar_feedback(fb, "Corriente I")
            except ValueError:
                st.warning("Ingresa un numero valido para I")

        if u_P:
            try:
                fb = _feedback_potencia(float(u_P), res, att["power"], V, current_type)
                _mostrar_feedback(fb, "Potencia P")
            except ValueError:
                st.warning("Ingresa un numero valido para P")

        if current_type == "AC" and u_Z:
            try:
                fb = _feedback_impedancia(float(u_Z), res, config, att["impedance"],
                                          R, f, L, C, xl, xc)
                _mostrar_feedback(fb, "Impedancia |Z|")
            except ValueError:
                st.warning("Ingresa un numero valido para Z")

        if current_type == "AC" and u_phi:
            try:
                fb = _feedback_fase(float(u_phi), res, att["phase"])
                _mostrar_feedback(fb, "Angulo de fase phi")
            except ValueError:
                st.warning("Ingresa un numero valido para phi")
