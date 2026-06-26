# CircuitProIA — Plataforma Educativa e Industrial con IA

**CircuitProIA (Voltiq)** es una plataforma especializada en educación e ingeniería eléctrica con inteligencia artificial, desarrollada como prototipo funcional v0.1 en **Streamlit** para presentación de pitch a inversores y jurados.

## 🎯 Propósito

Integra tres líneas de negocio en una plataforma única:
- **B2C:** Laboratorio digital de educación técnica con suscripción para estudiantes
- **B2B:** Agentes tutores personalizados (on-premise) para instituciones y empresas industriales
- **📈 Impacto:** Proyecciones financieras, análisis de mercado y diferenciadores competitivos

## 📚 Módulos

### 1️⃣ **🎓 Estudiantes — Laboratorio Digital de Ingeniería Eléctrica**
Plataforma interactiva para estudiantes con:
- **Guías de aprendizaje:** Contenido teórico organizado por unidades (DC, AC, Trifásico, Máquinas)
- **Ejercicios interactivos:** Banco de ejercicios con evaluación inmediata y retroalimentación detallada
- **Cuestionarios formativos:** 2 cuestionarios (23 preguntas) con retroalimentación formativa: 2 intentos por pregunta, pista al 1er error, revelación de la respuesta al 2do error, puntaje final por rangos
- **Glosario técnico:** 15+ términos eléctricos con definiciones, unidades y categorización
- **Simuladores en tiempo real:** RLC serie, diagramas fasoriales, curvas de Bode
- **Indicadores de progreso:** Seguimiento de avance global, por unidad, respuestas correctas, rachas

**Estado:** Unidad 1 (DC-AC) completamente desarrollada. Unidades 2-4 en construcción.

### 2️⃣ **🏭 Industria — Capacitación Aplicada**
Módulo de formación empresarial con:
- **Rutas por competencias:** LOTO (Bloqueo/Etiquetado), Mantenimiento predictivo, Eficiencia energética
- **Casos prácticos:** Simulaciones reales de decisiones de seguridad e ingeniería
- **Checklist de cumplimiento:** 6 items interactivos con progreso en vivo
- **Métricas de avance:** Rutas completadas, horas acumuladas, porcentaje de cumplimiento

**Estado:** Funcional con datos de ejemplo.

### 3️⃣ **🤖 Agentes — Tutores B2B Personalizados (RAG)**
Módulo de demostración de agentes tutores:
- **Pipeline RAG:** 5 etapas (Ingesta, Indexación, Especialización, Despliegue, Monitoreo)
- **Chat simulado:** Selectbox con base de conocimiento + respuesta RAG simulada
- **Casos de uso:** 3 escenarios reales (Universidad, Empresa distribuidora, Planta industrial)
- **Beneficios:** Privacidad, Conocimiento especializado, Integración, Mejora continua

**Estado:** Demo funcional. RAG no integrado con LLM real (simulado).

### 4️⃣ **📈 Negocio — Impacto y Financiero**
Sección de pitch con:
- **Proyecciones de ingresos:** Gráficos interactivos B2C vs B2B (años 1-4)
- **Análisis de mercado:** Distribución por segmento
- **Diferenciadores:** 4 ventajas competitivas clave
- **Modelo dual:** Explicación de estrategia B2C + B2B

**Estado:** Completo con datos de ejemplo.

## 🏗️ Estructura del Proyecto

```
voltiq/
├── app.py                          # Punto de entrada y navegación (st.navigation)
├── README.md                       # Este archivo
├── requirements.txt                # Dependencias Python
├── .gitignore                      # Archivos ignorados por git
│
├── .streamlit/
│   └── config.toml                 # Configuración de tema Streamlit
│
├── components/                     # Sistema de componentes reutilizables
│   ├── theme.py                    # Paleta de colores, CSS global, configuración de página
│   └── ui.py                       # Componentes declarativos (cards, metrics, chips, steps, etc.)
│
├── data/                           # Datos centralizados
│   ├── mock_data.py                # Datos simulados para todos los módulos
│   ├── cuestionarios_data.py       # Preguntas de los cuestionarios formativos (Dr. Maykop Pérez M., UdeC)
│   └── unidad_1_data.py            # Datos específicos de Unidad 1
│
├── modules/                        # Contenido educativo por módulo
│   └── students/
│       └── unit_1/
│           ├── __init__.py
│           ├── teoria.py           # Contenido teórico (12+ secciones con LaTeX)
│           ├── ejercicios.py       # Banco de ejercicios + selector de cuestionarios formativos
│           ├── cuestionarios.py    # Mecánica de evaluación formativa (2 intentos · pista · revelar · puntaje)
│           ├── glosario.py         # Diccionario de términos eléctricos
│           └── graficos.py         # Simuladores interactivos con Plotly
│
└── pages/                          # Páginas principales (Streamlit multipage)
    ├── 0_Inicio.py                 # Landing: propuesta de valor, métricas, tecnologías
    ├── 1_Estudiantes.py            # Módulo 1: Guías, Glosario, Ejercicios, Gráficos
    ├── 2_Industria.py              # Módulo 2: Rutas, Caso práctico, Checklist
    ├── 3_Agentes.py                # Módulo 3: Pipeline RAG, Beneficios, Demo chat, Casos
    └── 4_Negocio.py                # Módulo 4: Proyecciones, Mercado, Diferenciadores
```

