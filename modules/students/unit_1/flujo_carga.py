"""Flujo de Carga — Red de 2 Buses (Gauss-Seidel)."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ── MATEMÁTICA ────────────────────────────────────────────────────────────
def _cpolar(r, deg):
    return complex(r * np.cos(np.radians(deg)), r * np.sin(np.radians(deg)))


def _pol(c, d=4):
    return f"{abs(c):.{d}f} ∠ {np.degrees(np.angle(c)):.2f}°"


def _rect(c, d=4):
    s = "+" if c.imag >= 0 else "−"
    return f"{c.real:.{d}f} {s} j{abs(c.imag):.{d}f} pu"


def _solve(R, X, Pload, Qload, Qcap, V2mag, V2ang):
    """Gauss-Seidel. Bus 2 = slack (referencia), Bus 1 = PQ (carga).
    Ecuación: V1 = V2 + Z*I   =>   I = (V2 - V1) / Z
    """
    V2 = _cpolar(V2mag, V2ang)
    Z  = complex(R, X)
    S1 = complex(Pload, Qload - Qcap)   # potencia neta demandada en Bus 1

    if abs(Z) < 1e-9:
        I = np.conj(S1) / np.conj(V2) if abs(V2) > 1e-9 else 0j
        return dict(ok=True, iters=0, V1=V2, I=I,
                    S21=V2 * np.conj(I), Sloss=0j, V2=V2, dV=0j,
                    S_from=V2 * np.conj(I), S_to=V2 * np.conj(I))

    Y  = 1.0 / Z
    V1 = _cpolar(V2mag, 0.0)   # estimación inicial
    ok = False
    iters = 0
    for k in range(3000):
        V1_new = (np.conj(S1) / np.conj(V1) + V2 / Z) / Y
        err    = abs(V1_new - V1)
        V1     = V1_new
        iters  = k + 1
        if err < 1e-10:
            ok = True
            break

    # V1 = V2 + Z*I  =>  I = (V2 - V1) / Z
    I      = (V2 - V1) / Z
    # dV = Z*I = V2 - V1  (caída de tensión en la línea)
    dV     = Z * I                       # = V2 - V1
    S_from = V2 * np.conj(I)             # S2: potencia saliendo de Bus 2
    S_to   = V1 * np.conj(I)             # S21: potencia llegando a Bus 1
    I2     = abs(I) ** 2
    Sloss  = complex(I2 * R, I2 * X)
    return dict(ok=ok, iters=iters, V1=V1, I=I,
                S21=S_to, Sloss=Sloss, V2=V2, dV=dV,
                S_from=S_from, S_to=S_to)


# ── DIAGRAMA DEL CIRCUITO ───────────────────────────────────────────────────────
def _fig_circuito(r, R, X, Qcap):
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    dV = r["dV"]; Sf = r["S_from"]; St = r["S_to"]

    fig = go.Figure()
    N2x, N1x, Cy, ht = 1.5, 8.5, 4.0, 1.8
    Zmx = (N2x + N1x) / 2
    Zw, Zh = 1.4, 0.85

    def ln(x0, y0, x1, y1, color="#555", width=2):
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=color, width=width))

    def ann(x, y, txt, color="#333", size=9, xsh=0, ysh=0, anchor="center"):
        """Anotación sin flecha. Tamaño base reducido a 9px."""
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False,
                           font=dict(color=color, size=size),
                           xanchor=anchor, yanchor="middle",
                           xshift=xsh, yshift=ysh,
                           bgcolor="rgba(0,0,0,0)")

    # ─ Cable
    ln(N2x, Cy, N1x, Cy, "#1f77b4", 3)

    # ─ Barras verticales
    ln(N2x, Cy - ht, N2x, Cy + ht, "#ff7f0e", 6)
    ln(N1x, Cy - ht, N1x, Cy + ht, "#d62728", 6)

    # ─ Títulos nodos (11px bold)
    ann(N2x, Cy + ht + 0.5, "<b>Nodo 2</b>", "#ff7f0e", 11)
    ann(N1x, Cy + ht + 0.5, "<b>Nodo 1</b>", "#d62728", 11)

    # ─ Generador
    th = np.linspace(0, 2 * np.pi, 60)
    Gx, Gy, Gr = N2x - 1.6, Cy, 0.5
    fig.add_trace(go.Scatter(
        x=Gx + Gr * np.cos(th), y=Gy + Gr * np.sin(th),
        mode="lines", line=dict(color="#ff7f0e", width=2),
        fill="toself", fillcolor="white",
        showlegend=False, hoverinfo="skip",
    ))
    ann(Gx, Gy, "<b>~</b>", "#ff7f0e", 18)
    ln(Gx + Gr, Gy, N2x, Cy, "#ff7f0e", 2)

    # ─ Tierra Nodo 2
    ln(N2x, Cy - ht, N2x, Cy - ht - 0.28, "#555", 2)
    for w, dy in [(0.42, 0), (0.28, 0.16), (0.14, 0.32)]:
        ln(N2x - w/2, Cy - ht - 0.28 - dy,
           N2x + w/2, Cy - ht - 0.28 - dy, "#555", 2)

    # ─ Caja Z_línea
    fig.add_shape(type="rect",
                  x0=Zmx - Zw, y0=Cy - Zh, x1=Zmx + Zw, y1=Cy + Zh,
                  fillcolor="#eaf4fb", line=dict(color="#1f77b4", width=2))
    # Texto dentro de la caja: label pequeño arriba, valor bold abajo
    ann(Zmx, Cy + 0.35, "Z<sub>línea</sub> = R + jX", "#1f77b4", 9)
    sgn = "+" if X >= 0 else "−"
    ann(Zmx, Cy - 0.18, f"<b>{R:.2f} {sgn} j{abs(X):.2f} pu</b>", "#1a1a1a", 11)
    # ΔV bajo la caja
    ann(Zmx, Cy - Zh - 0.32, "ΔV<sub>línea</sub> = I · Z", "#555", 8)
    ann(Zmx, Cy - Zh - 0.65, f"{_pol(dV)}", "#2ca02c", 9)

    # ─ Corriente I (flecha sobre cable)
    fig.add_annotation(
        ax=N2x + 0.3, ay=Cy + 0.52,
        x=N1x - 0.3,  y=Cy + 0.52,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#17becf",
        text=f"<i>I</i> = {_pol(I)}",
        font=dict(color="#17becf", size=9),
        xanchor="center", yanchor="bottom", yshift=3,
    )

    # ─ Flujos S₂ (izq de caja) y S₂₁ (der de caja), bajo el cable
    Sm  = (N2x + Zmx) / 2
    Sm2 = (Zmx + N1x) / 2
    s2s  = "+" if Sf.imag >= 0 else "−"
    s21s = "+" if St.imag >= 0 else "−"

    # Flechas de flujo al nivel del cable
    fig.add_annotation(
        ax=N2x + 0.1, ay=Cy - 0.12,
        x=Zmx - Zw - 0.05, y=Cy - 0.12,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=1.2, arrowcolor="#888", text="",
    )
    fig.add_annotation(
        ax=Zmx + Zw + 0.05, ay=Cy - 0.12,
        x=N1x - 0.1, y=Cy - 0.12,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=1.2, arrowcolor="#888", text="",
    )
    # Labels de flujo (pequeños, sobre las flechas)
    ann(Sm,  Cy - 0.0, "S₂ =", "#666", 8)
    ann(Sm,  Cy - 0.28, f"{Sf.real:.3f} {s2s} j{abs(Sf.imag):.3f} pu", "#333", 8)
    ann(Sm2, Cy - 0.0, "S₂₁ =", "#666", 8)
    ann(Sm2, Cy - 0.28, f"{St.real:.3f} {s21s} j{abs(St.imag):.3f} pu", "#333", 8)

    # ─ Tensiones debajo de barras
    ann(N2x, Cy - ht - 0.9,  "V₂ =", "#888", 8)
    ann(N2x, Cy - ht - 1.25, f"<b>{_pol(V2, 2)}</b>", "#ff7f0e", 10)
    ann(N1x, Cy - ht - 0.9,  "V₁ =", "#888", 8)
    ann(N1x, Cy - ht - 1.25, f"<b>{_pol(V1, 4)}</b>", "#d62728", 10)

    # ─ Capacitor Qc (Nodo 1, arriba-derecha)
    Ccx = N1x + 1.1
    Ccy = Cy + ht + 0.5
    ln(N1x, Cy + ht,    N1x, Ccy - 0.2,  "#17becf", 2)
    ln(N1x, Ccy - 0.2,  Ccx, Ccy - 0.2,  "#17becf", 2)
    ln(Ccx, Ccy - 0.2,  Ccx, Ccy + 0.02, "#17becf", 2)
    for dy in [0.02, 0.2]:
        ln(Ccx - 0.35, Ccy + dy, Ccx + 0.35, Ccy + dy, "#17becf", 3)
    ann(Ccx, Ccy + 0.52, f"Q<sub>C</sub> = {Qcap:.2f} pu", "#17becf", 9)
    # Tierra capacitor
    ln(Ccx, Ccy + 0.22, Ccx, Ccy + 0.48, "#555", 2)
    for w, dy in [(0.35, 0), (0.23, 0.14), (0.11, 0.28)]:
        ln(Ccx - w/2, Ccy + 0.48 + dy,
           Ccx + w/2, Ccy + 0.48 + dy, "#555", 2)

    # ─ Carga P+jQ (Nodo 1, derecha)
    Lx0, Lx1 = N1x + 0.15, N1x + 1.65
    Ly0, Ly1 = Cy - 0.65, Cy + 0.4
    ln(N1x, Cy, Lx0, Cy, "#9467bd", 2)
    fig.add_shape(type="rect",
                  x0=Lx0, y0=Ly0, x1=Lx1, y1=Ly1,
                  fillcolor="#f5f0ff", line=dict(color="#9467bd", width=2))
    ann((Lx0 + Lx1) / 2, (Ly0 + Ly1) / 2 + 0.15,
        "P<sub>L</sub> + jQ<sub>L</sub>", "#9467bd", 9)
    S1d = r["S21"]
    s1s = "+" if S1d.imag >= 0 else "−"
    ann((Lx0 + Lx1) / 2, (Ly0 + Ly1) / 2 - 0.15,
        f"<b>{S1d.real:.2f} {s1s} j{abs(S1d.imag):.2f} pu</b>", "#1a1a1a", 9)

    # ─ Tierra Nodo 1
    ln(N1x, Cy - ht, N1x, Cy - ht - 0.28, "#555", 2)
    for w, dy in [(0.42, 0), (0.28, 0.16), (0.14, 0.32)]:
        ln(N1x - w/2, Cy - ht - 0.28 - dy,
           N1x + w/2, Cy - ht - 0.28 - dy, "#555", 2)

    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(range=[-0.5, 11.5], showgrid=False,
                   zeroline=False, showticklabels=False),
        yaxis=dict(range=[0.8, 7.5], showgrid=False,
                   zeroline=False, showticklabels=False,
                   scaleanchor="x", scaleratio=0.75),
        margin=dict(l=5, r=5, t=5, b=5),
        height=400,
        showlegend=False,
    )
    return fig


# ── DIAGRAMA FASORIAL ──────────────────────────────────────────────────────────
def _fig_fasorial(r):
    """Diagrama fasorial correcto:
    - V2 sale del origen (Bus 2 = slack, referencia)
    - V1 sale del origen (V1 = V2 + Z*I, calculado)
    - dV = Z*I = V2 - V1, va de la punta de V1 a la punta de V2
      (cierra el triángulo: O->V1 + V1->V2 = O->V2)
    - I escalado para visibilidad, misma dirección que el fasor I real
    """
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    # dV = Z*I = V2 - V1  =>  vector desde punta de V1 hasta punta de V2
    dV = V2 - V1

    # Escalar I para visualización (mismo ángulo, módulo comparable a V)
    scale = max(abs(V1), abs(V2)) * 0.6 / (abs(I) + 1e-9)
    Ip = I * scale

    fig = go.Figure()

    def vec(x0, y0, x1, y1, color, name, dash="solid"):
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(color=color, width=2.5, dash=dash),
            name=name, showlegend=True,
            hovertemplate=f"{name}<extra></extra>",
        ))
        fig.add_annotation(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowwidth=2.5,
            arrowcolor=color, arrowsize=1.0, text="",
        )
        fig.add_annotation(
            x=x1, y=y1, text=f"<b>{name}</b>",
            showarrow=False, font=dict(color=color, size=11),
            xshift=10, yshift=6,
        )

    # V2: del origen a la punta de V2 (Bus slack, referencia)
    vec(0, 0, V2.real, V2.imag, "#e07b7b", "V₂")
    # V1: del origen a la punta de V1 (tensión calculada Bus 1)
    vec(0, 0, V1.real, V1.imag, "#d62728", "V₁")
    # ΔV = Z·I = V2 - V1: de la punta de V1 a la punta de V2
    vec(V1.real, V1.imag, V2.real, V2.imag, "#17becf", "ΔV = Z·I")
    # I escalado: del origen, misma fase que I real
    vec(0, 0, Ip.real, Ip.imag, "#1f77b4", "I")

    # Punto en el origen
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers",
        marker=dict(size=7, color="#333"),
        showlegend=False, hoverinfo="skip",
    ))

    m = max(abs(V1), abs(V2), abs(Ip)) * 1.5 + 0.05
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(range=[-m, m], zeroline=True, zerolinecolor="#ccc",
                   zerolinewidth=1.5, showgrid=True, gridcolor="#f0f0f0",
                   title=dict(text="Re [pu]", font=dict(size=11))),
        yaxis=dict(range=[-m * 0.8, m * 0.8],
                   zeroline=True, zerolinecolor="#ccc", zerolinewidth=1.5,
                   showgrid=True, gridcolor="#f0f0f0",
                   title=dict(text="Im [pu]", font=dict(size=11)),
                   scaleanchor="x", scaleratio=1),
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(size=11)),
        margin=dict(l=50, r=20, t=35, b=60),
        height=360,
        title=dict(text="Diagrama Fasorial — Tensiones y Corriente",
                   font=dict(size=13), x=0.5),
    )
    return fig


# ── TABLA DE RESULTADOS (compacta) ────────────────────────────────────────────
def _tabla_resultados(r):
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    S21 = r["S21"]; Sl = r["Sloss"]; dV = r["dV"]
    eta = S21.real / (S21.real + Sl.real + 1e-12) * 100

    filas = [
        ("Tensión Bus 1",        "V₁ = V₂ + Z·I",            _pol(V1),     _rect(V1)),
        ("Corriente de línea",   "I = (V₂−V₁) / Z",          _pol(I),      _rect(I)),
        ("Pot. Activa P₂₁",      "Re(V₂ · I*)",               f"{S21.real:.5f} pu",  "—"),
        ("Pot. Reactiva Q₂₁",     "Im(V₂ · I*)",               f"{S21.imag:.5f} pu",  "—"),
        ("Pot. Aparente S₂₁",     "V₂ · I*",                    _pol(S21),    _rect(S21)),
        ("Caída de tensión ΔV",  "Z · I",                       _pol(dV),     _rect(dV)),
        ("Pérdidas activas",      "|I|² · R",                    f"{Sl.real:.6f} pu",  f"|I|²={abs(I)**2:.5f}"),
        ("Pérdidas reactivas",    "|I|² · X",                    f"{Sl.imag:.6f} pu",  f"η={eta:.2f}%"),
    ]
    df = pd.DataFrame(filas, columns=["Variable", "Expresión", "Polar / Valor", "Rectangular"])
    st.dataframe(df, use_container_width=True, hide_index=True)


# ── RENDER PRINCIPAL ────────────────────────────────────────────────────────────
def render():
    st.title("⚡ Flujo de Carga — Red de 2 Buses")
    st.caption(
        "Método de Gauss Seidel \u00a0|  **V₁ = V₂ + Z·I** \u00a0|  "
        "Sistema en valores por unidad [pu]"
    )
    st.caption(
        "Desarrollado por **Dr. Maykop Pérez Martínez** \u00a0|  "
        "Universidad de Concepción (UdeC) — Depto. Ingeniería Eléctrica"
    )
    st.divider()

    # Presets pendientes
    for src, dst in [
        ("_fc_R_p", "fc_R"), ("_fc_X_p", "fc_X"),
        ("_fc_P_p", "fc_P"), ("_fc_Q_p", "fc_Q"),
        ("_fc_Qc_p", "fc_Qc"), ("_fc_V_p", "fc_V"), ("_fc_A_p", "fc_A"),
    ]:
        if src in st.session_state:
            st.session_state[dst] = st.session_state.pop(src)

    col_param, col_diag = st.columns([1, 2], gap="large")

    with col_param:
        st.subheader("🎛️ Parámetros de la Red")
        st.markdown("**Línea de transmisión:** Z = R + jX [pu] \u00a0|  ΔV = Z·I")
        R = st.slider("R — Resistencia [pu]", 0.00, 0.50,
                      float(st.session_state.get("fc_R", 0.20)), 0.01,
                      key="fc_R", format="%.2f")
        X = st.slider("X — Reactancia [pu]", 0.00, 1.00,
                      float(st.session_state.get("fc_X", 0.74)), 0.01,
                      key="fc_X", format="%.2f")

        st.markdown("**Carga en Bus 1:** Scarga = PL + jQL [pu]\nCompensación: Qc (banco capacitivo)")
        Pload = st.slider("Pₗ — Potencia activa [pu]", 0.00, 2.00,
                          float(st.session_state.get("fc_P", 1.35)), 0.01,
                          key="fc_P", format="%.2f")
        Qload = st.slider("Qₗ — Potencia reactiva [pu]", -1.00, 2.00,
                          float(st.session_state.get("fc_Q", 1.00)), 0.01,
                          key="fc_Q", format="%.2f")
        Qcap  = st.slider("Qc — Banco capacitivo [pu]", 0.00, 2.00,
                          float(st.session_state.get("fc_Qc", 1.00)), 0.01,
                          key="fc_Qc", format="%.2f")

        st.markdown("**Bus 2 (barra slack):** V₂ = |V₂| ∠ δ₂ [pu]\nReferencia angular del sistema")
        V2mag = st.slider("|V₂| — Módulo [pu]", 0.80, 1.20,
                          float(st.session_state.get("fc_V", 0.98)), 0.01,
                          key="fc_V", format="%.2f")
        V2ang = st.slider("δ₂ — Ángulo [°]", -30.0, 10.0,
                          float(st.session_state.get("fc_A", 0.00)), 0.5,
                          key="fc_A", format="%.1f")

        st.divider()
        st.markdown("**Casos predefinidos:**")
        presets = {
            "Resistivo":  (0.00, 0.50, 0.50,  1.00, 1.00, 1.00,  0.0),
            "Inductivo":  (0.05, 0.30, 0.80,  0.60, 0.00, 0.95,  0.0),
            "Referencia": (0.20, 0.74, 1.35,  1.00, 1.00, 0.98,  0.0),
            "Alta carga": (0.10, 0.60, 1.20,  0.90, 0.80, 0.90, -5.0),
            "Capacitivo": (0.02, 0.40, 0.40, -0.30, 0.50, 1.00,  0.0),
        }
        keys = ["R", "X", "P", "Q", "Qc", "V", "A"]
        c1, c2 = st.columns(2)
        for i, (name, vals) in enumerate(presets.items()):
            col = c1 if i % 2 == 0 else c2
            if col.button(name, key=f"fc_pre_{i}", use_container_width=True):
                for k, v in zip(keys, vals):
                    st.session_state[f"_fc_{k}_p"] = float(v)
                st.rerun()

    r = _solve(R, X, Pload, Qload, Qcap, V2mag, V2ang)

    with col_diag:
        st.subheader("🔌 Diagrama del Circuito")
        st.plotly_chart(_fig_circuito(r, R, X, Qcap),
                        use_container_width=True, key="fc_circ")
        st.subheader("📐 Diagrama Fasorial")
        st.plotly_chart(_fig_fasorial(r),
                        use_container_width=True, key="fc_fas")

    st.divider()
    st.subheader("📊 Resultados")
    badge = "✅ Convergió" if r["ok"] else "❌ No convergió"
    st.caption(f"Gauss-Seidel \u00a0{badge} — {r['iters']} iteraciones \u00a0|  ε < 1×10⁻¹⁰")
    _tabla_resultados(r)

    st.divider()
    st.subheader("📐 Relaciones Fundamentales")
    rels = [
        ("TENSIÓN DE ENVÍO",     "V₁ = V₂ + Z · I"),
        ("POTENCIA RECIBIDA",    "S₂₁ = V₂ · I* = P₂₁ + jQ₂₁"),
        ("CORRIENTE DE LÍNEA",   "I = S₂₁* / V₂* = (V₂−V₁) / Z"),
        ("PÉRDIDAS EN LA LÍNEA", "S loss = |I|² · Z = P loss + jQ loss"),
        ("ADMITANCIA DE LÍNEA",  "Y = 1/Z = G + jB"),
        ("BALANCE DE POTENCIA",  "S gen = S carga + S loss"),
    ]
    cols = st.columns(3)
    for i, (name, eq) in enumerate(rels):
        with cols[i % 3]:
            st.info(f"**{name}**\n\n{eq}")
