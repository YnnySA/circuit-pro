# 🌍 Sistema de Multi-Idioma — CircuitProAI

> **Estado actual:** ✅ 100% implementado en todas las páginas y componentes.

---

## 🎯 Cómo funciona el sistema

El usuario cambia el idioma mediante un `selectbox` en la esquina superior derecha. El código persiste la selección en `st.session_state["language"]` y ejecuta `st.rerun()` para que toda la UI se re-renderice en el nuevo idioma. No hay llamadas a APIs externas: todas las traducciones viven en memoria en `data/i18n.py`.

```
┌───────────────────────────────────────────────────┐
│  CircuitProAI                     [Idioma ▼]  │
│  [Español / English]                          │
└───────────────────────────────────────────────────┘

Usuario cambia idioma
        ↓
set_language(new_lang)  →  st.session_state["language"] = "en"
        ↓
st.rerun()
        ↓
Cada página llama get_language() y usa t(clave, lang)
```

---

## 📁 Arquitectura de archivos

```
circuit-pro/
├── app.py                    ← Selector de idioma + sidebar_brand(lang)
├── data/
│   └── i18n.py               ← Única fuente de verdad para todos los textos
├── components/
│   └── ui.py                 ← sidebar_brand(lang) — recibe lang como parámetro
└── pages/
    ├── 0_Inicio.py           ← t() para hero, métricas y secciones
    ├── 1_Estudiantes.py      ← t() para tabs, métricas y mensajes
    ├── 2_Industria.py        ← t() para tabs, rutas, caso y checklist
    ├── 3_Agentes.py          ← t() para pipeline, demo y casos de uso
    └── 4_Negocio.py          ← t() para métricas, gráficos y modelo
```

---

## 🔑 API principal

### `t(key, lang)` — obtener una traducción

```python
from data.i18n import t, get_language

lang = get_language()          # lee st.session_state["language"]
st.markdown(t("nav.inicio", lang))   # → "Inicio" o "Home"
```

Si la clave no existe, `t()` devuelve la clave misma como fallback — nunca crashea.

### Convención de claves

Todas las claves usan prefijo de página o componente seguido de punto:

| Prefijo | Ámbito |
|---|---|
| `nav.*` | Ítems de navegación lateral |
| `sidebar.*` | Componentes del sidebar (brand, prototype, copyright) |
| `inicio.*` | Página Home |
| `estudiantes.*` | Módulo Estudiantes |
| `industria.*` | Módulo Industria |
| `agentes.*` | Módulo Agentes B2B |
| `negocio.*` | Módulo Negocio |
| `btn.*` | Botones reutilizables |
| `msg.*` | Mensajes de feedback |
| `metric.*` | Etiquetas de métricas genéricas |
| `fc.*` | Simulador Flujo de Carga |

---

## 🐛 Post-mortem: bugs encontrados en producción (2026-08-08)

Esta sección documenta los dos errores reales que causaron que el cambio de idioma no funcionara en producción, para que no se repitan.

---

### Bug #1 — Texto hardcodeado dentro de HTML en un componente

**Archivo afectado:** `components/ui.py` — función `sidebar_brand()`

**Código problemático:**
```python
# ❌ MALO — el texto está fijo en el string HTML
def sidebar_brand():
    st.sidebar.markdown(
        f"""...<span>IA aplicada a educación e industria</span>...""",
        unsafe_allow_html=True,
    )
```

**Por qué falla:** La función no recibe `lang` como parámetro, y el texto está interpolado directamente dentro del f-string del HTML. Aunque `data/i18n.py` tuviera la clave `sidebar.tagline` correctamente definida en ambos idiomas, esta función jamás la consultaba.

**Fix aplicado:**
```python
# ✅ CORRECTO — lang entra como parámetro y t() construye el texto
def sidebar_brand(lang: str = "es"):
    from data.i18n import t
    tagline = t("sidebar.tagline", lang)   # resuelto ANTES de armar el HTML
    st.sidebar.markdown(
        f"""...<span>{tagline}</span>...""",
        unsafe_allow_html=True,
    )
```

**Regla derivada:** Cualquier función de `components/ui.py` que renderice texto visible al usuario **debe** recibir `lang` como parámetro y llamar a `t()`. Nunca incrustar strings de UI directamente en HTML.

---

### Bug #2 — Labels de métricas leídos desde `mock_data` en vez de `i18n`

**Archivo afectado:** `pages/0_Inicio.py` — bloque de métricas de cabecera

**Código problemático:**
```python
# ❌ MALO — desempaqueta (valor, label) directo de mock_data (solo español)
from data.mock_data import BUSINESS_METRICS

for col, (num, label) in zip(cols, BUSINESS_METRICS):
    with col:
        metric_card(num, label)   # label siempre en español
```

