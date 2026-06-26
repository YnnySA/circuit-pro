"""
Módulo de ejercicios interactivos — Unidad 1: Circuitos Eléctricos
Contenido basado en material del Dr. Maykop Pérez Martínez,
Departamento de Ingeniería Eléctrica, Universidad de Concepción.
"""
import streamlit as st

from modules.students.unit_1 import cuestionarios


# ── Banco de ejercicios ───────────────────────────────────────────────────────
EJERCICIOS = [
    {
        "id": "ej1",
        "titulo": "Circuito serie con tres resistencias",
        "enunciado": (
            "Un circuito serie tiene una fuente de **48 V** y tres resistencias: "
            "$R_1 = 6\\,\\Omega$, $R_2 = 10\\,\\Omega$ y $R_3 = 8\\,\\Omega$. "
            "¿Cuál es la caída de tensión sobre $R_2$?"
        ),
        "opciones": ["V_R2 = 12 V", "V_R2 = 16 V", "V_R2 = 20 V", "V_R2 = 24 V"],
        "correcta": "V_R2 = 20 V",
        "explicacion": (
            "La resistencia total es $R_{eq} = 6 + 10 + 8 = 24\\,\\Omega$. "
            "La corriente es $I = 48/24 = 2$ A. "
            "La caída en $R_2$ es $V_{R_2} = I \\cdot R_2 = 2 \\times 10 = 20$ V. "
            "Alternativamente, por divisor de tensión: $V_{R_2} = 48 \\times 10/24 = 20$ V."
        ),
    },
    {
        "id": "ej2",
        "titulo": "Circuito paralelo — corriente de rama",
        "enunciado": (
            "Tres resistencias $R_1 = 12\\,\\Omega$, $R_2 = 6\\,\\Omega$ y $R_3 = 4\\,\\Omega$ "
            "están conectadas en paralelo a una fuente de **24 V**. "
            "¿Cuál es la corriente total entregada por la fuente?"
        ),
        "opciones": ["I_T = 4 A", "I_T = 8 A", "I_T = 12 A", "I_T = 14 A"],
        "correcta": "I_T = 12 A",
        "explicacion": (
            "En paralelo, la tensión es la misma en todas las ramas. "
            "Se calcula la corriente de cada rama: "
            "$I_1 = 24/12 = 2$ A, $I_2 = 24/6 = 4$ A, $I_3 = 24/4 = 6$ A. "
            "Aplicando LKC: $I_T = I_1 + I_2 + I_3 = 2 + 4 + 6 = 12$ A. "
            "También se puede verificar con la resistencia equivalente: "
            "$R_{eq} = \\frac{1}{1/12 + 1/6 + 1/4} = \\frac{1}{6/12} = 2\\,\\Omega$, "
            "luego $I_T = 24/2 = 12$ A."
        ),
    },
    {
        "id": "ej3",
        "titulo": "LKT — Malla con dos fuentes",
        "enunciado": (
            "En un lazo cerrado hay una fuente de **20 V**, otra fuente de **8 V** "
            "(opuesta a la primera) y dos resistencias: $R_1 = 3\\,\\Omega$ y $R_2 = 9\\,\\Omega$. "
            "Ambas fuentes y resistencias están en serie. "
            "¿Cuál es la corriente que circula por el lazo?"
        ),
        "opciones": ["I = 0,8 A", "I = 1,0 A", "I = 1,2 A", "I = 2,0 A"],
        "correcta": "I = 1,0 A",
        "explicacion": (
            "Aplicando la Ley de Kirchhoff de Tensiones (LKT) en el lazo: "
            "la tensión neta de las fuentes es $20 - 8 = 12$ V "
            "(se restan porque están en sentidos opuestos). "
            "La resistencia total del lazo es $R_{eq} = R_1 + R_2 = 3 + 9 = 12\\,\\Omega$. "
            "Por lo tanto: $I = V_{neta} / R_{eq} = 12 / 12 = 1{,}0$ A. "
            "La corriente que circula por el lazo es **1,0 A**."
        ),
    },
    {
        "id": "ej4",
        "titulo": "Valor RMS y potencia en CA",
        "enunciado": (
            "Una resistencia de $R = 50\\,\\Omega$ está alimentada por una señal senoidal "
            "con amplitud máxima $V_m = 141{,}4$ V. "
            "¿Qué potencia activa disipa la resistencia?"
        ),
        "opciones": ["P = 50 W", "P = 100 W", "P = 200 W", "P = 400 W"],
        "correcta": "P = 200 W",
        "explicacion": (
            "Primero se obtiene el valor RMS: $V_{rms} = 141{,}4 / \\sqrt{2} \\approx 100$ V. "
            "Como la carga es puramente resistiva ($fp = 1$), "
            "la potencia activa es $P = V_{rms}^2 / R = 100^2 / 50 = 200$ W. "
            "Recordar: en CA siempre se trabaja con valores RMS para calcular potencias."
        ),
    },
    {
        "id": "ej5",
        "titulo": "Impedancia de un circuito RL serie",
        "enunciado": (
            "Un circuito serie tiene $R = 30\\,\\Omega$ y una reactancia inductiva "
            "$X_L = 40\\,\\Omega$. "
            "¿Cuál es la magnitud de la impedancia total $|Z|$?"
        ),
        "opciones": ["|Z| = 35 Ω", "|Z| = 50 Ω", "|Z| = 70 Ω", "|Z| = 10 Ω"],
        "correcta": "|Z| = 50 Ω",
        "explicacion": (
            "La impedancia en forma compleja es $Z = R + jX_L = 30 + j40\\,\\Omega$. "
            "Su módulo se calcula como $|Z| = \\sqrt{R^2 + X_L^2} = \\sqrt{30^2 + 40^2} "
            "= \\sqrt{900 + 1600} = \\sqrt{2500} = 50\\,\\Omega$. "
            "Este es un triángulo 3-4-5 escalado por 10."
        ),
    },
    {
        "id": "ej6",
        "titulo": "Triángulo de potencia — potencia reactiva",
        "enunciado": (
            "Un circuito de CA consume una potencia activa de $P = 1{,}8$ kW "
            "y tiene una potencia aparente de $S = 3$ kVA. "
            "¿Cuál es la potencia reactiva $Q$ del circuito?"
        ),
        "opciones": ["Q = 1,2 kVAR", "Q = 2,0 kVAR", "Q = 2,4 kVAR", "Q = 3,6 kVAR"],
        "correcta": "Q = 2,4 kVAR",
        "explicacion": (
            "Por el triángulo de potencia: $S^2 = P^2 + Q^2$, despejando: "
            "$Q = \\sqrt{S^2 - P^2} = \\sqrt{3^2 - 1{,}8^2} = \\sqrt{9 - 3{,}24} "
            "= \\sqrt{5{,}76} = 2{,}4$ kVAR. "
            "El factor de potencia es $fp = P/S = 1{,}8/3 = 0{,}6$, "
            "lo que indica una carga con reactancia significativa."
        ),
    },
]


