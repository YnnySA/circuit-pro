# CircuitProIA — Plataforma de IA aplicada a educación e industria

Prototipo funcional en **Streamlit** para presentación de pitch. Integra tres módulos
de negocio en una sola plataforma con navegación multipágina.

## Módulos

1. **🎓 Estudiantes de ingeniería eléctrica** — laboratorio digital con guías por unidad,
   ejercicios interactivos, gráficos en tiempo real, retroalimentación inmediata e
   indicadores de progreso.
2. **🏭 Capacitación industrial** — rutas de formación por competencias, casos prácticos,
   simulaciones y checklist de cumplimiento.
3. **🤖 Agentes tutores B2B** — agentes personalizados con RAG sobre el conocimiento de
   cada institución, demo de chat y despliegue privado.

Más una sección de **📈 Impacto y negocio** con proyecciones, mercado objetivo y
diferenciación, pensada para jurados e inversionistas.

## Estructura del proyecto

```
voltiq/
├── app.py                  # Punto de entrada y navegación (st.navigation)
├── requirements.txt
├── .streamlit/
│   └── config.toml         # Tema visual
├── components/
│   ├── theme.py            # Paleta, CSS global y configuración de página
│   └── ui.py               # Componentes reutilizables (tarjetas, métricas, chips...)
├── data/
│   └── mock_data.py        # Datos de ejemplo simulados
└── pages/
    ├── 0_Inicio.py         # Landing / propuesta de valor
    ├── 1_Estudiantes.py    # Módulo 1
    ├── 2_Industria.py      # Módulo 2
    ├── 3_Agentes.py        # Módulo 3
    └── 4_Negocio.py        # Impacto y negocio
```

## Cómo ejecutar

```bash
cd voltiq
pip install -r requirements.txt
streamlit run app.py
```

La aplicación se abre en `http://localhost:8501`. Navega entre módulos con el menú lateral.

## Notas

- Es un **prototipo de demostración**: los datos y respuestas del agente son simulados.
- El estado de los ejercicios y checklists se mantiene con `st.session_state`.
- Diseñado para verse sólido y creíble en un pitch, no como sistema en producción.
