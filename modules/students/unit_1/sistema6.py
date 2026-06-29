"""
Sistema electrico industrial - Analisis de armonicos y filtros.
Traduccion funcional de sistema6_gui.m a Streamlit.
"""
import numpy as np
import plotly.graph_objects as go
import streamlit as st


def _init_state():
    defaults = {
        "s6_I_armonicos": None,
        "s6_Rc": None,
        "s6_Xlc": None,
        "s6_t_vec": None,
        "s6_f_v": None,
        "s6_n": None,
        "s6_Unom_v": None,
        "s6_thd_i_before": None,
        "s6_thd_u_before": None,
        "s6_thd_i_after": None,
        "s6_thd_u_after": None,
        "s6_fp_after": None,
        "s6_Icarga_before": None,
        "s6_Ucarga_before": None,
        "s6_Icarga_after": None,
        "s6_Ucarga_after": None,
        "s6_tipo_filtro": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _wave_chart(t_vec, y, title, y_label, color):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=t_vec * 1e3,
            y=y,
            mode="lines",
            line=dict(color=color, width=2),
            name=y_label,
        )
    )
    fig.update_layout(
        title=title,
        xaxis_title="Tiempo [ms]",
        yaxis_title=y_label,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=300,
        margin=dict(l=50, r=20, t=50, b=40),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(0,0,0,0.12)", griddash="dash")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.12)", griddash="dash")
    return fig


def _compute_prefilter(Pact_v, Qreact_v, Unom_v, f_v, I):
    n = I.shape[0]
    Rc = Unom_v**2 / (Pact_v * 1e3)
    Xlc = Unom_v**2 / (Qreact_v * 1e3)

    t_vec = np.linspace(0, 1 / f_v, 201)
    Ucarga = np.zeros_like(t_vec)
    Icarga = np.zeros_like(t_vec)
    Thu = np.zeros(n)
    Thi = np.zeros(n)

    for j in range(n):
        mod_I = I[j, 0]
        ang_I = np.deg2rad(I[j, 1])
        h_ord = I[j, 2]

        Ij = mod_I * (np.cos(ang_I) + 1j * np.sin(ang_I))
        U = Ij * (Rc + h_ord * Xlc * 1j)
        Zp = 10 * Rc + 10 * h_ord * Xlc * 1j
        Zc = Rc + h_ord * Xlc * 1j
        Urp = U * (Zp / (Zp + Zc))
        Irp = Urp / Zp

        mag_U = np.abs(Urp)
        ang_U = np.angle(Urp)
        mag_I = np.abs(Irp)
        ang_Ir = np.angle(Irp)

        Ucarga += mag_U * np.cos(h_ord * 2 * np.pi * f_v * t_vec + ang_U)
        Icarga += mag_I * np.cos(h_ord * 2 * np.pi * f_v * t_vec + ang_Ir)

        Thu[j] = mag_U
        Thi[j] = mag_I

    if Thi[0] == 0:
        thd_i = np.nan
    else:
        thd_i = np.sqrt(np.sum(Thi[1:] ** 2)) / Thi[0] * 100
    thd_u = np.sqrt(np.sum(Thu[1:] ** 2)) / Unom_v * 100

    return {
        "Rc": Rc,
        "Xlc": Xlc,
        "t_vec": t_vec,
        "Ucarga": Ucarga,
        "Icarga": Icarga,
        "Thu": Thu,
        "Thi": Thi,
        "thd_i": thd_i,
        "thd_u": thd_u,
        "n": n,
    }


