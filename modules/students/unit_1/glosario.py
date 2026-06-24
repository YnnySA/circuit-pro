"""
Módulo de glosario — Unidad 1: Términos de Circuitos Eléctricos
Contenido basado en material del Dr. Maykop Pérez Martínez,
Departamento de Ingeniería Eléctrica, Universidad de Concepción.
"""
import pandas as pd
import streamlit as st


# ── Datos del glosario ────────────────────────────────────────────────────────
TERMINOS = [
    # Glosario 1 — Conceptos básicos
    {
        "Término": "Admitancia (Y)",
        "Definición": "Inverso de la impedancia, medida en siemens (S). Es la razón entre la corriente y la tensión fasoriales.",
        "Unidad": "S (siemens)",
        "Categoría": "CA / Fasores",
    },
    {
        "Término": "Amperímetro",
        "Definición": "Instrumento de medición que cuantifica la corriente eléctrica. Se conecta siempre en serie con el elemento.",
        "Unidad": "—",
        "Categoría": "Instrumentos",
    },
    {
        "Término": "Conductancia (G)",
        "Definición": "Parte real de la admitancia. Representa la capacidad de un elemento para conducir corriente.",
        "Unidad": "S (siemens)",
        "Categoría": "CA / Fasores",
    },
    {
        "Término": "Fasor",
        "Definición": "Número complejo que representa una sinusoide en términos de su magnitud y fase inicial, eliminando la dependencia explícita del tiempo.",
        "Unidad": "—",
        "Categoría": "CA / Fasores",
    },
    {
        "Término": "Frecuencia Angular (ω)",
        "Definición": "Medida de la velocidad de variación de la sinusoide, expresada en radianes por segundo (rad/s). Se relaciona con la frecuencia lineal mediante ω = 2πf.",
        "Unidad": "rad/s",
        "Categoría": "Onda senoidal",
    },
    {
        "Término": "Impedancia (Z)",
        "Definición": "Oposición total al flujo de corriente en un circuito de CA, medida en ohms. Se compone de resistencia (parte real) y reactancia (parte imaginaria).",
        "Unidad": "Ω (ohms)",
        "Categoría": "CA / Fasores",
    },
    {
        "Término": "Reactancia (X)",
        "Definición": "Parte imaginaria de la impedancia. Puede ser inductiva (positiva, XL = ωL) o capacitiva (negativa, XC = −1/ωC).",
        "Unidad": "Ω (ohms)",
        "Categoría": "CA / Fasores",
    },
    {
        "Término": "Resistencia (R)",
        "Definición": "Parte real de la impedancia. Representa la transformación de energía eléctrica en energía calorífica (efecto Joule).",
        "Unidad": "Ω (ohms)",
        "Categoría": "Elementos pasivos",
    },
    # Glosario 2 — Redes de CA
    {
        "Término": "Circuito Abierto",
        "Definición": "Condición en la que la resistencia de una rama es infinita, lo que impide el paso de corriente por esa trayectoria.",
        "Unidad": "—",
        "Categoría": "Topología",
    },
    {
        "Término": "Cortocircuito",
        "Definición": "Condición en la que la resistencia de una rama es cero, obligando a toda la corriente a fluir por esa trayectoria de mínima oposición.",
        "Unidad": "—",
        "Categoría": "Topología",
    },
    {
        "Término": "Factor de Potencia (fp)",
        "Definición": "Coseno del ángulo de desfase entre la tensión y la corriente. Indica la eficiencia con que se convierte la potencia aparente en potencia activa. fp = cos(φ) = P/S.",
        "Unidad": "adimensional",
        "Categoría": "Potencia",
    },
    {
        "Término": "Fuente Dependiente",
        "Definición": "Elemento activo cuya salida (tensión o corriente) está determinada por el valor de otra variable en una parte distinta del circuito.",
        "Unidad": "—",
        "Categoría": "Fuentes",
    },
    {
        "Término": "Lazo",
        "Definición": "Cualquier trayectoria cerrada que se puede recorrer en un circuito eléctrico. Base de la Ley de Kirchhoff de Tensión (LKT).",
        "Unidad": "—",
        "Categoría": "Topología",
    },
    {
        "Término": "Ley de Ohm",
        "Definición": "Relación fundamental que vincula tensión, corriente e impedancia: U = Z · I. En CD: V = R · I.",
        "Unidad": "—",
        "Categoría": "Leyes",
    },
    {
        "Término": "Nodo",
        "Definición": "Punto de conexión donde se unen dos o más ramas de un circuito. Base de la Ley de Kirchhoff de Corriente (LKC).",
        "Unidad": "—",
        "Categoría": "Topología",
    },
    {
        "Término": "Potencia Aparente (S)",
        "Definición": "Producto de los valores RMS de la tensión y la corriente. S = Vrms · Irms = √(P² + Q²).",
        "Unidad": "VA (volt-ampere)",
        "Categoría": "Potencia",
    },
    {
        "Término": "Potencia Activa (P)",
        "Definición": "Potencia real disipada por la carga y suministrada útilmente. Depende de la resistencia del circuito. P = Vrms · Irms · cos(φ).",
        "Unidad": "W (watts)",
        "Categoría": "Potencia",
    },
    {
        "Término": "Potencia Instantánea",
        "Definición": "Producto de la tensión y la corriente en un momento específico del tiempo: p(t) = v(t) · i(t).",
        "Unidad": "W (watts)",
        "Categoría": "Potencia",
    },
    {
        "Término": "Potencia Reactiva (Q)",
        "Definición": "Mide el intercambio de energía sin pérdida entre la fuente y los elementos almacenadores (inductores y capacitores). Q = Vrms · Irms · sen(φ).",
        "Unidad": "VAR",
        "Categoría": "Potencia",
    },
    {
        "Término": "Rama",
        "Definición": "Segmento de un circuito que contiene uno o más elementos conectados entre dos nodos consecutivos.",
        "Unidad": "—",
        "Categoría": "Topología",
    },
    {
        "Término": "Valor RMS",
        "Definición": "Valor cuadrático medio que permite comparar los efectos térmicos de una señal alterna con una continua. Para sinusoides: Xrms = Xm / √2.",
        "Unidad": "V o A",
        "Categoría": "Onda senoidal",
    },
]

