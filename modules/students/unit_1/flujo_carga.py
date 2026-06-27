"""Flujo de Carga — Red de 2 Buses (Gauss-Seidel)."""
import numpy as np
import plotly.graph_objects as go
import streamlit as st


# ── MATEMÁTICA ─────────────────────────────────────────────────────────────────
def _cpolar(r, deg):
    return complex(r * np.cos(np.radians(deg)), r * np.sin(np.radians(deg)))


def _pol(c, d=4):
    sign = "+" if np.degrees(np.angle(c)) >= 0 else ""
    return f"{abs(c):.{d}f} ∠ {np.degrees(np.angle(c)):.2f}°"


def _rect(c, d=4):
    s = "+" if c.imag >= 0 else "−"
    return f"{c.real:.{d}f} {s} j{abs(c.imag):.{d}f} pu"


def _solve(R, X, Pload, Qload, Qcap, V2mag, V2ang):
    """Gauss-Seidel para red de 2 buses. Bus 2 = slack, Bus 1 = PQ."""
    V2 = _cpolar(V2mag, V2ang)
    Z  = complex(R, X)
    # Potencia neta en Bus 1: carga − compensación capacitiva
    S1 = complex(Pload, Qload - Qcap)

    if abs(Z) < 1e-9:
        I = np.conj(S1) / np.conj(V2) if abs(V2) > 1e-9 else 0j
        return dict(ok=True, iters=0, V1=V2, I=I,
                    S21=V2*np.conj(I), Sloss=0j, V2=V2, dV=0j,
                    S_from=V2*np.conj(I), S_to=V2*np.conj(I))

    Y = 1.0 / Z
    V1 = _cpolar(V2mag, 0.0)
    ok = False
    iters = 0
    for k in range(3000):
        V1_new = (np.conj(S1) / np.conj(V1) + V2 / Z) / Y
        err = abs(V1_new - V1)
        V1 = V1_new
        iters = k + 1
        if err < 1e-10:
            ok = True
            break

    I      = (V2 - V1) / Z
    dV     = Z * I
    S_from = V2 * np.conj(I)   # S₂  potencia saliendo del Bus 2
    S_to   = V1 * np.conj(I)   # S₂₁ potencia llegando al Bus 1
    I2     = abs(I) ** 2
    Sloss  = complex(I2 * R, I2 * X)
    return dict(ok=ok, iters=iters, V1=V1, I=I,
                S21=S_to, Sloss=Sloss, V2=V2, dV=dV,
                S_from=S_from, S_to=S_to)


