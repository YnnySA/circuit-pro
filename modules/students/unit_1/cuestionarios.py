"""
Módulo de cuestionarios formativos — Unidad 1: Circuitos Eléctricos
Contenido desarrollado por el Dr. Maykop Pérez Martínez,
Universidad de Concepción (UdeC) — Departamento de Ingeniería Eléctrica.

Replica la mecánica formativa de los cuestionarios HTML originales:
    • 2 intentos por pregunta (indicados con 2 "dots")
    • 1er error  -> se muestra una PISTA (sin revelar la respuesta), se permite reintentar
    • 2do error  -> se REVELA la respuesta correcta + explicación
    • acierto    -> felicitación + explicación ('ok')
    • retroalimentación específica por opción incorrecta cuando existe ('fb')
    • barra de progreso, navegación pregunta a pregunta y pantalla final de puntaje

El estado se gestiona con st.session_state, namespaced por cuestionario, de modo
que cada quiz mantiene su propio avance sin interferir con el banco de ejercicios
ni con el otro cuestionario.
"""
import re

import streamlit as st

from data.cuestionarios_data import CUESTIONARIOS, AUTOR


# ── Conversión de HTML inline a Markdown ──────────────────────────────────────
# Las pistas y explicaciones contienen <strong>, <em> y <sub>. Los componentes
# st.info / st.success / st.error renderizan Markdown (no HTML), por lo que
# convertimos esas etiquetas para que el énfasis se muestre correctamente.
def _html_a_md(texto: str) -> str:
    if not texto:
        return texto
    s = texto
    s = re.sub(r"</?strong>", "**", s)
    s = re.sub(r"</?em>", "*", s)
    # Subíndices: <sub>L</sub> -> _L  (notación legible para variables como Z_L)
    s = re.sub(r"<sub>(.*?)</sub>", r"_\1", s)
    # Limpiar cualquier otra etiqueta residual
    s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
    return s


# ── Estado por cuestionario ───────────────────────────────────────────────────
def _estado(qid: str) -> dict:
    """Devuelve (creando si hace falta) el diccionario de estado del cuestionario."""
    key = f"quiz_{qid}"
    if key not in st.session_state:
        st.session_state[key] = {
            "cur": 0,            # índice de la pregunta actual
            "score": 0,          # aciertos acumulados
            "attempts": 0,       # intentos fallidos en la pregunta actual (0, 1, 2)
            "locked": False,     # pregunta cerrada (acertada o respuesta revelada)
            "acertada": False,   # la pregunta actual se respondió correctamente
            "wrong_idx": [],     # índices de opciones marcadas como incorrectas
            "last_wrong": None,  # último índice incorrecto (para fb específico)
            "finished": False,   # cuestionario completado
        }
    return st.session_state[key]


def _reset_pregunta(estado: dict):
    """Reinicia el estado asociado a la pregunta actual."""
    estado["attempts"] = 0
    estado["locked"] = False
    estado["acertada"] = False
    estado["wrong_idx"] = []
    estado["last_wrong"] = None


def _reiniciar(qid: str):
    """Reinicia por completo el cuestionario."""
    st.session_state.pop(f"quiz_{qid}", None)
    # Limpiar también las claves de los radios de este cuestionario
    for k in list(st.session_state.keys()):
        if k.startswith(f"radio_{qid}_"):
            st.session_state.pop(k, None)