**Por qué falla:** `BUSINESS_METRICS` es una lista de tuplas `(valor, etiqueta_es)` definida en `mock_data.py`. El label es datos de contenido, no de UI — pero al desempaquetarlo directamente se salta por completo el sistema i18n.

**Fix aplicado:**
```python
# ✅ CORRECTO — valores desde mock_data, labels desde i18n
METRIC_LABELS = [
    t("inicio.metric_label_0", lang),   # "Líneas de negocio integradas" / "Integrated business lines"
    t("inicio.metric_label_1", lang),   # "Modelo dual de ingresos" / "Dual revenue model"
    t("inicio.metric_label_2", lang),   # "Reducción de tiempo de soporte" / "Support time reduction"
    t("inicio.metric_label_3", lang),   # "Disponibilidad de tutoría" / "Tutoring availability"
]
METRIC_VALUES = [item[0] for item in BUSINESS_METRICS]  # solo el número

for col, num, label in zip(cols, METRIC_VALUES, METRIC_LABELS):
    with col:
        metric_card(num, label)
```

**Regla derivada:** `mock_data.py` almacena **valores numéricos o datos estructurales** solamente. Todo texto visible al usuario — incluso si está dentro de mock_data — debe tener su clave en `i18n.py` y ser resuelto con `t()`.

---

### Bug #3 — Llamada a componente sin pasar `lang` (el más sutil)

**Archivo afectado:** `app.py`

**Código problemático:**
```python
# ❌ MALO — sidebar_brand() usa su default lang="es" siempre
sidebar_brand()   # ← nunca cambia a inglés aunque el usuario lo seleccione
```

**Por qué falla:** Aunque Bug #1 ya estaba corregido (la función ahora acepta `lang`), la llamada en `app.py` no pasaba el argumento. El default `lang="es"` en la firma de `sidebar_brand` hizo que este error pasara silencioso — no crashea, simplemente siempre muestra español.

**Fix aplicado:**
```python
# ✅ CORRECTO — leer lang ANTES de llamar a cualquier componente
lang = get_language()
sidebar_brand(lang)   # ← ahora respeta el idioma del usuario
```

**Regla derivada:** En `app.py`, la línea `lang = get_language()` debe estar **antes** de cualquier llamada a componentes de UI. El orden importa.

---

## ⚠️ Anti-patrones — Lista de verificación

Antes de hacer commit de cualquier cambio de UI, verifica que **ninguno** de estos errores esté presente:

```python
# ❌ 1. Texto UI hardcodeado en HTML
st.markdown("<span>Texto en español</span>", unsafe_allow_html=True)

# ❌ 2. Componente UI sin recibir lang
def mi_componente():
    st.write("Texto fijo")

# ❌ 3. Labels provenientes de mock_data directamente
for nombre, valor, label in MOCK_DATA:
    st.metric(label, valor)   # label podría ser solo español

# ❌ 4. Llamada a componente sin pasar lang
mi_componente()   # olvidó pasar lang

# ❌ 5. Obtener lang después de usarlo
sidebar_brand(lang)   # ← lang no definido aún aquí
lang = get_language() # ← demasiado tarde
```

---

## ✅ Estado por archivo

| Archivo | Estado | Notas |
|---|---|---|
| `data/i18n.py` | ✅ Completo | ~200 claves en `es` + `en` |
| `app.py` | ✅ Completo | Selector + `sidebar_brand(lang)` |
| `components/ui.py` | ✅ Completo | `sidebar_brand(lang)` con `t()` |
| `pages/0_Inicio.py` | ✅ Completo | Hero + métricas + secciones |
| `pages/1_Estudiantes.py` | ✅ Completo | Tabs + métricas + simuladores |
| `pages/2_Industria.py` | ✅ Completo | Rutas + caso + checklist |
| `pages/3_Agentes.py` | ✅ Completo | Pipeline + demo + casos |
| `pages/4_Negocio.py` | ✅ Completo | Finanzas + mercado + diferenciadores |

---

## 📦 Agregar una nueva clave de traducción

1. **Añade la clave en `data/i18n.py`** en ambos idiomas:

```python
TRANSLATIONS = {
    "es": {
        ...
        "nueva.clave": "Texto en español",
    },
    "en": {
        ...
        "nueva.clave": "Text in English",
    },
}
```

2. **Úsal a en tu página o componente:**

```python
lang = get_language()
st.write(t("nueva.clave", lang))
```

3. **Si es un componente de `ui.py`**, asígurate de que la función reciba `lang` como parámetro:

```python
def mi_componente(lang: str = "es"):
    from data.i18n import t
    texto = t("nueva.clave", lang)
    st.markdown(f"<div>{texto}</div>", unsafe_allow_html=True)
```

---

## 📖 Documentación asociada

- **`TRANSLATION_GUIDE.md`** — Guía paso a paso para traducir nuevo contenido
- **`TESTING_i18n.md`** — Casos de prueba para verificar el sistema
- **`data/i18n.py`** — Diccionario completo con comentarios por sección