CATEGORIAS = ["Todas"] + sorted(set(t["Categoría"] for t in TERMINOS))


def render():
    """Renderiza el glosario interactivo de la Unidad 1."""

    st.markdown("#### 📚 Glosario de Términos — Unidad 1")
    st.markdown(
        "Consulta y filtra los términos clave de circuitos eléctricos. "
        f"**{len(TERMINOS)} términos** disponibles."
    )

    # ── Controles de filtro ───────────────────────────────────────────────────
    col_buscar, col_cat = st.columns([2, 1])
    with col_buscar:
        busqueda = st.text_input(
            "🔍 Buscar término",
            placeholder="Ej: impedancia, fasor, nodo...",
            label_visibility="collapsed",
        )
    with col_cat:
        categoria = st.selectbox(
            "Categoría",
            CATEGORIAS,
            label_visibility="collapsed",
        )

    # ── Filtrado ─────────────────────────────────────────────────────────────
    df = pd.DataFrame(TERMINOS)

    if categoria != "Todas":
        df = df[df["Categoría"] == categoria]

    if busqueda:
        mask = (
            df["Término"].str.contains(busqueda, case=False, na=False)
            | df["Definición"].str.contains(busqueda, case=False, na=False)
        )
        df = df[mask]

    # ── Resultado ─────────────────────────────────────────────────────────────
    if df.empty:
        st.warning("No se encontraron términos con esa búsqueda.", icon="🔍")
    else:
        st.caption(f"Mostrando {len(df)} término(s)")

        # Tarjetas individuales por término
        for _, row in df.iterrows():
            with st.container(border=True):
                col_term, col_unidad = st.columns([3, 1])
                with col_term:
                    st.markdown(f"**{row['Término']}**")
                with col_unidad:
                    st.caption(f"🏷️ {row['Categoría']}  ·  {row['Unidad']}")
                st.markdown(row["Definición"])
    
    st.markdown("#### 📚 Glosario de Términos — Unidad 2")
    