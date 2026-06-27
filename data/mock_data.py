"""
Datos de ejemplo simulados para el prototipo VoltiQ.
Centralizados aquí para que las páginas queden limpias y sea fácil iterar
durante el pitch.
"""

# ---------------------------------------------------------------------------
# MÓDULO 1 — Estudiantes de ingeniería eléctrica
# ---------------------------------------------------------------------------
STUDENT_UNITS = [
    {
        "titulo": "Unidad 1 · Circuitos en Corriente Continua",
        "progreso": 100,
        "temas": ["Ley de Ohm", "Leyes de Kirchhoff", "Divisores de tensión", "Thévenin y Norton"],
        "estado": "Completada",
    },
    {
        "titulo": "Unidad 2 · Corriente Alterna y Fasores",
        "progreso": 32,
        "temas": ["Señales senoidales", "Impedancia", "Notación fasorial", "Potencia activa y reactiva"],
        "estado": "En curso",
    },
    {
        "titulo": "Unidad 3 · Sistemas Trifásicos",
        "progreso": 0,
        "temas": ["Conexión estrella/delta", "Potencia trifásica", "Factor de potencia"],
        "estado": "En curso",
    },
    {
        "titulo": "Unidad 4 · Máquinas Eléctricas",
        "progreso": 0,
        "temas": ["Transformadores", "Motores de inducción", "Generadores"],
        "estado": "Bloqueada",
    },
]

# Ejercicio interactivo de ejemplo (Ley de Ohm / divisor de tensión)
QUIZ_OHM = {
    "enunciado": (
        "En un circuito serie, una fuente de **12 V** alimenta dos resistencias: "
        "**R1 = 4 Ω** y **R2 = 8 Ω**. ¿Cuál es la corriente que circula por el circuito?"
    ),
    "opciones": ["0.5 A", "1.0 A", "1.5 A", "3.0 A"],
    "correcta": "1.0 A",
    "explicacion": (
        "La resistencia total es R = R1 + R2 = 4 + 8 = 12 Ω. "
        "Por la Ley de Ohm, I = V / R = 12 / 12 = **1.0 A**."
    ),
}

# Datos para el gráfico de la curva característica (V-I) de una resistencia
RESISTANCE_OHMS = 12

# ---------------------------------------------------------------------------
# MÓDULO 2 — Capacitación industrial
# ---------------------------------------------------------------------------
INDUSTRY_TRACKS = [
    {
        "nombre": "Seguridad Eléctrica y Bloqueo/Etiquetado (LOTO)",
        "nivel": "Operativo",
        "duracion": "6 h",
        "progreso": 80,
        "competencias": ["Identificación de riesgos", "Procedimiento LOTO", "EPP", "Respuesta a incidentes"],
    },
    {
        "nombre": "Mantenimiento Predictivo de Motores",
        "nivel": "Técnico",
        "duracion": "10 h",
        "progreso": 45,
        "competencias": ["Análisis de vibraciones", "Termografía", "Análisis de corriente", "Diagnóstico"],
    },
    {
        "nombre": "Eficiencia Energética en Planta",
        "nivel": "Profesional",
        "duracion": "8 h",
        "progreso": 20,
        "competencias": ["Auditoría energética", "Factor de potencia", "Gestión de demanda"],
    },
]

# Caso práctico de ejemplo
INDUSTRY_CASE = {
    "titulo": "Falla intermitente en arranque de motor de 75 kW",
    "contexto": (
        "Una bomba centrífuga accionada por un motor de inducción de 75 kW presenta "
        "disparos intermitentes del guardamotor durante el arranque. La planta no puede "
        "detener la línea por más de 30 minutos."
    ),
    "pregunta": "¿Cuál es la primera acción recomendada antes de intervenir el equipo?",
    "opciones": [
        "Reemplazar el motor de inmediato",
        "Aplicar procedimiento LOTO y verificar ausencia de tensión",
        "Aumentar el ajuste del guardamotor para evitar disparos",
        "Reiniciar el arranque varias veces para 'destrabar' el motor",
    ],
    "correcta": "Aplicar procedimiento LOTO y verificar ausencia de tensión",
    "explicacion": (
        "Toda intervención debe iniciar con el bloqueo y etiquetado (LOTO) y la verificación "
        "de ausencia de tensión. Aumentar el ajuste del guardamotor enmascara la falla y "
        "compromete la seguridad."
    ),
}