# ── DIAGRAMA DEL CIRCUITO ────────────────────────────────────────────────────────
def _fig_circuito(r, R, X, Qcap):
    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    dV = r["dV"]; Sf = r["S_from"]; St = r["S_to"]

    fig = go.Figure()

    # Posiciones
    N2x, N1x, Cy, ht = 1.5, 8.5, 4.0, 1.8
    Zmx = (N2x + N1x) / 2
    Zw, Zh = 1.3, 0.9

    def ln(x0, y0, x1, y1, color="#555", width=2):
        fig.add_shape(type="line", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color=color, width=width))

    def ann(x, y, txt, color="#222", size=11, xsh=0, ysh=0, anchor="center"):
        fig.add_annotation(x=x, y=y, text=txt, showarrow=False,
                           font=dict(color=color, size=size),
                           xanchor=anchor, yanchor="middle",
                           xshift=xsh, yshift=ysh,
                           bgcolor="rgba(0,0,0,0)")

    # Cable de transmisión
    ln(N2x, Cy, N1x, Cy, "#1f77b4", 3)

    # Barras verticales
    ln(N2x, Cy - ht, N2x, Cy + ht, "#ff7f0e", 6)
    ln(N1x, Cy - ht, N1x, Cy + ht, "#d62728", 6)

    # Títulos de nodos
    ann(N2x, Cy + ht + 0.55, "<b>Nodo 2</b>", "#ff7f0e", 13)
    ann(N1x, Cy + ht + 0.55, "<b>Nodo 1</b>", "#d62728", 13)

    # Generador (círculo)
    th = np.linspace(0, 2 * np.pi, 60)
    Gx, Gy, Gr = N2x - 1.6, Cy, 0.5
    fig.add_trace(go.Scatter(
        x=Gx + Gr * np.cos(th), y=Gy + Gr * np.sin(th),
        mode="lines", line=dict(color="#ff7f0e", width=2),
        fill="toself", fillcolor="white",
        showlegend=False, hoverinfo="skip",
    ))
    ann(Gx, Gy, "<b>~</b>", "#ff7f0e", 22)
    # Conexión generador → barra
    ln(Gx + Gr, Gy, N2x, Cy, "#ff7f0e", 2)

    # Tierra Nodo 2
    ln(N2x, Cy - ht, N2x, Cy - ht - 0.3, "#555", 2)
    for w, dy in [(0.45, 0), (0.3, 0.18), (0.15, 0.36)]:
        ln(N2x - w/2, Cy - ht - 0.3 - dy,
           N2x + w/2, Cy - ht - 0.3 - dy, "#555", 2)

    # Caja Z_línea
    fig.add_shape(type="rect",
                  x0=Zmx - Zw, y0=Cy - Zh, x1=Zmx + Zw, y1=Cy + Zh,
                  fillcolor="#eaf4fb",
                  line=dict(color="#1f77b4", width=2))
    ann(Zmx, Cy + 0.38, "Z<sub>línea</sub> = R + jX", "#1f77b4", 11)
    sgn = "+" if X >= 0 else "−"
    ann(Zmx, Cy - 0.2, f"<b>{R:.2f} {sgn} j{abs(X):.2f} pu</b>", "#222", 12)
    ann(Zmx, Cy - Zh - 0.38, "ΔV<sub>línea</sub> = I · Z", "#555", 10)
    ann(Zmx, Cy - Zh - 0.78, f"{_pol(dV)}", "#2ca02c", 10)

    # Corriente I (flecha sobre cable)
    fig.add_annotation(
        ax=N2x + 0.3, ay=Cy + 0.55,
        x=N1x - 0.3,  y=Cy + 0.55,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#17becf",
        text=f"<b><i>I</i> = {_pol(I)}</b>",
        font=dict(color="#17becf", size=11),
        xanchor="center", yanchor="bottom", yshift=4,
    )

    # Flujos S₂ y S₂₁
    Sm = (N2x + Zmx) / 2
    s2s = "+" if Sf.imag >= 0 else "−"
    ann(Sm, Cy + 0.2, "S₂ =", "#555", 9)
    ann(Sm, Cy - 0.18, f"{Sf.real:.3f} {s2s} j{abs(Sf.imag):.3f} pu", "#222", 9)
    fig.add_annotation(
        ax=N2x + 0.15, ay=Cy + 0.06,
        x=Zmx - Zw - 0.05, y=Cy + 0.06,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor="#555", text="",
    )

    Sm2 = (Zmx + N1x) / 2
    s21s = "+" if St.imag >= 0 else "−"
    ann(Sm2, Cy + 0.2, "S₂₁ =", "#555", 9)
    ann(Sm2, Cy - 0.18, f"{St.real:.3f} {s21s} j{abs(St.imag):.3f} pu", "#222", 9)
    fig.add_annotation(
        ax=Zmx + Zw + 0.05, ay=Cy + 0.06,
        x=N1x - 0.15,       y=Cy + 0.06,
        xref="x", yref="y", axref="x", ayref="y",
        showarrow=True, arrowhead=2, arrowwidth=1.5, arrowcolor="#555", text="",
    )

    # Tensiones debajo de barras
    ann(N2x, Cy - ht - 1.1, "V₂ =", "#555", 10)
    ann(N2x, Cy - ht - 1.55, f"<b>{_pol(V2, 2)}</b>", "#ff7f0e", 11)
    ann(N1x, Cy - ht - 1.1, "V₁ =", "#555", 10)
    ann(N1x, Cy - ht - 1.55, f"<b>{_pol(V1, 4)}</b>", "#d62728", 11)

    # Capacitor Qc (Nodo 1, arriba-derecha)
    Ccx = N1x + 1.2
    Ccy = Cy + ht + 0.55
    ln(N1x, Cy + ht,    N1x, Ccy - 0.22, "#17becf", 2)
    ln(N1x, Ccy - 0.22, Ccx, Ccy - 0.22, "#17becf", 2)
    ln(Ccx, Ccy - 0.22, Ccx, Ccy + 0.05, "#17becf", 2)
    for dy in [0.05, 0.25]:
        ln(Ccx - 0.38, Ccy + dy, Ccx + 0.38, Ccy + dy, "#17becf", 3)
    ann(Ccx, Ccy + 0.65, f"Q<sub>C</sub> = {Qcap:.2f} pu", "#17becf", 11)
    # Tierra capacitor
    ln(Ccx, Ccy + 0.28, Ccx, Ccy + 0.58, "#555", 2)
    for w, dy in [(0.38, 0), (0.25, 0.15), (0.13, 0.30)]:
        ln(Ccx - w/2, Ccy + 0.58 + dy,
           Ccx + w/2, Ccy + 0.58 + dy, "#555", 2)

    # Carga P+jQ (Nodo 1, derecha)
    Lx0, Lx1 = N1x + 0.2, N1x + 1.75
    Ly0, Ly1 = Cy - 0.75, Cy + 0.45
    ln(N1x, Cy, Lx0, Cy, "#9467bd", 2)
    fig.add_shape(type="rect",
                  x0=Lx0, y0=Ly0, x1=Lx1, y1=Ly1,
                  fillcolor="#f5f0ff",
                  line=dict(color="#9467bd", width=2))
    ann((Lx0+Lx1)/2, (Ly0+Ly1)/2 + 0.17, "P<sub>L</sub> + jQ<sub>L</sub>", "#9467bd", 11)
    S1disp = r["S21"]
    ann((Lx0+Lx1)/2, (Ly0+Ly1)/2 - 0.18,
        f"<b>{S1disp.real:.2f} + j{S1disp.imag:.2f} pu</b>", "#222", 11)

    # Tierra Nodo 1
    ln(N1x, Cy - ht, N1x, Cy - ht - 0.3, "#555", 2)
    for w, dy in [(0.45, 0), (0.3, 0.18), (0.15, 0.36)]:
        ln(N1x - w/2, Cy - ht - 0.3 - dy,
           N1x + w/2, Cy - ht - 0.3 - dy, "#555", 2)

    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(range=[-0.4, 11.2], showgrid=False,
                   zeroline=False, showticklabels=False),
        yaxis=dict(range=[0.6, 7.4], showgrid=False,
                   zeroline=False, showticklabels=False,
                   scaleanchor="x", scaleratio=0.85),
        margin=dict(l=10, r=10, t=10, b=10),
        height=430,
        showlegend=False,
    )
    return fig


