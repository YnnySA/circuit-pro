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
        "industria.section_eyebrow": "Módulo · Industria",
        "industria.section_title": "🏭 Capacitación aplicada por competencias",
        "industria.section_desc": (
            "Formación aterrizada a escenarios reales de planta: rutas por competencias, casos "
            "prácticos, simulaciones y checklists de cumplimiento."
        ),
        "industria.metric_routes": "Rutas de capacitación activas",
        "industria.metric_progress": "Avance promedio del equipo",
        "industria.metric_hours": "Horas de contenido",
        "industria.metric_compliance": "Cumplimiento de seguridad",
        "industria.tab_rutas": "🧭 Rutas por competencias",
        "industria.tab_caso": "🛠️ Caso práctico",
        "industria.tab_checklist": "✅ Checklist de cumplimiento",
        "industria.routes_header": "Programas de formación por competencias",
        "industria.level_label": "Nivel:",
        "industria.duration_label": "Duración:",
        "industria.progress_label": "Avance:",
        "industria.case_radio": "Selecciona la acción correcta:",
        "industria.case_btn": "Evaluar decisión",
        "industria.case_no_selection": "Selecciona una opción antes de evaluar.",
        "industria.case_correct": "Decisión correcta. ",
        "industria.case_wrong": "Decisión riesgosa. ",
        "industria.checklist_header": "Checklist de inspección y cumplimiento",
        "industria.checklist_caption": "Marca cada ítem completado. El progreso se actualiza en tiempo real.",
        "industria.checklist_progress": "Cumplimiento:",
        "industria.checklist_ok": "Checklist completo. Equipo apto para operación.",
        "industria.checklist_mid": "Avance aceptable. Completa los ítems restantes.",
        "industria.checklist_low": "Cumplimiento insuficiente para autorizar la operación.",
        "industria.tab_rutas_old": "Rutas de competencia",
        "industria.intro": "Formación aplicada para profesionales industriales",

        # ─────────────────────────────────────────────────────────
        # PÁGINA AGENTES
        # ─────────────────────────────────────────────────────────
        "agentes.section_eyebrow": "Módulo · B2B",
        "agentes.section_title": "🤖 Agentes tutores personalizados",
        "agentes.section_desc": (
            "Desarrollamos asistentes de IA especializados en el conocimiento de cada institución, "
            "con técnicas RAG y despliegue privado para proteger sus datos."
        ),
        "agentes.metric_rag": "Recuperación aumentada",
        "agentes.metric_onprem": "Despliegue privado",
        "agentes.metric_support": "Menos carga de soporte",
        "agentes.metric_availability": "Disponibilidad",
        "agentes.tab_pipeline": "🔄 Flujo de servicio",
        "agentes.tab_beneficios": "⭐ Beneficios",
        "agentes.tab_demo": "💬 Demo del agente",
        "agentes.tab_casos": "🏢 Casos de uso",
        "agentes.pipeline_header": "Del conocimiento del cliente a un agente operativo",
        "agentes.pipeline_caption": "Proceso de implementación en 5 etapas.",
        "agentes.pipeline_info": (
            "El flujo es repetible y configurable: incorporar un nuevo cliente no requiere "
            "reconstruir la plataforma, solo cargar su base de conocimiento."
        ),
        "agentes.benefits_header": "Propuesta de valor para instituciones y empresas",
        "agentes.demo_header": "Demostración: agente especializado con RAG",
        "agentes.demo_caption": (
            "Simulación: el agente responde usando los manuales internos del cliente. "
            "Las respuestas son demostrativas para el pitch."
        ),
        "agentes.demo_select": "Base de conocimiento del agente:",
        "agentes.demo_input": "Escribe una pregunta para el agente:",
        "agentes.demo_placeholder": "Ej: ¿Cuál es el procedimiento antes de intervenir un tablero energizado?",
        "agentes.demo_btn": "Consultar al agente",
        "agentes.demo_source": "Fuente consultada:",
        "agentes.demo_response": (
            "Según los procedimientos cargados, antes de intervenir un tablero se debe "
            "aplicar **bloqueo y etiquetado (LOTO)**, verificar la **ausencia de tensión** "
            "con instrumento certificado y usar el **EPP** correspondiente. "
            "\n\n_Esta respuesta se genera recuperando los fragmentos relevantes del "
            "documento mediante RAG, citando la fuente interna._"
        ),
        "agentes.demo_ref": "📎 Referencia: Sección 4.2 — Procedimientos de intervención segura",
        "agentes.demo_greeting": (
            "👋 Hola, soy el agente especializado de tu institución. "
            "Pregúntame sobre los manuales y procedimientos cargados."
        ),
        "agentes.cases_header": "Agentes desplegados (ejemplos)",
        "agentes.cases_col_client": "Cliente",
        "agentes.cases_col_agent": "Agente",
        "agentes.cases_col_base": "Base de conocimiento",
        "agentes.tab_pipeline_old": "Pipeline RAG",
        "agentes.tab_beneficios_old": "Beneficios",
        "agentes.tab_demo_old": "Demo: Chat de asistente",
        "agentes.intro": "Tutores personalizados con IA para empresas",

        # ─────────────────────────────────────────────────────────
        # PÁGINA NEGOCIO
        # ─────────────────────────────────────────────────────────
        "negocio.section_eyebrow": "Impacto y negocio",
        "negocio.section_title": "📈 Una visión clara de crecimiento",
        "negocio.section_desc": (
            "Modelo de negocio dual (B2C + B2B), mercado objetivo definido y escalabilidad basada "
            "en agentes inteligentes."
        ),
        "negocio.revenue_header": "Proyección de ingresos (MM CLP)",
        "negocio.revenue_caption": "Escenario base a 4 años, combinando suscripciones B2C y contratos B2B.",
        "negocio.revenue_b2c": "B2C · Estudiantes",
        "negocio.revenue_b2b": "B2B · Instituciones",
        "negocio.revenue_total": "Ingreso proyectado Año 4:",
        "negocio.revenue_suffix": "MM CLP combinando ambas líneas.",
        "negocio.market_header": "Mercado objetivo",
        "negocio.market_caption": "Distribución del mercado direccionable por segmento.",
        "negocio.market_col_segment": "Segmento",
        "negocio.market_col_weight": "Peso (%)",
        "negocio.diff_eyebrow": "Ventaja competitiva",
        "negocio.diff_title": "Qué nos hace diferentes",
        "negocio.model_eyebrow": "Modelo y escalabilidad",
        "negocio.model_title": "Cómo crece CircuitProIA",
        "negocio.model_b2c_title": "B2C — Suscripción",
        "negocio.model_b2c_text": (
            "Estudiantes y profesionales acceden por suscripción mensual a guías, ejercicios "
            "y tutoría con IA."
        ),
        "negocio.model_b2b_title": "B2B — Licencias y servicios",
        "negocio.model_b2b_text": (
            "Universidades y empresas contratan agentes personalizados, despliegue privado "
            "y capacitación a medida."
        ),
        "negocio.model_expand_title": "Expansión",
        "negocio.model_expand_text": (
            "El mismo motor se replica a nuevos dominios técnicos y países de LATAM por "
            "configuración, no por reconstrucción."
        ),
        "negocio.cta": (
            "CircuitProIA combina valor educativo inmediato con un motor B2B escalable: un producto en "
            "etapa temprana con una ruta clara hacia el crecimiento."
        ),
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
        "fc.circuit_diagram": "🔌 Diagrama del Circuito",
        "fc.phasor_diagram": "📐 Diagrama Fasorial",
        "fc.phasor_title": "Diagrama Fasorial — Tensiones y Corriente",
        "fc.fundamental_relations": "📐 Relaciones Fundamentales",
        "fc.converged": "✅ Convergió",
        "fc.not_converged": "❌ No convergió",
        "fc.iterations": "iteraciones",
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
        "fc.table_col_variable": "Variable",
        "fc.table_col_expression": "Expresión",
        "fc.table_col_polar": "Polar / Valor",
        "fc.table_col_rect": "Rectangular",
        "fc.table_v1": "Tensión Bus 1",
        "fc.table_current": "Corriente de línea",
        "fc.table_p21": "Pot. Activa P₂₁",
        "fc.table_q21": "Pot. Reactiva Q₂₁",
        "fc.table_s21": "Pot. Aparente S₂₁",
        "fc.table_dv": "Caída de tensión ΔV",
        "fc.table_ploss": "Pérdidas activas",
        "fc.table_qloss": "Pérdidas reactivas",
        "fc.rel_sending": "TENSIÓN DE ENVÍO",
        "fc.rel_received": "POTENCIA RECIBIDA",
        "fc.rel_current": "CORRIENTE DE LÍNEA",
        "fc.rel_losses": "PÉRDIDAS EN LA LÍNEA",
        "fc.rel_admittance": "ADMITANCIA DE LÍNEA",
        "fc.rel_balance": "BALANCE DE POTENCIA",
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
        "industria.section_eyebrow": "Module · Industry",
        "industria.section_title": "🏭 Applied competency-based training",
        "industria.section_desc": (
            "Training grounded in real plant scenarios: competency routes, case studies, "
            "simulations, and compliance checklists."
        ),
        "industria.metric_routes": "Active training routes",
        "industria.metric_progress": "Average team progress",
        "industria.metric_hours": "Content hours",
        "industria.metric_compliance": "Safety compliance",
        "industria.tab_rutas": "🧭 Competency Routes",
        "industria.tab_caso": "🛠️ Case Study",
        "industria.tab_checklist": "✅ Compliance Checklist",
        "industria.routes_header": "Competency-based training programs",
        "industria.level_label": "Level:",
        "industria.duration_label": "Duration:",
        "industria.progress_label": "Progress:",
        "industria.case_radio": "Select the correct action:",
        "industria.case_btn": "Evaluate decision",
        "industria.case_no_selection": "Please select an option before evaluating.",
        "industria.case_correct": "Correct decision. ",
        "industria.case_wrong": "Risky decision. ",
        "industria.checklist_header": "Inspection and compliance checklist",
        "industria.checklist_caption": "Check each completed item. Progress updates in real time.",
        "industria.checklist_progress": "Compliance:",
        "industria.checklist_ok": "Checklist complete. Equipment cleared for operation.",
        "industria.checklist_mid": "Acceptable progress. Complete the remaining items.",
        "industria.checklist_low": "Insufficient compliance to authorize operation.",
        "industria.tab_rutas_old": "Competency Routes",
        "industria.intro": "Applied training for industrial professionals",

        # ─────────────────────────────────────────────────────────
        # PÁGINA AGENTES
        # ─────────────────────────────────────────────────────────
        "agentes.section_eyebrow": "Module · B2B",
        "agentes.section_title": "🤖 Personalized tutoring agents",
        "agentes.section_desc": (
            "We build AI assistants specialized in each institution's knowledge, "
            "using RAG techniques and private deployment to protect their data."
        ),
        "agentes.metric_rag": "Augmented retrieval",
        "agentes.metric_onprem": "Private deployment",
        "agentes.metric_support": "Less support load",
        "agentes.metric_availability": "Availability",
        "agentes.tab_pipeline": "🔄 Service flow",
        "agentes.tab_beneficios": "⭐ Benefits",
        "agentes.tab_demo": "💬 Agent demo",
        "agentes.tab_casos": "🏢 Use cases",
        "agentes.pipeline_header": "From client knowledge to an operational agent",
        "agentes.pipeline_caption": "Implementation process in 5 stages.",
        "agentes.pipeline_info": (
            "The flow is repeatable and configurable: onboarding a new client does not require "
            "rebuilding the platform — just load their knowledge base."
        ),
        "agentes.benefits_header": "Value proposition for institutions and enterprises",
        "agentes.demo_header": "Demo: specialized agent with RAG",
        "agentes.demo_caption": (
            "Simulation: the agent responds using the client's internal manuals. "
            "Responses are demonstrative for the pitch."
        ),
        "agentes.demo_select": "Agent knowledge base:",
        "agentes.demo_input": "Ask the agent a question:",
        "agentes.demo_placeholder": "E.g.: What is the procedure before intervening an energized panel?",
        "agentes.demo_btn": "Query the agent",
        "agentes.demo_source": "Source consulted:",
        "agentes.demo_response": (
            "According to the loaded procedures, before intervening a panel you must apply "
            "**lockout/tagout (LOTO)**, verify **absence of voltage** with a certified instrument, "
            "and use the corresponding **PPE**. "
            "\n\n_This response is generated by retrieving relevant fragments from the "
            "document via RAG, citing the internal source._"
        ),
        "agentes.demo_ref": "📎 Reference: Section 4.2 — Safe intervention procedures",
        "agentes.demo_greeting": (
            "👋 Hi, I am your institution's specialized agent. "
            "Ask me about the loaded manuals and procedures."
        ),
        "agentes.cases_header": "Deployed agents (examples)",
        "agentes.cases_col_client": "Client",
        "agentes.cases_col_agent": "Agent",
        "agentes.cases_col_base": "Knowledge base",
        "agentes.tab_pipeline_old": "RAG Pipeline",
        "agentes.tab_beneficios_old": "Benefits",
        "agentes.tab_demo_old": "Demo: Assistant Chat",
        "agentes.intro": "Personalized AI tutors for enterprises",

        # ─────────────────────────────────────────────────────────
        # PÁGINA NEGOCIO
        # ─────────────────────────────────────────────────────────
        "negocio.section_eyebrow": "Impact & Business",
        "negocio.section_title": "📈 A clear vision of growth",
        "negocio.section_desc": (
            "Dual business model (B2C + B2B), defined target market, and scalability based "
            "on intelligent agents."
        ),
        "negocio.revenue_header": "Revenue projection (MM CLP)",
        "negocio.revenue_caption": "Base scenario over 4 years, combining B2C subscriptions and B2B contracts.",
        "negocio.revenue_b2c": "B2C · Students",
        "negocio.revenue_b2b": "B2B · Institutions",
        "negocio.revenue_total": "Projected revenue Year 4:",
        "negocio.revenue_suffix": "MM CLP combining both lines.",
        "negocio.market_header": "Target market",
        "negocio.market_caption": "Distribution of addressable market by segment.",
        "negocio.market_col_segment": "Segment",
        "negocio.market_col_weight": "Weight (%)",
        "negocio.diff_eyebrow": "Competitive advantage",
        "negocio.diff_title": "What makes us different",
        "negocio.model_eyebrow": "Model & scalability",
        "negocio.model_title": "How CircuitProIA grows",
        "negocio.model_b2c_title": "B2C — Subscription",
        "negocio.model_b2c_text": (
            "Students and professionals access monthly subscriptions to guides, exercises, "
            "and AI tutoring."
        ),
        "negocio.model_b2b_title": "B2B — Licenses & services",
        "negocio.model_b2b_text": (
            "Universities and companies hire personalized agents, private deployment, "
            "and tailored training."
        ),
        "negocio.model_expand_title": "Expansion",
        "negocio.model_expand_text": (
            "The same engine replicates to new technical domains and LATAM countries by "
            "configuration, not reconstruction."
        ),
        "negocio.cta": (
            "CircuitProIA combines immediate educational value with a scalable B2B engine: an early-stage "
            "product with a clear path to growth."
        ),
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
        "fc.circuit_diagram": "🔌 Circuit Diagram",
        "fc.phasor_diagram": "📐 Phasor Diagram",
        "fc.phasor_title": "Phasor Diagram — Voltages and Current",
        "fc.fundamental_relations": "📐 Fundamental Relations",
        "fc.converged": "✅ Converged",
        "fc.not_converged": "❌ Did not converge",
        "fc.iterations": "iterations",
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
        "fc.table_col_variable": "Variable",
        "fc.table_col_expression": "Expression",
        "fc.table_col_polar": "Polar / Value",
        "fc.table_col_rect": "Rectangular",
        "fc.table_v1": "Bus 1 Voltage",
        "fc.table_current": "Line Current",
        "fc.table_p21": "Active Power P₂₁",
        "fc.table_q21": "Reactive Power Q₂₁",
        "fc.table_s21": "Apparent Power S₂₁",
        "fc.table_dv": "Voltage Drop ΔV",
        "fc.table_ploss": "Active Losses",
        "fc.table_qloss": "Reactive Losses",
        "fc.rel_sending": "SENDING VOLTAGE",
        "fc.rel_received": "RECEIVED POWER",
        "fc.rel_current": "LINE CURRENT",
        "fc.rel_losses": "LINE LOSSES",
        "fc.rel_admittance": "LINE ADMITTANCE",
        "fc.rel_balance": "POWER BALANCE",
    },
}


def t(key: str, lang: str = "es") -> str:
    return TRANSLATIONS.get(lang, {}).get(key, key)


def get_language() -> str:
    import streamlit as st
    return st.session_state.get("language", "es")


def set_language(lang: str):
    import streamlit as st
    st.session_state["language"] = lang
