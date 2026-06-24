"""
Módulo de teoría — Unidad 1: Conceptos Básicos y Leyes de Circuitos Eléctricos
Contenido basado en material del Dr. Maykop Pérez Martínez,
Departamento de Ingeniería Eléctrica, Universidad de Concepción.
"""
import streamlit as st


def render():
    """Renderiza el contenido teórico completo de la Unidad 1."""

    st.markdown("### 📖 Teoría — Unidad 1: Circuitos Eléctricos")
    st.markdown(
        "Esta unidad cubre los fundamentos de la teoría de circuitos, "
        "desde los conceptos básicos hasta las leyes y métodos generales "
        "que rigen el análisis de redes eléctricas en CD y CA."
    )

    # ── SECCIÓN 1 ────────────────────────────────────────────────────────────
    with st.expander("⚡ 1. Circuito Eléctrico — Definición y propósito", expanded=True):
        st.markdown(
            """
Un **circuito eléctrico** es una interconexión de dispositivos eléctricos que forman
al menos una **trayectoria cerrada** para la circulación de corriente.
Su propósito fundamental es **comunicar o transferir energía** de un punto a otro.

Los elementos de un circuito se clasifican en dos grandes categorías:
"""
        )
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                """
**🔋 Elementos Activos**
- Capaces de *suministrar* energía o proporcionar ganancia
- Ejemplos: fuentes de tensión, fuentes de corriente, baterías, generadores
"""
            )
        with col2:
            st.markdown(
                """
**🔌 Elementos Pasivos**
- *Reciben* la energía y pueden disiparla o almacenarla
- Ejemplos: resistencias (R), bobinas (L), condensadores (C)
"""
            )

    # ── SECCIÓN 2 ────────────────────────────────────────────────────────────
    with st.expander("📏 2. Magnitudes Fundamentales"):
        st.markdown("### Carga Eléctrica")
        st.markdown(
            "Es una propiedad de las partículas atómicas y constituye el principio "
            "subyacente de todos los fenómenos eléctricos. Se mide en **coulombs (C)**."
        )
        st.markdown("### Corriente Eléctrica")
        st.markdown("Es la **tasa de cambio de la carga** en el tiempo:")
        st.latex(r"i(t) = \frac{dq}{dt} \quad \text{[Amperes, A]}")
        st.markdown("Se mide con un **amperímetro**, conectado **en serie** con el elemento.")

        st.markdown("### Tensión (Diferencia de Potencial)")
        st.markdown(
            "Es la energía necesaria para mover una unidad de carga entre dos puntos:"
        )
        st.latex(r"v_{ab} = \frac{dw}{dq} \quad \text{[Volts, V]}")
        st.markdown("Se mide con un **voltímetro**, conectado **en paralelo** al elemento.")

        st.markdown("### CD vs. CA")
        col_cd, col_ca = st.columns(2)
        with col_cd:
            st.info("**CD (Corriente Directa)**\n\nConstante en el tiempo. No cambia magnitud ni dirección.", icon="➡️")
        with col_ca:
            st.info("**CA (Corriente Alterna)**\n\nVaría sinusoidalmente. Invierte dirección y magnitud periódicamente.", icon="〰️")

    # ── SECCIÓN 3 ────────────────────────────────────────────────────────────
    with st.expander("〰️ 3. Onda Senoidal"):
        st.markdown("Una señal senoidal es una señal periódica caracterizada por:")
        st.latex(r"u(t) = U_m \cdot \text{sen}(\omega t + \theta)")
        st.markdown(
            """
| Símbolo | Nombre | Unidad |
|---|---|---|
| $U_m$ | Amplitud máxima | V o A |
| $\\omega$ | Frecuencia angular | rad/s |
| $\\theta$ | Fase inicial | rad o ° |
| $T$ | Período | s |
| $f$ | Frecuencia lineal | Hz |
"""
        )
        st.markdown("La relación entre frecuencia angular y frecuencia lineal es:")
        st.latex(r"\omega = 2\pi f = \frac{2\pi}{T}")

        st.markdown("### Valor Eficaz (RMS)")
        st.markdown(
            "Valor equivalente en CD que produce el mismo efecto térmico. "
            "Para señales sinusoidales:"
        )
        st.latex(r"U_{rms} = \frac{U_m}{\sqrt{2}} \approx 0{,}707 \cdot U_m")

    # ── SECCIÓN 4 ────────────────────────────────────────────────────────────
    with st.expander("🔄 4. Fasores y Dominio Frecuencial"):
        st.markdown(
            "Un **fasor** es un número complejo que representa una sinusoide "
            "en términos de su magnitud y fase, eliminando la dependencia del tiempo:"
        )
        st.latex(r"\mathbf{U} = U_m \angle \theta = U_m e^{j\theta} = U_m(\cos\theta + j\,\text{sen}\,\theta)")

        st.markdown("### Ley de Ohm Fasorial")
        st.latex(r"\mathbf{U} = \mathbf{Z} \cdot \mathbf{I}")
        st.markdown("Donde la **impedancia** $\\mathbf{Z}$ es:")
        st.latex(r"\mathbf{Z} = R + jX \quad \text{[}\Omega\text{]}")
        st.markdown("- $R$ = resistencia (parte real)\n- $X$ = reactancia (parte imaginaria)")

        st.markdown("### Comportamiento de L y C en CD")
        col_l, col_c = st.columns(2)
        with col_l:
            st.warning("**Inductor en CD** ($\\omega = 0$)\n\n$Z_L = j\\omega L = 0$ → **cortocircuito**", icon="🔌")
        with col_c:
            st.warning("**Condensador en CD** ($\\omega = 0$)\n\n$Z_C = 1/(j\\omega C) \\to \\infty$ → **circuito abierto**", icon="⭕")

    # ── SECCIÓN 5 ────────────────────────────────────────────────────────────
    with st.expander("🔋 5. Fuentes Eléctricas"):
        st.markdown("### Fuente Independiente Ideal de Tensión")
        st.markdown(
            "Mantiene una tensión específica en sus terminales, **independiente** "
            "de la corriente que el circuito le demande. Ejemplo: baterías de CD."
        )
        st.markdown("### Fuentes Dependientes (Controladas)")
        st.markdown("Su salida está determinada por otra variable del circuito. Existen **cuatro tipos**:")
        st.markdown(
            """
| Sigla | Nombre completo | Controlada por | Produce |
|---|---|---|---|
| **FTCT** | Fuente de Tensión Controlada por Tensión | Tensión | Tensión |
| **FTCC** | Fuente de Tensión Controlada por Corriente | Corriente | Tensión |
| **FCCT** | Fuente de Corriente Controlada por Tensión | Tensión | Corriente |
| **FCCC** | Fuente de Corriente Controlada por Corriente | Corriente | Corriente |
"""
        )
        st.markdown("### Transformación de Fuentes")
        st.markdown(
            "Convierte una **fuente de tensión en serie con Z** en una "
            "**fuente de corriente en paralelo con Z**, y viceversa. "
            "Son equivalentes en terminales, pero **no internamente**."
        )

    # ── SECCIÓN 6 ────────────────────────────────────────────────────────────
    with st.expander("🗺️ 6. Topología del Circuito"):
        st.markdown("""
- **Nodo:** Punto donde concurren dos o más ramas del circuito.
- **Rama:** Conjunto de elementos entre dos nodos consecutivos.
- **Lazo:** Cualquier trayectoria cerrada en el circuito.

Estos conceptos permiten identificar la estructura y las posibles
trayectorias de corriente en una red eléctrica.
""")

    # ── SECCIÓN 7 ────────────────────────────────────────────────────────────
    with st.expander("⚙️ 7. Conexión de Impedancias"):
        st.markdown("### En Serie")
        st.markdown("La corriente es la misma en todos los elementos. Las impedancias se suman:")
        st.latex(r"Z_{eq} = Z_1 + Z_2 + \cdots + Z_n")

        st.markdown("### En Paralelo")
        st.markdown("La tensión es la misma en todos los elementos:")
        st.latex(r"\frac{1}{Z_{eq}} = \frac{1}{Z_1} + \frac{1}{Z_2} + \cdots + \frac{1}{Z_n}")
        st.markdown("En términos de admitancia ($Y = 1/Z$, medida en siemens S):")
        st.latex(r"Y_{eq} = Y_1 + Y_2 + \cdots + Y_n")

    # ── SECCIÓN 8 ────────────────────────────────────────────────────────────
    with st.expander("📐 8. Leyes de Kirchhoff"):
        st.markdown("### LKC — Ley de Kirchhoff de Corriente (Nodos)")
        st.markdown("La suma algebraica de las corrientes que entran a un nodo es igual a cero:")
        st.latex(r"\sum_{k=1}^{n} i_k = 0")
        st.caption("Lo que entra debe salir. Se aplica en cada nodo del circuito.")

        st.markdown("### LKT — Ley de Kirchhoff de Tensión (Lazos)")
        st.markdown("La suma algebraica de las tensiones en cualquier lazo cerrado es igual a cero:")
        st.latex(r"\sum_{k=1}^{n} v_k = 0")
        st.caption("La energía suministrada por las fuentes es igual a la disipada en los elementos.")

    # ── SECCIÓN 9 ────────────────────────────────────────────────────────────
    with st.expander("✂️ 9. Divisores de Tensión y Corriente"):
        st.markdown("### Divisor de Tensión")
        st.markdown("La tensión se distribuye entre elementos en **serie** en proporción a sus impedancias:")
        st.latex(r"V_k = V_s \cdot \frac{Z_k}{Z_{eq}}")

        st.markdown("### Divisor de Corriente")
        st.markdown("La corriente se distribuye entre elementos en **paralelo** inversamente a sus impedancias:")
        st.latex(r"I_1 = I_s \cdot \frac{Z_2}{Z_1 + Z_2} \qquad I_2 = I_s \cdot \frac{Z_1}{Z_1 + Z_2}")

    # ── SECCIÓN 10 ───────────────────────────────────────────────────────────
    with st.expander("⚡ 10. Potencia en CA"):
        col_p, col_q, col_s = st.columns(3)
        with col_p:
            st.markdown("**Potencia Activa (P)**")
            st.latex(r"P = V_{rms}\,I_{rms}\cos\phi")
            st.caption("Watts (W). Potencia real disipada.")
        with col_q:
            st.markdown("**Potencia Reactiva (Q)**")
            st.latex(r"Q = V_{rms}\,I_{rms}\sin\phi")
            st.caption("VAR. Intercambio con L y C.")
        with col_s:
            st.markdown("**Potencia Aparente (S)**")
            st.latex(r"S = V_{rms}\,I_{rms} = \sqrt{P^2 + Q^2}")
            st.caption("VA. Producto RMS tensión × corriente.")

        st.markdown("### Factor de Potencia")
        st.latex(r"fp = \cos\phi = \frac{P}{S}")
        st.info(
            "$fp = 1$ → carga puramente resistiva (ideal). "
            "$fp$ bajo → presencia significativa de reactancia.",
            icon="💡",
        )