# ── DIAGRAMA FASORIAL ───────────────────────────────────────────────────────────
def _fig_fasorial(r):
    V1 = r["V1"]; V2 = r["V2"]; dV = r["dV"]; I = r["I"]

    # Escalar I para que sea comparable con V
    scale = max(abs(V1), abs(V2)) * 0.65 / (abs(I) + 1e-9)
    Ip = I * scale

    fig = go.Figure()

    def vec(x0, y0, x1, y1, color, name):
        fig.add_trace(go.Scatter(
            x=[x0, x1], y=[y0, y1], mode="lines",
            line=dict(color=color, width=2.5),
            name=name, showlegend=True,
            hovertemplate=f"{name}<extra></extra>",
        ))
        fig.add_annotation(
            ax=x0, ay=y0, x=x1, y=y1,
            xref="x", yref="y", axref="x", ayref="y",
            showarrow=True, arrowhead=3, arrowwidth=2.5,
            arrowcolor=color, arrowsize=1.1, text="",
        )
        # Etiqueta junto a la punta
        fig.add_annotation(
            x=x1, y=y1, text=f"<b>{name}</b>",
            showarrow=False, font=dict(color=color, size=12),
            xshift=10, yshift=6,
        )

    vec(0, 0, V2.real, V2.imag, "#e07b7b", "V₂")
    vec(0, 0, V1.real, V1.imag, "#d62728", "V₁")
    vec(V2.real, V2.imag, V1.real, V1.imag, "#17becf", "ΔV = Z·I")
    vec(0, 0, Ip.real,  Ip.imag,  "#1f77b4", "I")

    # Punto en origen
    fig.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers",
        marker=dict(size=7, color="#333"),
        showlegend=False, hoverinfo="skip",
    ))

    m = max(abs(V1), abs(V2), abs(Ip)) * 1.45 + 0.05
    fig.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(range=[-m, m], zeroline=True, zerolinecolor="#bbb",
                   zerolinewidth=1.5, showgrid=True, gridcolor="#eee",
                   title=dict(text="Re [pu]", font=dict(size=12))),
        yaxis=dict(range=[-m * 0.8, m * 0.8],
                   zeroline=True, zerolinecolor="#bbb", zerolinewidth=1.5,
                   showgrid=True, gridcolor="#eee",
                   title=dict(text="Im [pu]", font=dict(size=12)),
                   scaleanchor="x", scaleratio=1),
        legend=dict(orientation="h", y=-0.18, x=0.5, xanchor="center",
                    font=dict(size=12)),
        margin=dict(l=50, r=20, t=20, b=60),
        height=370,
        title=dict(text="Diagrama Fasorial — Tensiones y Corriente",
                   font=dict(size=14), x=0.5),
    )
    return fig


