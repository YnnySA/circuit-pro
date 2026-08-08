# Guía de Traducción (i18n) para CircuitProIA

## ¿Qué se ha hecho?

Se ha implementado un sistema completo de **multi-idioma (i18n)** con soporte para **español e inglés**.

### Cambios Principales:

1. **Sistema de Traducción Centralizado** (`data/i18n.py`)
   - Diccionario `TRANSLATIONS` con pares clave-valor para cada idioma
   - Función `t(key, lang)` para obtener traducciones
   - Funciones `get_language()` y `set_language()` para manejar el idioma en `st.session_state`

2. **Selector de Idioma** (esquina superior derecha)
   - Agregado en `app.py` con selectbox en columna derecha
   - Opciones: "Español" / "English"
   - Cambio automático de idioma con `st.rerun()`

3. **Navegación Traducida**
   - Títulos de páginas usan `t()` en `app.py`
   - Menú lateral traducido

4. **Firmas de Módulos Actualizadas**
   - Todos los módulos en `modules/students/unit_1/` ahora aceptan `lang: str = "es"`
   - Importan la función `t()` de `data/i18n.py`

## Cómo Agregar Traducciones

### Paso 1: Agregar la Clave en `data/i18n.py`

Abre `data/i18n.py` y agrega tu texto en ambos idiomas:

```python
TRANSLATIONS = {
    "es": {
        "mipagina.mi_clave": "Texto en español aquí",
        ...
    },
    "en": {
        "mipagina.mi_clave": "Text in English here",
        ...
    },
}
```

**Convención de nombres de claves:**
- Usa puntos para agrupar: `seccion.descripcion.detalle`
- Ejemplos: `inicio.pill`, `estudiantes.metric_progress`, `msg.correct`

### Paso 2: Usar la Traducción en tu Código

En el módulo o página que necesita traducción:

```python
from data.i18n import t, get_language

lang = get_language()
st.markdown(t("mipagina.mi_clave", lang))
```

## Traducción de Módulos Pendientes

Los siguientes módulos necesitan traducción de contenido interno:

### Prioritarios:

1. **`modules/students/unit_1/teoria.py`**
   - Títulos y secciones numeradas
   - Explícadores en markdown
   - Ejemplos matemáticos
   
   Clave sugerida: `teoria.section_N_title`, `teoria.section_N_text`

2. **`modules/students/unit_1/glosario.py`**
   - Términos y definiciones
   - Clave sugerida: Mantener estructura de `TERMINOS` (lista de dicts) y traducir dentro del render()

3. **`modules/students/unit_1/ejercicios.py`**
   - Enunciados, opciones, explicaciones
   - Clave sugerida: `ejercicio.ej{id}.titulo`, `ejercicio.ej{id}.enunciado`

### Módulos Avanzados:

4. **`modules/students/unit_1/graficos.py`** — Etiquetas de UI
5. **`modules/students/unit_1/flujo_carga.py`** — Labels y validaciones
6. **`modules/students/unit_1/factor_potencia.py`** — Mensajes y tooltips
7. **`modules/students/unit_1/sistema6.py`** — Análisis de armónicos

### Páginas Principales:

8. **`pages/2_Industria.py`** — Capacitación industrial
9. **`pages/3_Agentes.py`** — Agentes B2B
10. **`pages/4_Negocio.py`** — Impacto y negocio

## Ejemplo Completo: Traducir un Ejercicio

### Antes (sin traducción):
```python
EJERCICIOS = [
    {
        "id": "ej1",
        "titulo": "Circuito serie con tres resistencias",
        "enunciado": "Una red tiene...",
        "opciones": ["Opción A", "Opción B"],
        "correcta": "Opción A",
    }
]
```

### Después (con traducción):
```python
# data/i18n.py
TRANSLATIONS = {
    "es": {
        "ejercicio.ej1.titulo": "Circuito serie con tres resistencias",
        "ejercicio.ej1.enunciado": "Una red tiene...",
        "ejercicio.ej1.opcion_a": "Opción A",
        "ejercicio.ej1.opcion_b": "Opción B",
    },
    "en": {
        "ejercicio.ej1.titulo": "Series circuit with three resistors",
        "ejercicio.ej1.enunciado": "A network has...",
        "ejercicio.ej1.opcion_a": "Option A",
        "ejercicio.ej1.opcion_b": "Option B",
    }
}

# modules/students/unit_1/ejercicios.py
from data.i18n import t, get_language

def render(lang: str = "es"):
    lang = get_language()
    
    # Usar las traducciones
    titulo = t("ejercicio.ej1.titulo", lang)
    enunciado = t("ejercicio.ej1.enunciado", lang)
    # ... etc
```

## Test Rápido

Para probar el sistema de i18n:

1. Inicia la aplicación: `streamlit run app.py`
2. En la esquina superior derecha, cambia entre idiomas
3. Verifica que:
   - El menú de navegación cambia
   - La página de inicio cambia
   - El idioma se preserva al navegar entre páginas

## Arquitectura

```
app.py (inicia i18n, proporciona selector)
  ↓
st.session_state["language"]  ("es" o "en")
  ↓
pages/*.py (usan get_language())
  ↓
modules/unit_1/*.py (reciben lang como parámetro)
  ↓
data/i18n.py (función t() resuelve traducciones)
```

## Próximos Pasos Sugeridos

1. **Traducir teoria.py** — Contenido teórico principal
2. **Traducir ejercicios.py** — Banco de ejercicios
3. **Traducir glosario.py** — Términos técnicos
4. **Traducir páginas 2-4** — Industria, Agentes, Negocio
5. **Agregar más idiomas** — Añadir nuevas claves en TRANSLATIONS

## Notas Importantes

- No traducir términos técnicos especializados (V, A, Ω, RAG, LLM, etc.) a menos que sea necesario
- Mantener consistencia terminológica entre idiomas (ej: "impedancia" = "impedance")
- Usar formato markdown para matemáticas en ambos idiomas
- Probar cambios de idioma después de cada modificación

---

**¿Preguntas?** Revisa `data/i18n.py` para ver el formato completo de traducciones.