## 🎨 Características Técnicas

- ✅ **Navegación multipágina** con `st.navigation()` — 5 páginas en 2 grupos temáticos
- ✅ **Componentes declarativos** — Sistema de UI reutilizable (cards, metrics, chips, steps)
- ✅ **Ejercicios interactivos** — Radio buttons, evaluación inmediata, explicaciones detalladas
- ✅ **Gráficos interactivos** — Sliders conectados a Plotly en tiempo real
- ✅ **Checklists dinámicos** — Progreso en vivo con checkboxes
- ✅ **Simuladores** — RLC serie, diagramas fasoriales, curvas de Bode
- ✅ **Tema visual centralizado** — 9 colores, tipografía Inter, CSS global inyectado
- ✅ **Estado compartido** — `st.session_state` para persistencia de ejercicios, checklists
- ✅ **Indicadores de progreso** — Métricas visuales actualizadas en tiempo real

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.8+
- pip o conda

### Setup
```bash
# 1. Clonar repositorio
git clone https://github.com/tuuser/voltiq.git
cd voltiq

# 2. Crear y activar entorno virtual (recomendado)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar aplicación
streamlit run app.py
```

La aplicación se abre automáticamente en `http://localhost:8501`.

### Navegación
- Menú lateral izquierdo para cambiar entre módulos
- Cada módulo tiene tabs con diferentes secciones
- Ejercicios y checklists mantienen su estado durante la sesión

## 🎨 Paleta de Colores

```
🔵 Primario:      #0B5FFF  (Azul eléctrico)
🔷 Secundario:    #00C2D1  (Cian energético)
🟠 Acento:        #FFB020  (Ámbar)
⚫ Texto:          #0E1726  (Azul marino oscuro)
⚪ Fondo:          #F6F8FC  (Gris muy suave)
```

Tipografía: **Inter** (Google Fonts, weights 400-800)

## 📊 Estado del Proyecto

| Componente | Estado | Notas |
|-----------|--------|-------|
| **Navegación** | ✅ Completo | st.navigation funcional |
| **Módulo 1 (Unit 1)** | ✅ Completo | Contenido, ejercicios, glosario, gráficos |
| **Módulo 1 (Units 2-4)** | 🔄 En construcción | Estructura lista, contenido pendiente |
| **Módulo 2** | ✅ Completo | Rutas, caso práctico, checklist |
| **Módulo 3** | ✅ Demostrable | Chat simulado, RAG no integrado |
| **Módulo 4** | ✅ Completo | Proyecciones, mercado, diferenciadores |
| **Componentes UI** | ✅ Pulido | Sistema robusto y consistente |
| **Base de datos** | ❌ No implementada | Datos en memoria (session_state) |
| **Autenticación** | ❌ No implementada | Sin tracking de usuarios |
| **RAG real** | ❌ No implementado | Simulación funcional |

**Versión:** v0.1 — Prototipo navegable para pitch

## ⚠️ Issues Conocidos

| Issue | Severidad | Solución |
|-------|-----------|----------|
| Plotly no en requirements.txt | 🔴 Alta | Agregar `plotly>=5.0` (FIXED en este commit) |
| Unidades 2-4 no completadas | 🟡 Media | Seguir desarrollo según roadmap |
| RAG es simulado | 🟡 Media | Integrar LLM real en futuro (LangChain + OpenAI) |
| Sin persistencia de datos | 🟡 Media | Agregar BD (PostgreSQL) en v0.2 |
| Sin autenticación | 🟡 Media | Implementar en v0.2 |

## 🔄 Patrones de Desarrollo

1. **Componentes Declarativos** — UI definida como funciones puras en `components/ui.py`
2. **Centralización de Datos** — Todos los datos mock en `data/mock_data.py`
3. **Separación por Responsabilidad** — Cada archivo (teoria.py, ejercicios.py, etc.) tiene una función `render()`
4. **Estado Explícito** — `st.session_state` bien organizado y documentado
5. **CSS Global Inyectado** — Clases reutilizables sin necesidad de archivos CSS externos
6. **Tabs Paralelas** — Organización clara de contenido en secciones

## 📦 Dependencias

Ver [requirements.txt](requirements.txt) para versiones completas.

**Mínimas:**
- `streamlit>=1.36` — Framework principal
- `pandas>=2.0` — Manejo de datos
- `numpy>=1.24` — Cálculos numéricos
- `plotly>=5.0` — Gráficos interactivos

## 🚀 Próximas Fases (v0.2+)

- [ ] Integrar LLM real para agentes RAG (LangChain + OpenAI)
- [ ] Agregar base de datos (PostgreSQL) para persistencia
- [ ] Implementar autenticación de usuarios
- [ ] Completar Unidades 2-4 del módulo de estudiantes
- [ ] Conectar con sistemas LMS (Moodle, Canvas)
- [ ] Agregar analytics y tracking de progreso
- [ ] Deploy en Streamlit Cloud / servidor propio

## 📝 Licencia

[Agregar licencia según corresponda]

## 👨‍💻 Autor

Desarrollado como tesis doctoral (7th Challenge - Doctorado)

## 📞 Contacto

[Agregar información de contacto si aplica]
