# 🧪 Prueba del Sistema Multi-Idioma (i18n)

## Verificación Rápida

### 1. Inicia la Aplicación
```bash
cd circuitpro
streamlit run app.py
```

La aplicación debe abrir automáticamente en `http://localhost:8501`.

### 2. Ubica el Selector de Idioma
```
En la esquina SUPERIOR DERECHA de la pantalla,
verás un widget selectbox con dos opciones:
  • Español
  • English
```

### 3. Cambia el Idioma
- Haz clic en el selectbox
- Selecciona "English"
- La página **debe actualizar automáticamente** (con `st.rerun()`)

### 4. Verifica las Traducciones

#### Navegación Lateral (Sidebar)
- **Antes:** "Plataforma", "Módulos", "Asistencia Especializada"
- **Después:** "Platform", "Modules", "Specialized Assistance"

#### Títulos de Páginas
- **Antes:** "Inicio", "Estudiantes", "Capacitación industrial"
- **Después:** "Home", "Students", "Industrial Training"

#### Página de Inicio
- **Antes:** "CircuitProIA — aprende, capacita y automatiza..."
- **Después:** "CircuitProIA — Learn, Train & Automate..."

#### Página de Estudiantes
- **Antes:** "Módulo · Estudiantes", "Progreso global del curso"
- **Después:** "Module · Students", "Overall course progress"

### 5. Navega Entre Páginas
- Ve a diferentes páginas (Inicio, Estudiantes, etc.)
- Verifica que **el idioma se mantiene** al navegar
- Cambia el idioma nuevamente a Español
- **Debe actualizar en todas las páginas**

## Checklist de Validación

| Feature | Español | English | Status |
|---------|---------|---------|--------|
| Selector de idioma visible | ✓ | ✓ | ? |
| Navegación lateral traducida | ✓ | ✓ | ? |
| Títulos de páginas traducidos | ✓ | ✓ | ? |
| Página Inicio completamente traducida | ✓ | ✓ | ? |
| Página Estudiantes completamente traducida | ✓ | ✓ | ? |
| Idioma persiste al navegar | ✓ | ✓ | ? |
| Cambio dinámico (st.rerun) funciona | ✓ | ✓ | ? |

## Pruebas Avanzadas

### Test 1: Persistencia de Estado
1. Cambia a "English"
2. Abre navegador en nueva pestaña y accede a `http://localhost:8501`
3. **Resultado esperado:** El nuevo navegador **NO** hereda el idioma (está en sesión separada)
4. Regresa a la pestaña original
5. **Resultado esperado:** Sigue en "English"

### Test 2: Múltiples Usuarios (Simulado)
1. Abre dos navegadores diferentes (Chrome + Firefox, o normal + incógnito)
2. En uno pon "Español", en otro "English"
3. **Resultado esperado:** Cada uno mantiene su propio idioma

### Test 3: Widgets Secundarios
1. Cambia a "English"
2. Navega a "Estudiantes"
3. Abre algún expander o pestaña
4. **Resultado esperado:** Los textos internos de modules aún están en **español** (traducción pendiente)

## Resolución de Problemas

### El selector de idioma no aparece
- Verifica que `app.py` tiene las líneas 40-53 actualizar
- Ejecuta: `python -m py_compile app.py`
- Reinicia: `streamlit run app.py`

### El cambio de idioma no se refleja
- Asegúrate de que `data/i18n.py` existe
- Verifica que la función `t()` es importada correctamente
- Revisa la consola de Streamlit por errores

### Error: "ModuleNotFoundError: No module named 'data.i18n'"
- Asegúrate de estar en el directorio `circuitpro`
- Verifica que `data/i18n.py` existe
- Ejecuta: `python -c "from data.i18n import t; print('OK')"`

### El selector desaparece después de cambiar de idioma
- Es normal que Streamlit recrear widgets después de `st.rerun()`
- El selector debe reaparecer inmediatamente
- Si desaparece por más de 2 segundos, hay un error en el `rerun()`

## Observaciones Esperadas

✅ **El selector debe estar en la ESQUINA SUPERIOR DERECHA**
- Si no ves ese selectbox, revisa líneas 40-53 de `app.py`

✅ **Al cambiar idioma, la página se actualiza rápidamente**
- Verás un parpadeo breve (es el `st.rerun()`)

✅ **La navegación cambia de idioma, pero el contenido de módulos aún está en español**
- Es esperado: `teoria.py`, `glosario.py`, etc. aún no han sido traducidos
- Ver `TRANSLATION_GUIDE.md` para continuar traduciendo

## Debugging

Si algo no funciona, ejecuta esto en Python:

```python
# En el directorio circuitpro/
from data.i18n import t, get_language, set_language

# Prueba la función t()
print(t("nav.inicio", "es"))  # Debe imprimir: "Inicio"
print(t("nav.inicio", "en"))  # Debe imprimir: "Home"

# Prueba las funciones de estado (solo funcionan dentro de Streamlit)
import streamlit as st
st.write(f"Idioma actual: {get_language()}")
```

## Siguientes Pasos

Cuando hayas verificado que todo funciona:

1. Lee `TRANSLATION_GUIDE.md`
2. Abre `data/i18n.py` y familiarízate con la estructura
3. Comienza a traducir `modules/students/unit_1/teoria.py` siguiendo el patrón

---

**¿Encontraste un bug?** Documéntalo y reporta:
- Qué página estabas viendo
- Qué idioma seleccionaste
- Qué no se tradujo
- Screenshot si es posible