# ── Cabecera con atribución ───────────────────────────────────────────────────
def _cabecera(quiz: dict):
    st.markdown(
        f"""
        <div style="background:linear-gradient(90deg, rgba(11,95,255,0.06), rgba(0,194,209,0.06));
                    border:1px solid #E4E9F2; border-radius:14px;
                    padding:0.9rem 1.2rem; margin-bottom:1rem;">
            <div style="font-size:0.92rem; color:#0E1726;">
                Desarrollado por <strong style="color:#0B5FFF;">{AUTOR['nombre']}</strong>
            </div>
            <div style="font-size:0.84rem; color:#0891a0; font-weight:600;">{AUTOR['institucion']}</div>
            <div style="font-size:0.8rem; color:#5B6B82;">{AUTOR['departamento']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f"#### ⚡ {quiz['titulo']}")
    st.caption(quiz["descripcion"])


# ── Render de una pregunta ────────────────────────────────────────────────────
def _render_pregunta(qid: str, quiz: dict, estado: dict):
    preguntas = quiz["preguntas"]
    total = len(preguntas)
    cur = estado["cur"]
    p = preguntas[cur]
    letras = ["A", "B", "C", "D"]

    # Barra de progreso + etiqueta
    st.progress(cur / total, text=f"Pregunta {cur + 1} de {total}")

    # Indicador de intentos (dots)
    d1 = "🔴" if estado["attempts"] >= 1 else "⚪"
    d2 = "🔴" if estado["attempts"] >= 2 else "⚪"
    st.markdown(
        f"<div style='font-size:0.82rem;color:#5B6B82;margin:0.2rem 0 0.6rem 0;'>"
        f"Intentos: {d1} {d2}</div>",
        unsafe_allow_html=True,
    )

    # Enunciado (permite HTML inline: <strong>, <em>, sub/sup)
    st.markdown(
        f"<div style='font-size:1.05rem;color:#0E1726;line-height:1.6;"
        f"margin-bottom:0.6rem;'>{p['q']}</div>",
        unsafe_allow_html=True,
    )

    # Opciones como radio. Se etiquetan A) ... D) y se permite HTML.
    radio_key = f"radio_{qid}_{cur}"
    opciones_lbl = [f"{letras[i]})  {op}" for i, op in enumerate(p["opciones"])]

    eleccion = st.radio(
        "Selecciona tu respuesta:",
        options=list(range(len(p["opciones"]))),
        format_func=lambda i: opciones_lbl[i],
        index=None,
        key=radio_key,
        disabled=estado["locked"],
        label_visibility="collapsed",
    )

    # Botón verificar (solo si la pregunta no está cerrada)
    if not estado["locked"]:
        if st.button("Verificar respuesta", key=f"btn_{qid}_{cur}", type="primary"):
            if eleccion is None:
                st.warning("Selecciona una opción antes de verificar.", icon="✋")
            else:
                _verificar(estado, p, eleccion)
                st.rerun()

    # ── Retroalimentación formativa ──────────────────────────────────────────
    if estado["attempts"] >= 1 and not estado["acertada"] and not estado["locked"]:
        # 1er error -> pista (la pregunta sigue abierta)
        st.info(f"💡 **Pista:** {_html_a_md(p['pista'])}", icon="💡")

    if estado["acertada"]:
        st.success(f"✓ ¡Correcto! {_html_a_md(p['ok'])}", icon="🎉")

    elif estado["locked"] and not estado["acertada"]:
        # 2do error -> revelar respuesta correcta + explicación
        correcta_lbl = letras[p["correcta"]]
        extra = ""
        li = estado["last_wrong"]
        if li is not None and li < len(p["fb"]) and p["fb"][li].strip():
            extra = f"\n\n*Tu elección:* {_html_a_md(p['fb'][li])}"
        st.error(
            f"⚠️ **La respuesta correcta es la opción {correcta_lbl}.**\n\n"
            f"{_html_a_md(p['ok'])}{extra}",
            icon="📖",
        )

    # Botón siguiente / finalizar (cuando la pregunta está cerrada)
    if estado["locked"]:
        es_ultima = cur == total - 1
        label = "🏁 Ver resultado" if es_ultima else "Siguiente pregunta →"
        if st.button(label, key=f"next_{qid}_{cur}", type="primary"):
            if es_ultima:
                estado["finished"] = True
            else:
                estado["cur"] += 1
                _reset_pregunta(estado)
            st.rerun()


def _verificar(estado: dict, p: dict, eleccion: int):
    """Aplica la lógica de 2 intentos sobre la elección del usuario."""
    if eleccion == p["correcta"]:
        estado["acertada"] = True
        estado["locked"] = True
        estado["score"] += 1
    else:
        estado["attempts"] += 1
        estado["last_wrong"] = eleccion
        if eleccion not in estado["wrong_idx"]:
            estado["wrong_idx"].append(eleccion)
        if estado["attempts"] >= 2:
            # 2do error -> se revela la respuesta y se cierra la pregunta
            estado["locked"] = True


# ── Pantalla de puntaje final ─────────────────────────────────────────────────
def _mensaje_final(qid: str, score: int, total: int):
    """Reproduce los rangos de retroalimentación de los HTML originales."""
    pct = score / total
    if score == total:
        return "🌟 Dominio completo", (
            "Respondiste correctamente todas las preguntas. Tienes un sólido "
            "dominio de los conceptos fundamentales."
        )
    # Umbrales relativos coherentes con ambos cuestionarios originales
    if pct >= 0.7:
        return "💯 Muy buen desempeño", (
            "Excelente nivel. Revisa los pocos conceptos donde tuviste dificultad "
            "para consolidar tu aprendizaje."
        )
    if pct >= 0.5:
        return "📚 Desempeño aceptable", (
            "Conoces los conceptos fundamentales, pero hay áreas que requieren "
            "refuerzo. Repasa las leyes de Kirchhoff, transformaciones de fuentes "
            "y potencia en CA."
        )
    return "🔄 Necesitas repasar los contenidos", (
        "Te recomendamos revisar topología de circuitos, leyes de Kirchhoff, "
        "divisores, transformaciones y potencia antes de intentarlo nuevamente."
    )


def _render_resultado(qid: str, quiz: dict, estado: dict):
    total = len(quiz["preguntas"])
    score = estado["score"]
    sub, msg = _mensaje_final(qid, score, total)

    st.progress(1.0, text="Cuestionario completado")
    st.markdown(
        f"""
        <div style="text-align:center; background:#FFFFFF; border:1px solid #E4E9F2;
                    border-radius:18px; padding:2.4rem 1.5rem; margin:0.6rem 0;">
            <div style="font-size:3.4rem; font-weight:900; color:#0B5FFF; line-height:1;">
                {score}/{total}
            </div>
            <div style="font-size:1.15rem; color:#0891a0; font-weight:600; margin-top:0.5rem;">
                {sub}
            </div>
            <div style="font-size:0.95rem; color:#5B6B82; max-width:540px;
                        margin:0.8rem auto 0; line-height:1.6;">
                {msg}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("↻ Intentar nuevamente", key=f"restart_{qid}", type="primary"):
        _reiniciar(qid)
        st.rerun()


# ── API pública ───────────────────────────────────────────────────────────────
def render():
    """Renderiza el selector de cuestionarios formativos y el quiz activo."""
    st.markdown("#### 📝 Cuestionarios formativos — Unidad 1")
    st.markdown(
        "Evaluaciones con **retroalimentación formativa**: cada pregunta admite "
        "dos intentos. Tras el primer error recibirás una pista; tras el segundo, "
        "se te mostrará la respuesta correcta con su explicación."
    )

    opciones = {c["titulo"]: qid for qid, c in CUESTIONARIOS.items()}
    titulo_sel = st.selectbox(
        "Elige un cuestionario:",
        options=list(opciones.keys()),
        key="quiz_selector",
    )
    qid = opciones[titulo_sel]
    quiz = CUESTIONARIOS[qid]
    estado = _estado(qid)

    st.divider()
    _cabecera(quiz)

    if estado["finished"]:
        _render_resultado(qid, quiz, estado)
    else:
        _render_pregunta(qid, quiz, estado)