# Checklist de cumplimiento operativo
COMPLIANCE_CHECKLIST = [
    "Inspección visual de tablero y conexiones",
    "Verificación de torque en bornes de potencia",
    "Medición de aislamiento (megóhmetro)",
    "Registro de temperatura de operación",
    "Prueba de parada de emergencia",
    "Actualización de bitácora de mantenimiento",
]

# ---------------------------------------------------------------------------
# MÓDULO 3 — Agentes tutores personalizados (B2B)
# ---------------------------------------------------------------------------
AGENT_PIPELINE = [
    ("Ingesta de conocimiento", "Manuales, normas, cursos y procedimientos de la institución se cargan y normalizan."),
    ("Indexación vectorial (RAG)", "El contenido se fragmenta y vectoriza para recuperación semántica precisa."),
    ("Especialización del agente", "Se define personalidad, alcance y restricciones según el cliente."),
    ("Despliegue privado", "Operación en nube privada o on-premise para proteger datos sensibles."),
    ("Monitoreo y mejora", "Métricas de uso y retroalimentación continua para afinar respuestas."),
]

AGENT_BENEFITS = [
    ("🔒", "Privacidad por diseño", "Despliegue on-premise o nube privada; los datos nunca salen del perímetro del cliente."),
    ("📚", "Conocimiento propio", "El agente responde con base en los manuales y normas internas, no en información genérica."),
    ("⚙️", "Integración flexible", "Conectores a SharePoint, Moodle, LMS, intranets y bases documentales existentes."),
    ("📈", "Mejora continua", "Tablero de métricas, brechas de conocimiento detectadas y reentrenamiento periódico."),
]

AGENT_CASES = [
    {"cliente": "Universidad regional", "agente": "Tutor de Circuitos 24/7", "base": "Apuntes, guías y exámenes de la cátedra"},
    {"cliente": "Empresa de distribución eléctrica", "agente": "Asistente de procedimientos", "base": "Manuales de seguridad y normativa SEC"},
    {"cliente": "Planta industrial", "agente": "Copiloto de mantenimiento", "base": "Hojas técnicas y bitácoras de equipos"},
]

# ---------------------------------------------------------------------------
# IMPACTO Y NEGOCIO
# ---------------------------------------------------------------------------
BUSINESS_METRICS = [
    ("3", "Líneas de negocio integradas"),
    ("B2C · B2B", "Modelo dual de ingresos"),
    ("70%", "Reducción de tiempo de soporte estimada"),
    ("24/7", "Disponibilidad de tutoría"),
]

REVENUE_PROJECTION = {
    "anios": ["Año 1", "Año 2", "Año 3", "Año 4"],
    "b2c": [12, 38, 95, 180],     # MM CLP
    "b2b": [20, 70, 160, 340],    # MM CLP
}

MARKET_SEGMENTS = [
    ("Estudiantes de ingeniería (LATAM)", 35),
    ("Capacitación industrial / técnica", 40),
    ("Agentes B2B institucionales", 25),
]

DIFFERENTIATORS = [
    ("Especialización técnica real", "Foco en ingeniería eléctrica e industrial, no contenido genérico."),
    ("Modelo dual B2C + B2B", "Aprendizaje individual y servicios institucionales en una sola plataforma."),
    ("IA con datos propios y privados", "Agentes RAG desplegables on-premise para clientes sensibles."),
    ("Escalable por configuración", "Nuevos dominios y clientes se incorporan sin reescribir la plataforma."),
]