def _compute_postfilter(I, Rc, Xlc, t_vec, f_v, Unom_v, L_mH, C_uF, R_ohm, tipo):
    n = I.shape[0]
    L_v = L_mH * 1e-3
    C_v = C_uF * 1e-6

    Xl = 2 * np.pi * f_v * L_v
    Xc = 1 / (2 * np.pi * f_v * C_v)

    Ucarga = np.zeros_like(t_vec)
    Icarga = np.zeros_like(t_vec)
    Thu = np.zeros(n)
    Thi = np.zeros(n)

    for j in range(n):
        mod_I = I[j, 0]
        ang_I = np.deg2rad(I[j, 1])
        h_ord = I[j, 2]

        Ij = mod_I * (np.cos(ang_I) + 1j * np.sin(ang_I))
        U = Ij * (Rc + h_ord * Xlc * 1j)
        Zc = Rc + h_ord * Xlc * 1j
        Zp = 10 * Zc

        Xlf_h = Xl * h_ord
        Xcf_h = Xc / h_ord

        if tipo == "serie":
            Irp = U * (1j * (Xl * h_ord - Xc / h_ord)) / (
                ((Zc + Zp) * (1j * (Xl * h_ord - Xc / h_ord))) + Xl * Xc
            )
            Urp = Irp * Zp
        elif tipo == "paralelo":
            Zf = R_ohm + (Xlf_h - Xcf_h) * 1j
            Zpar = (Zf * Zp) / (Zf + Zp)
            Ifuente = U / (Zpar + Zc)
            Irp = Ifuente * Zf / (Zp + Zf)
            Urp = Ifuente * Zpar
        else:
            Zf = (R_ohm * Xlf_h * 1j) / (R_ohm + Xlf_h * 1j) - Xcf_h * 1j
            Zpar = (Zf * Zp) / (Zf + Zp)
            Ifuente = U / (Zpar + Zc)
            Irp = Ifuente * Zf / (Zp + Zf)
            Urp = Ifuente * Zpar

        mag_U = np.abs(Urp)
        ang_U = np.angle(Urp)
        mag_Ir = np.abs(Irp)
        ang_Ir = np.angle(Irp)

        Ucarga += mag_U * np.cos(h_ord * 2 * np.pi * f_v * t_vec + ang_U)
        Icarga += mag_Ir * np.cos(h_ord * 2 * np.pi * f_v * t_vec + ang_Ir)

        Thu[j] = mag_U
        Thi[j] = mag_Ir

    if Thi[0] == 0:
        thd_i = np.nan
    else:
        thd_i = np.sqrt(np.sum(Thi[1:] ** 2)) / Thi[0] * 100
    thd_u = np.sqrt(np.sum(Thu[1:] ** 2)) / Unom_v * 100

    if tipo == "serie":
        Zf_fp = 1j * (Xl - Xc)
        Ztotal = Zf_fp + (Rc + Xlc * 1j)
    elif tipo == "paralelo":
        Zf_fp = R_ohm + (Xl - Xc) * 1j
        Ztotal = (Zf_fp * (Rc + Xlc * 1j)) / (Zf_fp + Rc + Xlc * 1j)
    else:
        Zf_fp = (R_ohm * Xl * 1j) / (R_ohm + Xl * 1j) - Xc * 1j
        Ztotal = (Zf_fp * (Rc + Xlc * 1j)) / (Zf_fp + Rc + Xlc * 1j)

    fp_mejorado = np.cos(np.angle(Ztotal))

    return {
        "Ucarga": Ucarga,
        "Icarga": Icarga,
        "thd_i": thd_i,
        "thd_u": thd_u,
        "fp_mejorado": fp_mejorado,
    }


