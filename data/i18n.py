"""
Sistema de traducción (i18n) para CircuitProAI.
Centraliza todos los textos en español e inglés.
"""

TRANSLATIONS = {
    "es": {
        # ─────────────────────────────────────────────────────────
        # APP GENERAL
        # ─────────────────────────────────────────────────────────
        "page_title": "CircuitPro · IA para educación e industria",
        "sidebar.platform": "Plataforma",
        "sidebar.modules": "Módulos",
        "sidebar.specialized": "Asistencia Especializada",
        "sidebar.prototype": "Prototipo de demostración · v0.1",
        "sidebar.copyright": "© 2026 CircuitProAI",
        "sidebar.tagline": "IA aplicada a educación e industria",

        # ─────────────────────────────────────────────────────────
        # NAVEGACIÓN
        # ─────────────────────────────────────────────────────────
        "nav.inicio": "Inicio",
        "nav.estudiantes": "Estudiantes",
        "nav.industria": "Capacitación industrial",
        "nav.agentes": "Agentes B2B",
        "nav.negocio": "Impacto y negocio",

        # ─────────────────────────────────────────────────────────
        # PÁGINA INICIO
        # ─────────────────────────────────────────────────────────
        "inicio.pill": "EdTech + IA · Ingeniería eléctrica e industria",
        "inicio.hero_title": "CircuitProAI — aprende, capacita y automatiza con IA especializada",
        "inicio.hero_subtitle": (
            "Una plataforma que une el aprendizaje guiado de estudiantes, la capacitación "
            "aplicada de profesionales y agentes tutores personalizados para instituciones. "
            "Todo con inteligencia artificial entrenada en conocimiento técnico real."
        ),
        "inicio.modules_eyebrow": "Una plataforma, tres módulos",
        "inicio.modules_title": "Un ecosistema completo de formación técnica",
        "inicio.modules_subtitle": (
            "Cada módulo atiende a una audiencia distinta, pero comparten la misma base de IA y contenido."
        ),
        "inicio.students_title": "Estudiantes de ingeniería",
        "inicio.students_text": (
            "Laboratorio digital con guías por unidad, ejercicios interactivos, gráficos "
            "explicativos, retroalimentación inmediata e indicadores de avance."
        ),
        "inicio.industry_title": "Capacitación industrial",
        "inicio.industry_text": (
            "Rutas de formación por competencias, casos reales, simulaciones y checklists "
            "de cumplimiento para profesionales de planta y mantenimiento."
        ),
        "inicio.agents_title": "Agentes tutores B2B",
        "inicio.agents_text": (
            "Asistentes personalizados con RAG sobre los manuales y normas de cada "
            "institución, desplegables de forma privada para proteger sus datos."
        ),
        "inicio.info": (
            "Usa el menú de la izquierda para recorrer cada módulo. "
            "Este es un prototipo navegable diseñado para el pitch."
        ),
        "inicio.why_title": "Por qué CircuitProAI",
        "inicio.why_subtitle": "Conocimiento técnico real, no respuestas genéricas",
        "inicio.value_specialization": "Especialización",
        "inicio.value_specialization_text": (
            "Foco en ingeniería eléctrica e industrial. El contenido y los agentes hablan "
            "el lenguaje técnico del sector."
        ),
        "inicio.value_privacy": "Privacidad",
        "inicio.value_privacy_text": (
            "Los agentes B2B pueden operar on-premise o en nube privada, garantizando que "
            "los datos sensibles nunca salgan del cliente."
        ),
        "inicio.value_scalability": "Escalabilidad",
        "inicio.value_scalability_text": (
            "Nuevos dominios, cursos y clientes se incorporan por configuración, sin "
            "reconstruir la plataforma."
        ),
        "inicio.tech_section": "Tecnologías y enfoques",
        # Métricas de las 4 columnas del hero
        "inicio.metric_label_0": "Líneas de negocio integradas",
        "inicio.metric_label_1": "Modelo dual de ingresos",
        "inicio.metric_label_2": "Reducción de tiempo de soporte estimada",
        "inicio.metric_label_3": "Disponibilidad de tutoría",

        # ─────────────────────────────────────────────────────────
        # PÁGINA ESTUDIANTES
        # ─────────────────────────────────────────────────────────
        "estudiantes.tab_teoria": "Teoría",
        "estudiantes.tab_ejercicios": "Ejercicios",
        "estudiantes.tab_glosario": "Glosario",
        "estudiantes.tab_graficos": "Gráficos interactivos",
        "estudiantes.unit_select": "Selecciona una unidad:",
        "estudiantes.intro": "Contenido educativo de ingeniería eléctrica",
        "estudiantes.section_title": "Módulo · Estudiantes",
        "estudiantes.section_subtitle": "🎓 Laboratorio digital de circuitos y máquinas eléctricas",
        "estudiantes.section_description": (
            "Aprendizaje guiado por unidades, con ejercicios interactivos, gráficos explicativos "
            "y retroalimentación inmediata."
        ),
        "estudiantes.metric_progress": "Progreso global del curso",
        "estudiantes.metric_units": "Unidades completadas",
        "estudiantes.metric_last_answer": "Última respuesta correcta",
        "estudiantes.metric_streak": "Días de racha de estudio",
        "estudiantes.tab_guides": "📚 Guías de aprendizaje",
        "estudiantes.tab_glossary": "📖 Glosario",
        "estudiantes.tab_exercise": "🧪 Ejercicio interactivo",
        "estudiantes.tab_graphics": "📈 Visualización",
        "estudiantes.unit_locked": "Completa la unidad anterior para desbloquear este contenido.",
        "estudiantes.unit_completed": "Unidad completada. ¡Buen trabajo!",
        "estudiantes.unit_building": "🚧 Contenido en construcción. Esta unidad estará disponible próximamente.",
        "estudiantes.sim_ohm": "⚡ Simulador Ley de Ohm",
        "estudiantes.sim_flow": "🔌 Flujo de Carga — 2 Buses",
        "estudiantes.sim_power_factor": "⚙️ Mejora del Factor de Potencia",
        "estudiantes.sim_harmonics": "🎛️ Análisis Armónico Industrial",

        # ─────────────────────────────────────────────────────────
        # PÁGINA INDUSTRIA
        # ─────────────────────────────────────────────────────────
        "industria.tab_rutas": "Rutas de competencia",
        "industria.tab_caso": "Caso de estudio",
        "industria.tab_checklist": "Checklist de cumplimiento",
        "industria.intro": "Formación aplicada para profesionales industriales",

        # ─────────────────────────────────────────────────────────
        # PÁGINA AGENTES
        # ─────────────────────────────────────────────────────────
        "agentes.tab_pipeline": "Pipeline RAG",
        "agentes.tab_beneficios": "Beneficios",
        "agentes.tab_demo": "Demo: Chat de asistente",
        "agentes.intro": "Tutores personalizados con IA para empresas",

        # ─────────────────────────────────────────────────────────
        # PÁGINA NEGOCIO
        # ─────────────────────────────────────────────────────────
        "negocio.tab_financiero": "Proyecciones financieras",
        "negocio.tab_mercado": "Análisis de mercado",
        "negocio.tab_diferenciadores": "Diferenciadores",
        "negocio.intro": "Impacto empresarial y estrategia de crecimiento",

        # ─────────────────────────────────────────────────────────
        # CONTROLES COMUNES
        # ─────────────────────────────────────────────────────────
        "btn.submit": "Enviar",
        "btn.verify": "Verificar",
        "btn.next": "Siguiente",
        "btn.prev": "Anterior",
        "btn.reset": "Reiniciar",
        "btn.check": "Marcar",
        "btn.uncheck": "Desmarcar",
        "label.language": "Idioma",
        "label.spanish": "Español",
        "label.english": "English",

        # ─────────────────────────────────────────────────────────
        # FEEDBACK Y MENSAJES
        # ─────────────────────────────────────────────────────────
        "msg.correct": "¡Correcto!",
        "msg.incorrect": "Incorrecto. Intenta de nuevo.",
        "msg.hint": "Pista:",
        "msg.explanation": "Explicación:",
        "msg.loading": "Cargando...",
        "msg.no_selection": "Por favor, selecciona una opción.",

        # ─────────────────────────────────────────────────────────
        # MÉTRICAS Y PROGRESO
        # ─────────────────────────────────────────────────────────
        "metric.students": "Estudiantes activos",
        "metric.companies": "Empresas asociadas",
        "metric.hours": "Horas de contenido",
        "metric.agents": "Agentes desplegados",
        "metric.progress": "Progreso",
        "metric.completed": "Completado",

        # ─────────────────────────────────────────────────────────
        # FLUJO DE CARGA (Power Flow)
        # ─────────────────────────────────────────────────────────
        "fc.title": "⚡ Flujo de Carga — Red de 2 Buses",
        "fc.method": "Método de Gauss Seidel",
        "fc.equation": "V₁ = V₂ + Z·I",
        "fc.system": "Sistema en valores por unidad [pu]",
        "fc.author": "Desarrollado por **Dr. Maykop Pérez Martínez** — Universidad de Concepción (UdeC) — Depto. Ingeniería Eléctrica",
        "fc.network_params": "🎛️ Parámetros de la Red",
        "fc.transmission_line": "**Línea de transmisión:** Z = R + jX [pu]  |  ΔV = Z·I",
        "fc.resistance": "R — Resistencia [pu]",
        "fc.reactance": "X — Reactancia [pu]",
        "fc.load_bus": "**Carga en Bus 1:** Scarga = PL + jQL [pu]  \nCompensación: Qc (banco capacitivo)",
        "fc.active_power": "Pₗ — Potencia activa [pu]",
        "fc.reactive_power": "Qₗ — Potencia reactiva [pu]",
        "fc.capacitor_bank": "Qc — Banco capacitivo [pu]",
        "fc.slack_bus": "**Bus 2 (barra slack):** V₂ = |V₂| ∠ δ₂ [pu]  \nReferencia angular del sistema",
        "fc.voltage_magnitude": "|V₂| — Módulo [pu]",
        "fc.voltage_angle": "δ₂ — Ángulo [°]",
        "fc.presets": "**Casos predefinidos:**",
        "fc.preset_resistive": "Resistivo",
        "fc.preset_inductive": "Inductivo",
        "fc.preset_reference": "Referencia",
        "fc.preset_high_load": "Alta carga",
        "fc.preset_capacitive": "Capacitivo",
        "fc.results": "📊 Resultados del Flujo",
        "fc.solution_method": "**Iteración — Método de Gauss-Seidel:**",
        "fc.initial_guess": "Valor inicial (flat start) V₁ = 1.0 pu, δ₁ = 0°",
        "fc.iteration": "Iteración",
        "fc.voltage_bus1": "V₁ [pu]",
        "fc.angle_bus1": "δ₁ [°]",
        "fc.convergence": "Convergencia (tol = 1e-4)",
        "fc.power_flow_summary": "**Resumen del Flujo de Potencia:**",
        "fc.power_injected": "Potencia inyectada en Bus 1 (desde la línea)",
        "fc.power_loss": "**Pérdidas de potencia en la línea:**",
        "fc.reactive_loss": "Pérdida reactiva en la línea",
        "fc.apparent_power": "Potencia aparente (corriente eficaz)",
        "fc.efficiency": "**Eficiencia de la transmisión:**",
    },
    "en": {
        # ─────────────────────────────────────────────────────────
        # APP GENERAL
        # ─────────────────────────────────────────────────────────
        "page_title": "CircuitPro · AI for Education & Industry",
        "sidebar.platform": "Platform",
        "sidebar.modules": "Modules",
        "sidebar.specialized": "Specialized Assistance",
        "sidebar.prototype": "Demo prototype · v0.1",
        "sidebar.copyright": "© 2026 CircuitProAI",
        "sidebar.tagline": "AI for Education & Industry",

        # ─────────────────────────────────────────────────────────
        # NAVEGACIÓN
        # ─────────────────────────────────────────────────────────
        "nav.inicio": "Home",
        "nav.estudiantes": "Students",
        "nav.industria": "Industrial Training",
        "nav.agentes": "B2B Agents",
        "nav.negocio": "Impact & Business",

        # ─────────────────────────────────────────────────────────
        # PÁGINA INICIO
        # ─────────────────────────────────────────────────────────
        "inicio.pill": "EdTech + AI · Electrical Engineering & Industry",
        "inicio.hero_title": "CircuitProAI — Learn, Train & Automate with Specialized AI",
        "inicio.hero_subtitle": (
            "A platform that combines guided student learning, professional training, "
            "and personalized tutoring agents for institutions. All powered by artificial "
            "intelligence trained on real technical knowledge."
        ),
        "inicio.modules_eyebrow": "One platform, three modules",
        "inicio.modules_title": "A complete technical training ecosystem",
        "inicio.modules_subtitle": (
            "Each module serves a different audience, but they all share the same AI foundation and content."
        ),
        "inicio.students_title": "Engineering Students",
        "inicio.students_text": (
            "Digital lab with unit guides, interactive exercises, explanatory graphics, "
            "immediate feedback, and progress indicators."
        ),
        "inicio.industry_title": "Industrial Training",
        "inicio.industry_text": (
            "Competency-based training routes, real-world cases, simulations, and compliance "
            "checklists for plant and maintenance professionals."
        ),
        "inicio.agents_title": "B2B Tutoring Agents",
        "inicio.agents_text": (
            "Personalized assistants with RAG over each institution's manuals and standards, "
            "deployed privately to protect their data."
        ),
        "inicio.info": (
            "Use the left menu to explore each module. "
            "This is a navigable prototype designed for the pitch."
        ),
        "inicio.why_title": "Why CircuitProAI",
        "inicio.why_subtitle": "Real technical knowledge, not generic answers",
        "inicio.value_specialization": "Specialization",
        "inicio.value_specialization_text": (
            "Focus on electrical and industrial engineering. Content and agents speak "
            "the technical language of the sector."
        ),
        "inicio.value_privacy": "Privacy",
        "inicio.value_privacy_text": (
            "B2B agents can operate on-premise or in private cloud, ensuring that "
            "sensitive data never leaves the client."
        ),
        "inicio.value_scalability": "Scalability",
        "inicio.value_scalability_text": (
            "New domains, courses, and clients are added by configuration, without "
            "rebuilding the platform."
        ),
        "inicio.tech_section": "Technologies & Approaches",
        # Métricas de las 4 columnas del hero
        "inicio.metric_label_0": "Integrated business lines",
        "inicio.metric_label_1": "Dual revenue model",
        "inicio.metric_label_2": "Estimated support time reduction",
        "inicio.metric_label_3": "Tutoring availability",

        # ─────────────────────────────────────────────────────────
        # PÁGINA ESTUDIANTES
        # ─────────────────────────────────────────────────────────
        "estudiantes.tab_teoria": "Theory",
        "estudiantes.tab_ejercicios": "Exercises",
        "estudiantes.tab_glosario": "Glossary",
        "estudiantes.tab_graficos": "Interactive Graphics",
        "estudiantes.unit_select": "Select a unit:",
        "estudiantes.intro": "Electrical engineering educational content",
        "estudiantes.section_title": "Module · Students",
        "estudiantes.section_subtitle": "🎓 Digital lab for circuits and electrical machines",
        "estudiantes.section_description": (
            "Unit-guided learning with interactive exercises, explanatory graphics, "
            "and immediate feedback."
        ),
        "estudiantes.metric_progress": "Overall course progress",
        "estudiantes.metric_units": "Completed units",
        "estudiantes.metric_last_answer": "Last correct answer",
        "estudiantes.metric_streak": "Study streak days",
        "estudiantes.tab_guides": "📚 Learning Guides",
        "estudiantes.tab_glossary": "📖 Glossary",
        "estudiantes.tab_exercise": "🧪 Interactive Exercise",
        "estudiantes.tab_graphics": "📈 Visualization",
        "estudiantes.unit_locked": "Complete the previous unit to unlock this content.",
        "estudiantes.unit_completed": "Unit completed. Great job!",
        "estudiantes.unit_building": "🚧 Content under construction. This unit will be available soon.",
        "estudiantes.sim_ohm": "⚡ Ohm's Law Simulator",
        "estudiantes.sim_flow": "🔌 Power Flow — 2 Buses",
        "estudiantes.sim_power_factor": "⚙️ Power Factor Improvement",
        "estudiantes.sim_harmonics": "🎛️ Industrial Harmonic Analysis",

        # ─────────────────────────────────────────────────────────
        # PÁGINA INDUSTRIA
        # ─────────────────────────────────────────────────────────
        "industria.tab_rutas": "Competency Routes",
        "industria.tab_caso": "Case Study",
        "industria.tab_checklist": "Compliance Checklist",
        "industria.intro": "Applied training for industrial professionals",

        # ─────────────────────────────────────────────────────────
        # PÁGINA AGENTES
        # ─────────────────────────────────────────────────────────
        "agentes.tab_pipeline": "RAG Pipeline",
        "agentes.tab_beneficios": "Benefits",
        "agentes.tab_demo": "Demo: Assistant Chat",
        "agentes.intro": "Personalized AI tutors for enterprises",

        # ─────────────────────────────────────────────────────────
        # PÁGINA NEGOCIO
        # ─────────────────────────────────────────────────────────
        "negocio.tab_financiero": "Financial Projections",
        "negocio.tab_mercado": "Market Analysis",
        "negocio.tab_diferenciadores": "Differentiators",
        "negocio.intro": "Business impact and growth strategy",

        # ─────────────────────────────────────────────────────────
        # CONTROLES COMUNES
        # ─────────────────────────────────────────────────────────
        "btn.submit": "Submit",
        "btn.verify": "Verify",
        "btn.next": "Next",
        "btn.prev": "Previous",
        "btn.reset": "Reset",
        "btn.check": "Check",
        "btn.uncheck": "Uncheck",
        "label.language": "Language",
        "label.spanish": "Español",
        "label.english": "English",

        # ─────────────────────────────────────────────────────────
        # FEEDBACK Y MENSAJES
        # ─────────────────────────────────────────────────────────
        "msg.correct": "Correct!",
        "msg.incorrect": "Incorrect. Try again.",
        "msg.hint": "Hint:",
        "msg.explanation": "Explanation:",
        "msg.loading": "Loading...",
        "msg.no_selection": "Please select an option.",

        # ─────────────────────────────────────────────────────────
        # MÉTRICAS Y PROGRESO
        # ─────────────────────────────────────────────────────────
        "metric.students": "Active Students",
        "metric.companies": "Associated Companies",
        "metric.hours": "Content Hours",
        "metric.agents": "Deployed Agents",
        "metric.progress": "Progress",
        "metric.completed": "Completed",

        # ─────────────────────────────────────────────────────────
        # FLUJO DE CARGA (Power Flow)
        # ─────────────────────────────────────────────────────────
        "fc.title": "⚡ Power Flow — 2-Bus Network",
        "fc.method": "Gauss-Seidel Method",
        "fc.equation": "V₁ = V₂ + Z·I",
        "fc.system": "System in per-unit values [pu]",
        "fc.author": "Developed by **Dr. Maykop Pérez Martínez** — Universidad de Concepción (UdeC) — Dept. Electrical Engineering",
        "fc.network_params": "🎛️ Network Parameters",
        "fc.transmission_line": "**Transmission Line:** Z = R + jX [pu]  |  ΔV = Z·I",
        "fc.resistance": "R — Resistance [pu]",
        "fc.reactance": "X — Reactance [pu]",
        "fc.load_bus": "**Load at Bus 1:** Sload = PL + jQL [pu]  \nCompensation: Qc (capacitor bank)",
        "fc.active_power": "Pₗ — Active Power [pu]",
        "fc.reactive_power": "Qₗ — Reactive Power [pu]",
        "fc.capacitor_bank": "Qc — Capacitor Bank [pu]",
        "fc.slack_bus": "**Bus 2 (slack bus):** V₂ = |V₂| ∠ δ₂ [pu]  \nAngular reference of the system",
        "fc.voltage_magnitude": "|V₂| — Magnitude [pu]",
        "fc.voltage_angle": "δ₂ — Angle [°]",
        "fc.presets": "**Predefined cases:**",
        "fc.preset_resistive": "Resistive",
        "fc.preset_inductive": "Inductive",
        "fc.preset_reference": "Reference",
        "fc.preset_high_load": "High load",
        "fc.preset_capacitive": "Capacitive",
        "fc.results": "📊 Power Flow Results",
        "fc.solution_method": "**Iteration — Gauss-Seidel Method:**",
        "fc.initial_guess": "Initial value (flat start) V₁ = 1.0 pu, δ₁ = 0°",
        "fc.iteration": "Iteration",
        "fc.voltage_bus1": "V₁ [pu]",
        "fc.angle_bus1": "δ₁ [°]",
        "fc.convergence": "Convergence (tol = 1e-4)",
        "fc.power_flow_summary": "**Power Flow Summary:**",
        "fc.power_injected": "Power injected at Bus 1 (from the line)",
        "fc.power_loss": "**Power losses in the line:**",
        "fc.reactive_loss": "Reactive power loss in the line",
        "fc.apparent_power": "Apparent power (effective current)",
        "fc.efficiency": "**Transmission efficiency:**",
    },
}


def t(key: str, lang: str = "es") -> str:
    """
    Obtiene la traducción de una clave.

    Args:
        key: Clave de traducción (ej: "nav.inicio")
        lang: Código de idioma ("es" o "en"). Por defecto "es".

    Returns:
        Texto traducido, o la clave si no existe.
    """
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_language() -> str:
    """
    Obtiene el idioma actual desde session_state.
    Por defecto "es" si no está configurado.
    """
    import streamlit as st
    return st.session_state.get("language", "es")


def set_language(lang: str):
    """Establece el idioma actual en session_state."""
    import streamlit as st
    st.session_state["language"] = lang