# ── RENDER PRINCIPAL ───────────────────────────────────────────────────────────────
def render():
    # Título
    st.title("⚡ Flujo de Carga — Red de 2 Buses")
    st.caption(
        "Método de Gauss Seidel \u00a0|  **V₁ = V₂ + Z·I** \u00a0|  "
        "Sistema en valores por unidad [pu]"
    )
    st.caption(
        "Desarrollado por **Dr. Maykop Pérez Martínez**  |  "
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

    # ── LAYOUT: parámetros izq | diagramas der ────────────────────────────
    col_param, col_diag = st.columns([1, 2], gap="large")

    with col_param:
        st.subheader("🎛️ Parámetros de la Red")

        st.markdown("**Línea de transmisión:**  "
                    "**Z** = R + jX [pu] \u00a0|  Caída de tensión: **ΔV** = Z · I")
        R = st.slider("R — Resistencia [pu]", 0.00, 0.50,
                      float(st.session_state.get("fc_R", 0.20)), 0.01,
                      key="fc_R", format="%.2f")
        X = st.slider("X — Reactancia [pu]",  0.00, 1.00,
                      float(st.session_state.get("fc_X", 0.74)), 0.01,
                      key="fc_X", format="%.2f")

        st.markdown("**Carga en Bus 1:**  "
                    "S\u2093ₐᵣgₐ = Pₗ + jQₗ [pu]  "
                    "\nCompensación: **Qc** (banco capacitivo)")
        Pload = st.slider("Pₗ — Potencia activa [pu]",   0.00, 2.00,
                          float(st.session_state.get("fc_P", 1.35)), 0.01,
                          key="fc_P", format="%.2f")
        Qload = st.slider("Qₗ — Potencia reactiva [pu]", -1.00, 2.00,
                          float(st.session_state.get("fc_Q", 1.00)), 0.01,
                          key="fc_Q", format="%.2f")
        Qcap  = st.slider("Qc — Banco capacitivo [pu]",  0.00, 2.00,
                          float(st.session_state.get("fc_Qc", 1.00)), 0.01,
                          key="fc_Qc", format="%.2f")

        st.markdown("**Bus 2 (barra slack):**  "
                    "V₂ = |V₂| ∠ δ₂ [pu]  \n"
                    "Referencia angular del sistema")
        V2mag = st.slider("|V₂| — Módulo [pu]", 0.80, 1.20,
                          float(st.session_state.get("fc_V", 0.98)), 0.01,
                          key="fc_V", format="%.2f")
        V2ang = st.slider("δ₂ — Ángulo [°]",   -30.0, 10.0,
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

    # ── Resolver ───────────────────────────────────────────────────────────────
    r = _solve(R, X, Pload, Qload, Qcap, V2mag, V2ang)

    with col_diag:
        st.subheader("🔌 Diagrama del Circuito")
        st.plotly_chart(_fig_circuito(r, R, X, Qcap),
                        use_container_width=True, key="fc_circ")

        st.subheader("📐 Diagrama Fasorial")
        st.plotly_chart(_fig_fasorial(r),
                        use_container_width=True, key="fc_fas")

    # ── RESULTADOS (ancho completo) ──────────────────────────────────────────
    st.divider()
    st.subheader("📊 Resultados")

    V1 = r["V1"]; V2 = r["V2"]; I = r["I"]
    S21 = r["S21"]; Sl = r["Sloss"]; dV = r["dV"]

    badge = "✅ Convergió" if r["ok"] else "❌ No convergió"
    st.caption(f"Gauss-Seidel \u00a0{badge}\u00a0 — {r['iters']} iteraciones \u00a0|  ε < 1×10⁻¹⁰")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Tensión Bus 1 — V₁ = V₂ + Z·I",
                  _pol(V1), _rect(V1))
        st.metric("Pot. Activa Bus 2→1 — P₂₁",
                  f"{S21.real:.5f} pu", "Re(V₂ · I*)")
        st.metric("Pot. Aparente S₂₁",
                  _pol(S21), _rect(S21))
        st.metric("Pérdidas activas — P_loss = |I|²·R",
                  f"{Sl.real:.6f} pu", f"|I|² = {abs(I)**2:.5f}")
    with c2:
        st.metric("Corriente de línea — I = (V₂−V₁) / Z",
                  _pol(I), _rect(I))
        st.metric("Pot. Reactiva Bus 2→1 — Q₂₁",
                  f"{S21.imag:.5f} pu", "Im(V₂ · I*)")
        st.metric("Caída de tensión — ΔV = Z·I",
                  _pol(dV), _rect(dV))
        st.metric("Pérdidas reactivas — Q_loss = |I|²·X",
                  f"{Sl.imag:.6f} pu", f"η = {S21.real/(S21.real+Sl.real+1e-12)*100:.2f}%")

    # ── RELACIONES FUNDAMENTALES ──────────────────────────────────────────
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