def render():
    """Renderiza el banco de ejercicios interactivos de la Unidad 1."""

    st.markdown("#### 🧪 Ejercicios Interactivos — Unidad 1")
    st.markdown(
        "Resuelve cada problema aplicando los conceptos de la guía teórica. "
        "Selecciona tu respuesta y recibe retroalimentación con el desarrollo completo."
    )

    # ── Inicializar estado ────────────────────────────────────────────────────
    if "ej_respondidos" not in st.session_state:
        st.session_state.ej_respondidos = {}
    if "ej_expanded" not in st.session_state:
        st.session_state.ej_expanded = {}

    # ── Contador de aciertos ──────────────────────────────────────────────────
    aciertos = sum(1 for v in st.session_state.ej_respondidos.values() if v)
    total_respondidos = len(st.session_state.ej_respondidos)

    if total_respondidos > 0:
        col_score, col_reset = st.columns([3, 1])
        with col_score:
            st.progress(
                aciertos / len(EJERCICIOS),
                text=f"Aciertos: {aciertos} / {len(EJERCICIOS)}",
            )
        with col_reset:
            if st.button("🔄 Reiniciar todos", use_container_width=True):
                st.session_state.ej_respondidos = {}
                st.session_state.ej_expanded = {}
                st.rerun()

    st.divider()

    # ── Ejercicios ────────────────────────────────────────────────────────────
    for i, ej in enumerate(EJERCICIOS):
        ej_key = ej["id"]
        ya_respondido = ej_key in st.session_state.ej_respondidos
        fue_correcto = st.session_state.ej_respondidos.get(ej_key, None)

        if not ya_respondido:
            icono = "⬜"
        elif fue_correcto:
            icono = "✅"
        else:
            icono = "❌"

        # Inicializar estado del expander si no existe
        if ej_key not in st.session_state.ej_expanded:
            st.session_state.ej_expanded[ej_key] = False

        with st.expander(
            f"{icono} Ejercicio {i + 1} — {ej['titulo']}",
            expanded=st.session_state.ej_expanded[ej_key],
        ):
            st.markdown(ej["enunciado"])
            st.write("")

            eleccion = st.radio(
                "Selecciona tu respuesta:",
                ej["opciones"],
                index=None,
                key=f"radio_{ej_key}",
                disabled=ya_respondido,
            )

            if not ya_respondido:
                if st.button(
                    "Verificar respuesta",
                    key=f"btn_{ej_key}",
                    type="primary",
                ):
                    if eleccion is None:
                        st.warning("Selecciona una opción antes de verificar.", icon="✋")
                    else:
                        correcto = eleccion == ej["correcta"]
                        st.session_state.ej_respondidos[ej_key] = correcto
                        st.session_state.ej_expanded[ej_key] = True  # mantener abierto
                        st.rerun()

            if ya_respondido:
                if fue_correcto:
                    st.success(f"✅ ¡Correcto! {ej['explicacion']}", icon="🎉")
                else:
                    st.error(
                        f"❌ Respuesta incorrecta. "
                        f"La correcta es **{ej['correcta']}**.\n\n"
                        f"{ej['explicacion']}",
                        icon="📖",
                    )

    # ── Cuestionarios formativos (selector) ──────────────────────────────────
    st.divider()
    cuestionarios.render()