def render():
    _init_state()

    st.markdown("## Sistema Eléctrico Industrial - Análisis de Armónicos")
    st.caption(
        "Traducción de sistema6_gui.m: cálculo de THD antes/después de filtro y "
        "factor de potencia mejorado."
    )

    st.markdown("### Datos del sistema")
    c1, c2, c3 = st.columns(3)
    with c1:
        pact = _safe_float(st.text_input("Potencia activa [kW]", key="s6_pact"))
        fp_in = _safe_float(st.text_input("Factor de potencia", key="s6_fp"))
    with c2:
        qreact = _safe_float(st.text_input("Potencia reactiva [kvar]", key="s6_qreact"))
        n_arm = _safe_float(st.text_input("Número de armónicos", key="s6_n_arm"))
    with c3:
        unom = _safe_float(st.text_input("Tensión nominal [V]", key="s6_unom"))
        f_hz = _safe_float(st.text_input("Frecuencia [Hz]", key="s6_f_hz"))

    st.markdown("### Corrientes armónicas (módulo, ángulo y orden)")
    if n_arm is None or n_arm < 1 or not float(n_arm).is_integer():
        st.info("Ingrese un número de armónicos entero (>= 1) para habilitar la tabla.")
        df = None
    else:
        n = int(n_arm)
        if "s6_arm_table" not in st.session_state or len(st.session_state["s6_arm_table"]) != n:
            st.session_state["s6_arm_table"] = [
                {"Modulo_A": 0.0, "Angulo_deg": 0.0, "Orden_h": 1.0} for _ in range(n)
            ]
        df = st.data_editor(
            st.session_state["s6_arm_table"],
            use_container_width=True,
            num_rows="fixed",
            key="s6_editor",
        )

    if st.button("Click para entrar las corrientes armónicas", type="primary"):
        if any(v is None for v in [pact, qreact, unom, f_hz, n_arm]):
            st.error("Complete todos los campos del sistema antes de continuar.")
        elif pact <= 0 or qreact <= 0 or unom <= 0 or f_hz <= 0:
            st.error("Potencias, tensión y frecuencia deben ser positivas.")
        elif n_arm < 1 or not float(n_arm).is_integer():
            st.error("Número de armónicos inválido (entero >= 1).")
        else:
            try:
                I = np.array(
                    [[row["Modulo_A"], row["Angulo_deg"], row["Orden_h"]] for row in df],
                    dtype=float,
                )
            except Exception:
                st.error("La tabla de armónicos tiene valores no válidos.")
                I = None

            if I is not None:
                pref = _compute_prefilter(pact, qreact, unom, f_hz, I)
                st.session_state["s6_I_armonicos"] = I
                st.session_state["s6_Rc"] = pref["Rc"]
                st.session_state["s6_Xlc"] = pref["Xlc"]
                st.session_state["s6_t_vec"] = pref["t_vec"]
                st.session_state["s6_f_v"] = f_hz
                st.session_state["s6_n"] = pref["n"]
                st.session_state["s6_Unom_v"] = unom
                st.session_state["s6_thd_i_before"] = pref["thd_i"]
                st.session_state["s6_thd_u_before"] = pref["thd_u"]
                st.session_state["s6_Icarga_before"] = pref["Icarga"]
                st.session_state["s6_Ucarga_before"] = pref["Ucarga"]
                st.success("Cálculo sin filtro completado.")

    thd_i_before = st.session_state["s6_thd_i_before"]
    thd_u_before = st.session_state["s6_thd_u_before"]
    r_before_1, r_before_2 = st.columns(2)
    with r_before_1:
        st.text_input(
            "THD de corriente antes de implementar el filtro",
            value="" if thd_i_before is None else f"{thd_i_before:.1f} %",
            disabled=True,
        )
    with r_before_2:
        st.text_input(
            "THD de tensión antes de implementar el filtro",
            value="" if thd_u_before is None else f"{thd_u_before:.1f} %",
            disabled=True,
        )

    st.markdown("---")
    st.markdown("### Parámetros del filtro")
    p1, p2 = st.columns(2)
    with p1:
        L_mH = _safe_float(st.text_input("Inductancia [mH]", key="s6_L_mH"))
        C_uF = _safe_float(st.text_input("Capacitancia [µF]", key="s6_C_uF"))
        R_ohm = _safe_float(st.text_input("Resistencia [Ω]", key="s6_R_ohm"))
    with p2:
        tipo_label = st.radio(
            "Variantes de filtro",
            ["Filtro serie", "Filtro paralelo", "Filtro pasa altos"],
            key="s6_tipo",
        )
        tipo = "serie" if tipo_label == "Filtro serie" else ("paralelo" if tipo_label == "Filtro paralelo" else "pasa")

    if st.button("Click resultados de la implementación del filtro"):
        I = st.session_state["s6_I_armonicos"]
        Rc = st.session_state["s6_Rc"]
        Xlc = st.session_state["s6_Xlc"]
        t_vec = st.session_state["s6_t_vec"]
        f_v = st.session_state["s6_f_v"]
        unom_v = st.session_state["s6_Unom_v"]

        if I is None:
            st.error("Primero ingrese las corrientes armónicas y calcule el caso sin filtro.")
        elif any(v is None for v in [L_mH, C_uF, R_ohm]):
            st.error("Complete los parámetros del filtro (L, C, R).")
        elif L_mH <= 0 or C_uF <= 0 or R_ohm <= 0:
            st.error("L, C y R deben ser mayores que 0.")
        else:
            post = _compute_postfilter(I, Rc, Xlc, t_vec, f_v, unom_v, L_mH, C_uF, R_ohm, tipo)
            st.session_state["s6_thd_i_after"] = post["thd_i"]
            st.session_state["s6_thd_u_after"] = post["thd_u"]
            st.session_state["s6_fp_after"] = post["fp_mejorado"]
            st.session_state["s6_Icarga_after"] = post["Icarga"]
            st.session_state["s6_Ucarga_after"] = post["Ucarga"]
            st.session_state["s6_tipo_filtro"] = tipo
            st.success("Cálculo con filtro completado.")

    thd_i_after = st.session_state["s6_thd_i_after"]
    thd_u_after = st.session_state["s6_thd_u_after"]
    fp_after = st.session_state["s6_fp_after"]

    r_after_1, r_after_2, r_after_3 = st.columns(3)
    with r_after_1:
        st.text_input(
            "THD de corrientes después de implementado el filtro",
            value="" if thd_i_after is None else f"{thd_i_after:.1f} %",
            disabled=True,
        )
    with r_after_2:
        st.text_input(
            "THD de tensión después de implementado el filtro",
            value="" if thd_u_after is None else f"{thd_u_after:.1f} %",
            disabled=True,
        )
    with r_after_3:
        st.text_input(
            "Factor de potencia después de implementado el filtro",
            value="" if fp_after is None else f"{fp_after:.4f}",
            disabled=True,
        )

    t_vec = st.session_state["s6_t_vec"]
    i_before = st.session_state["s6_Icarga_before"]
    u_before = st.session_state["s6_Ucarga_before"]
    i_after = st.session_state["s6_Icarga_after"]
    u_after = st.session_state["s6_Ucarga_after"]

    if t_vec is not None and i_before is not None and u_before is not None:
        st.markdown("### Formas de onda")
        tab_before, tab_after = st.tabs(["Sin filtro", "Con filtro"])
        with tab_before:
            st.plotly_chart(
                _wave_chart(
                    t_vec,
                    i_before,
                    "Corriente en la carga de prueba — contaminación armónica del sistema",
                    "Amplitud [A]",
                    "#1f77b4",
                ),
                use_container_width=True,
                key="s6_wave_i_before",
            )
            st.plotly_chart(
                _wave_chart(
                    t_vec,
                    u_before,
                    "Tensión en la carga de prueba — contaminación armónica del sistema",
                    "Amplitud [V]",
                    "#d62728",
                ),
                use_container_width=True,
                key="s6_wave_u_before",
            )

        with tab_after:
            if i_after is None or u_after is None:
                st.info("Aún no se calculó la implementación del filtro.")
            else:
                st.plotly_chart(
                    _wave_chart(
                        t_vec,
                        i_after,
                        f"Corriente en la carga de prueba — después del filtro {st.session_state['s6_tipo_filtro']}",
                        "Amplitud [A]",
                        "#1f77b4",
                    ),
                    use_container_width=True,
                    key="s6_wave_i_after",
                )
                st.plotly_chart(
                    _wave_chart(
                        t_vec,
                        u_after,
                        f"Tensión en la carga de prueba — después del filtro {st.session_state['s6_tipo_filtro']}",
                        "Amplitud [V]",
                        "#d62728",
                    ),
                    use_container_width=True,
                    key="s6_wave_u_after",
                )
