"""Página de inicio / landing principal de CircuitProIA."""
import streamlit as st

from components.ui import (
    hero, section_header, feature_card, metric_card, chips, divider
)
from data.mock_data import BUSINESS_METRICS

# --- Hero ---------------------------------------------------------------
hero(
    pill="EdTech + IA · Ingeniería eléctrica e industria",
    title="CircuitProIA — aprende, capacita y automatiza con IA especializada",
    subtitle=(
        "Una plataforma que une el aprendizaje guiado de estudiantes, la capacitación "
        "aplicada de profesionales y agentes tutores personalizados para instituciones. "
        "Todo con inteligencia artificial entrenada en conocimiento técnico real."
    ),
    icon_size=120,
    icon_position="left",
)

st.write("")

# --- Métricas de cabecera ----------------------------------------------
cols = st.columns(4)
for col, (num, label) in zip(cols, BUSINESS_METRICS):
    with col:
        metric_card(num, label)

divider()

# --- Resumen de los tres módulos ---------------------------------------
section_header(
    "Una plataforma, tres módulos",
    "Un ecosistema completo de formación técnica",
    "Cada módulo atiende a una audiencia distinta, pero comparten la misma base de IA y contenido.",
)

c1, c2, c3 = st.columns(3)
with c1:
    feature_card(
        "🎓",
        "Estudiantes de ingeniería",
        "Laboratorio digital con guías por unidad, ejercicios interactivos, gráficos "
        "explicativos, retroalimentación inmediata e indicadores de avance.",
    )
with c2:
    feature_card(
        "🏭",
        "Capacitación industrial",
        "Rutas de formación por competencias, casos reales, simulaciones y checklists "
        "de cumplimiento para profesionales de planta y mantenimiento.",
    )
with c3:
    feature_card(
        "🤖",
        "Agentes tutores B2B",
        "Asistentes personalizados con RAG sobre los manuales y normas de cada "
        "institución, desplegables de forma privada para proteger sus datos.",
    )

st.write("")
st.info(
    "Usa el menú de la izquierda para recorrer cada módulo. "
    "Este es un prototipo navegable diseñado para el pitch.",
    icon="🧭",
)

divider()

# --- Propuesta de valor en bloques -------------------------------------
section_header(
    "Por qué CircuitProIA",
    "Conocimiento técnico real, no respuestas genéricas",
)

v1, v2, v3 = st.columns(3)
with v1:
    feature_card(
        "🎯",
        "Especialización",
        "Foco en ingeniería eléctrica e industrial. El contenido y los agentes hablan "
        "el lenguaje técnico del sector.",
    )
with v2:
    feature_card(
        "🔒",
        "Privacidad",
        "Los agentes B2B pueden operar on-premise o en nube privada, garantizando que "
        "los datos sensibles nunca salgan del cliente.",
    )
with v3:
    feature_card(
        "🚀",
        "Escalabilidad",
        "Nuevos dominios, cursos y clientes se incorporan por configuración, sin "
        "reconstruir la plataforma.",
    )

st.write("")
st.markdown("##### Tecnologías y enfoques")
chips(
    ["Python", "Streamlit", "RAG", "LLM especializados", "Despliegue privado",
     "Analítica de aprendizaje", "Gamificación"],
    variant="cyan",
)
