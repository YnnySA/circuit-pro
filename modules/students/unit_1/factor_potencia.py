"""
Simulador de mejora del factor de potencia y propuesta de filtro.
Traducción funcional de factor_potencia_gui.m a Streamlit.
"""
import math

import streamlit as st


def _init_state():
    defaults = {
        "fp_q_antes": None,
        "fp_q_despues": None,
        "fp_qc": None,
        "fp_c_uf": None,
        "fp_c_f": None,
        "fp_f_hz": None,
        "fp_l_h": None,
        "fp_r_ohm": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def _safe_float(value: str):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _calcular_compensacion(p_kw: float, fp_actual: float, fp_deseado: float, u_v: float, f_hz: float):
    q_antes = p_kw * math.tan(math.acos(fp_actual))
    q_despues = p_kw * math.tan(math.acos(fp_deseado))
    qc = q_antes - q_despues
    c_uf = qc * 1e3 / (u_v**2 * 2 * math.pi * f_hz) * 1e6

    st.session_state["fp_q_antes"] = q_antes
    st.session_state["fp_q_despues"] = q_despues
    st.session_state["fp_qc"] = qc
    st.session_state["fp_c_uf"] = c_uf
    st.session_state["fp_c_f"] = c_uf * 1e-6
    st.session_state["fp_f_hz"] = f_hz


def _calcular_filtro(h: int, factor_q: float, tipo: str):
    c_f = st.session_state["fp_c_f"]
    f_hz = st.session_state["fp_f_hz"]

    w_h = 2 * math.pi * f_hz * h
    l_h = 1 / (w_h**2 * c_f)

    st.session_state["fp_l_h"] = l_h
    if tipo == "Filtro serie":
        st.session_state["fp_r_ohm"] = None
    else:
        st.session_state["fp_r_ohm"] = (w_h * l_h) / factor_q


def render():
    _init_state()

    st.markdown("## Mejora del factor de potencia y propuesta de filtro")
    st.caption(
        "Traducción del GUI MATLAB a Streamlit: cálculo de compensación reactiva y "
        "dimensionamiento básico de filtro por armónico."
    )

    st.markdown("### Datos del sistema industrial antes de la mejora")
    c1, c2 = st.columns(2)
    with c1:
        p_kw = _safe_float(st.text_input("Potencia Activa [kW]", key="fp_p_kw"))
        fp_actual = _safe_float(st.text_input("Factor de potencia actual", key="fp_actual"))
        u_v = _safe_float(st.text_input("Tensión del sistema [V]", key="fp_u_v"))
    with c2:
        fp_deseado = _safe_float(st.text_input("Factor de potencia deseado", key="fp_deseado"))
        f_hz = _safe_float(st.text_input("Frecuencia [Hz]", key="fp_f_hz_input"))

    if st.button("Resultados de la mejora del factor de potencia", type="primary"):
        if any(v is None for v in [p_kw, fp_actual, fp_deseado, u_v, f_hz]):
            st.error("Complete todos los campos de entrada.")
        elif fp_actual <= 0 or fp_actual >= 1:
            st.error("El factor de potencia actual debe estar en (0, 1).")
        elif fp_deseado <= 0 or fp_deseado > 1:
            st.error("El factor de potencia deseado debe estar en (0, 1].")
        elif fp_deseado <= fp_actual:
            st.error("El FP deseado debe ser mayor que el FP actual.")
        elif u_v <= 0 or f_hz <= 0:
            st.error("La tensión y la frecuencia deben ser valores positivos.")
        else:
            _calcular_compensacion(p_kw, fp_actual, fp_deseado, u_v, f_hz)

    q_antes = st.session_state["fp_q_antes"]
    q_despues = st.session_state["fp_q_despues"]
    qc = st.session_state["fp_qc"]
    c_uf = st.session_state["fp_c_uf"]

    r1, r2 = st.columns(2)
    with r1:
        st.text_input(
            "Potencia reactiva antes de la compensación [kvar]",
            value=f"{q_antes:.4f}" if q_antes is not None else "",
            disabled=True,
        )
        st.text_input(
            "Potencia reactiva del banco de condensadores [kvar]",
            value=f"{qc:.4f}" if qc is not None else "",
            disabled=True,
        )
    with r2:
        st.text_input(
            "Potencia reactiva después de la compensación [kvar]",
            value=f"{q_despues:.4f}" if q_despues is not None else "",
            disabled=True,
        )
        st.text_input(
            "Capacitancia del banco [µF]",
            value=f"{c_uf:.4f}" if c_uf is not None else "",
            disabled=True,
        )

    st.markdown("---")
    st.markdown("### Datos para propuesta de filtro")

    f1, f2 = st.columns(2)
    with f1:
        h = _safe_float(st.text_input("Orden del armónico a eliminar", key="fp_h"))
        tipo_filtro = st.selectbox(
            "Tipo de filtro",
            ["— Seleccione —", "Filtro serie", "Filtro paralelo", "Filtro pasa altos"],
            index=0,
        )
    with f2:
        q_factor = _safe_float(st.text_input("Factor de calidad (Q)", key="fp_q_factor"))

    if st.button("Resultados de la propuesta de filtro"):
        if st.session_state["fp_c_f"] is None:
            st.error("Primero calcule la compensación con el botón superior.")
        elif h is None or h < 1 or not float(h).is_integer():
            st.error("Ingrese un orden de armónico válido (entero ≥ 1).")
        elif tipo_filtro == "— Seleccione —":
            st.error("Seleccione un tipo de filtro.")
        elif tipo_filtro != "Filtro serie" and (q_factor is None or q_factor <= 0):
            st.error("Ingrese el factor de calidad Q (> 0) para este tipo de filtro.")
        else:
            _calcular_filtro(int(h), q_factor if q_factor is not None else 0.0, tipo_filtro)

    l_h = st.session_state["fp_l_h"]
    r_ohm = st.session_state["fp_r_ohm"]
    o1, o2 = st.columns(2)
    with o1:
        st.text_input(
            "Inductancia [H]",
            value=f"{l_h:.6f}" if l_h is not None else "",
            disabled=True,
        )
    with o2:
        st.text_input(
            "Resistencia [Ω]",
            value=("— (filtro LC)" if l_h is not None and r_ohm is None else (f"{r_ohm:.6f}" if r_ohm is not None else "")),
            disabled=True,
        )
