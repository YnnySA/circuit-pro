"""
Datos de los cuestionarios formativos — Unidad 1.
Contenido desarrollado por el Dr. Maykop Pérez Martínez,
Universidad de Concepción (UdeC) — Departamento de Ingeniería Eléctrica.

Cada cuestionario sigue una mecánica de evaluación formativa:
  - 2 intentos por pregunta
  - 1er error  -> se muestra una PISTA (sin revelar la respuesta)
  - 2do error  -> se REVELA la respuesta correcta + explicación
  - acierto    -> felicitación + explicación ('ok')
  - 'fb' contiene retroalimentación específica por opción incorrecta (opcional)

Esquema de cada pregunta:
  {
    "q":        str,        # enunciado (puede contener HTML inline: <strong>, <em>, sub/sup)
    "opciones": [str, ...], # 4 alternativas
    "correcta": int,        # índice 0-3 de la opción correcta
    "pista":    str,        # pista mostrada tras el 1er error
    "ok":       str,        # explicación mostrada al acertar o al revelar
    "fb":       [str, ...], # retroalimentación por opción (índice alineado a 'opciones')
  }
"""

# Atribución mostrada en la cabecera de los cuestionarios
AUTOR = {
    "nombre": "Dr. Maykop Pérez Martínez",
    "institucion": "Universidad de Concepción (UdeC)",
    "departamento": "Departamento de Ingeniería Eléctrica",
}

CUESTIONARIOS = {
    "circuitos": {
        "id": 'circuitos',
        "titulo": 'Cuestionario Formativo — Circuitos Eléctricos',
        "descripcion": '2 intentos por pregunta · pista al 1er error · respuesta al 2do error',
        "preguntas": [
            {
                "q": '¿Cuál es la función principal de los <strong>elementos activos</strong> en un circuito eléctrico?',
                "opciones": ['Bloquear el flujo de corriente continua.', 'Disipar energía en forma de calor o luz.', 'Almacenar energía en campos magnéticos.', 'Proporcionar energía eléctrica o ganancia a la red.'],
                "correcta": 3,
                "pista": 'Considere la diferencia entre <em>generar energía</em> y consumirla o transformarla.',
                "ok": 'Los elementos activos, como las fuentes de tensión y corriente, son capaces de <strong>suministrar energía</strong> al sistema.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'En el Sistema Internacional de Unidades, ¿en qué unidad se mide la <strong>carga eléctrica</strong>?',
                "opciones": ['Ampere (A)', 'Volt (V)', 'Coulomb (C)', 'Ohm (Ω)'],
                "correcta": 2,
                "pista": 'Recuerde el nombre del científico asociado a la ley de atracción entre cargas.',
                "ok": 'El <strong>coulomb</strong> es la unidad básica para cuantificar la propiedad eléctrica de las partículas atómicas.',
                "fb": ['', '', '', ''],
            },
            {
                "q": '¿Cómo se define la <strong>corriente eléctrica</strong> en términos de carga y tiempo?',
                "opciones": ['Es la fuerza necesaria para mover los electrones.', 'Es la tasa de cambio de la carga en el tiempo.', 'Es la energía total acumulada en un punto del conductor.', 'Es el producto de la resistencia por la tensión aplicada.'],
                "correcta": 1,
                "pista": 'Piense en la corriente como un <em>flujo o movimiento constante</em> de partículas.',
                "ok": 'La corriente representa la velocidad a la cual la carga eléctrica pasa por un punto de referencia determinado.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'Si una corriente varía <strong>sinusoidalmente</strong> con respecto al tiempo, ¿cómo se le denomina?',
                "opciones": ['Corriente Alterna (CA)', 'Corriente Pulsante', 'Corriente Directa (CD)', 'Corriente Estática'],
                "correcta": 0,
                "pista": 'Este es el tipo de corriente que se utiliza típicamente en los hogares para electrodomésticos.',
                "ok": '¡Exacto! La corriente alterna cambia de dirección y magnitud de forma periódica siguiendo una función <strong>seno o coseno</strong>.',
                "fb": ['', '', '', ''],
            },
            {
                "q": '¿Cuál es la forma correcta de conectar un <strong>voltímetro</strong> para medir la tensión en un elemento?',
                "opciones": ['En serie con el elemento.', 'Entre el borne positivo de la fuente y tierra únicamente.', 'En serie-paralelo dependiendo de la resistencia.', 'En paralelo con el elemento.'],
                "correcta": 3,
                "pista": 'La tensión se mide <em>entre los extremos</em> de un componente, no a través de él.',
                "ok": 'La tensión es una diferencia de potencial entre dos puntos, por lo que el medidor debe conectarse a <strong>ambos extremos</strong> del elemento.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'En el análisis de circuitos en el dominio de la frecuencia, ¿qué representa un <strong>fasor</strong>?',
                "opciones": ['La frecuencia angular medida en rad/s.', 'Un número real que indica la potencia consumida.', 'Un número complejo que representa la amplitud y la fase de una sinusoide.', 'La parte imaginaria de la resistencia eléctrica.'],
                "correcta": 2,
                "pista": 'Considere qué componentes de una onda sinusoidal son capturados al pasar al <em>dominio complejo</em>.',
                "ok": 'Los fasores permiten simplificar los cálculos al eliminar la dependencia explícita del tiempo de las señales sinusoidales.',
                "fb": ['', '', '', 'La resistencia es puramente real; la parte imaginaria de la impedancia es la <strong>reactancia</strong>.'],
            },
            {
                "q": 'Si el desfasaje relativo <em>φ</em> entre la tensión <em>u(t)</em> y la corriente <em>i(t)</em> es mayor a cero (<em>φ > 0</em>), ¿qué se puede afirmar?',
                "opciones": ['La corriente está en adelanto respecto a la tensión.', 'La tensión está en fase con la corriente.', 'La tensión está en adelanto respecto a la corriente.', 'El circuito es puramente resistivo.'],
                "correcta": 2,
                "pista": 'Relacione el <em>signo del ángulo</em> con la posición temporal de una onda frente a la otra.',
                "ok": 'Un ángulo positivo indica que el pico de la onda de tensión ocurre <strong>temporalmente antes</strong> que el de la corriente.',
                "fb": ['', '', '', 'En un circuito puramente resistivo, la tensión y la corriente alcanzan sus máximos al mismo tiempo (en fase).'],
            },
            {
                "q": 'La impedancia <em>Z</em> se compone de una parte real y una imaginaria. ¿Cómo se denomina a la <strong>parte imaginaria</strong>?',
                "opciones": ['Conductancia (G)', 'Reactancia (X)', 'Admitancia (Y)', 'Susceptancia (B)'],
                "correcta": 1,
                "pista": 'Esta propiedad puede ser <em>inductiva o capacitiva</em> dependiendo de su signo.',
                "ok": 'La <strong>reactancia</strong> representa la oposición debida a inductores (positiva) o condensadores (negativa).',
                "fb": ['', '', '', 'La susceptancia representa la parte imaginaria de la <strong>admitancia</strong>, no de la impedancia.'],
            },
            {
                "q": '¿Cómo se comporta un <strong>inductor (bobina)</strong> ante un estímulo de Corriente Directa (CD) en estado estacionario?',
                "opciones": ['Como una resistencia infinita.', 'Como un <strong>cortocircuito</strong>.', 'Como un circuito abierto.', 'Generando una tensión alterna constante.'],
                "correcta": 1,
                "pista": 'Piense en el valor de la impedancia <em>Z<sub>L</sub> = jωL</em> cuando la frecuencia es <strong>cero</strong>.',
                "ok": 'Cuando ω = 0 (CD), <em>Z<sub>L</sub> = j(0)L = 0</em>, por lo que el inductor se comporta como un <strong>cortocircuito</strong>.',
                "fb": ['', '', '', 'Un inductor pasivo no genera energía; bajo CD no hay variación de flujo que induzca tensión.'],
            },
            {
                "q": '¿Cuál es la relación matemática entre la <strong>impedancia (Z)</strong> y la <strong>admitancia (Y)</strong>?',
                "opciones": ['Y = Z · cos(φ)', 'Y = 1 / Z', 'Y = R + jB', 'Y = Z²'],
                "correcta": 1,
                "pista": 'Es una relación de <em>reciprocidad matemática</em> similar a la de resistencia y conductancia.',
                "ok": 'La admitancia se define como el <strong>inverso de la impedancia</strong> y mide la facilidad de flujo de corriente.',
                "fb": ['', '', '', ''],
            },
        ],
    },
    "analisis": {
        "id": 'analisis',
        "titulo": 'Cuestionario Formativo — Análisis de Circuitos',
        "descripcion": '2 intentos por pregunta · pista al 1er error · respuesta al 2do error',
        "preguntas": [
            {
                "q": '¿Qué característica define fundamentalmente a un <em>elemento activo</em> en un circuito eléctrico?',
                "opciones": ['Que su impedancia interna siempre es igual a cero en cualquier condición.', 'Su capacidad exclusiva para disipar energía en forma de calor.', 'Su capacidad para generar energía, suministrar ganancia o ejercer control.', 'Actuar únicamente como un punto de conexión entre tres o más conductores.'],
                "correcta": 2,
                "pista": 'Considere si el elemento simplemente consume energía o si puede <em>aportarla o modificarla</em> activamente.',
                "ok": 'Los <strong>elementos activos</strong> se distinguen por su capacidad de inyectar energía neta al circuito o controlar el flujo de energía, como generadores o amplificadores.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'En una <em>fuente de tensión independiente ideal</em>, ¿qué sucede con la corriente que entrega al circuito?',
                "opciones": ['Entrega cualquier corriente necesaria para mantener su tensión terminal establecida.', 'La corriente es siempre constante independientemente de la tensión en sus terminales.', 'No puede entregar corriente si la resistencia de carga es mayor a un valor crítico.', 'La corriente depende proporcionalmente de la temperatura del generador.'],
                "correcta": 0,
                "pista": 'Recuerde que el valor de la <em>tensión es el parámetro fijo</em> en este tipo de fuentes.',
                "ok": 'Una fuente de tensión ideal mantiene su voltaje constante e independiente de la carga, <strong>ajustando la corriente</strong> según lo requiera el circuito externo.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'Al realizar una <em>transformación equivalente</em> entre una fuente real de tensión y una de corriente, ¿en qué punto son realmente equivalentes?',
                "opciones": ['Únicamente cuando la frecuencia de la señal es igual a cero (CD).', 'Solo cuando la impedancia asociada es puramente reactiva.', 'Tanto interna como externamente en todas las condiciones de operación.', 'Solo con respecto a lo que sucede externamente entre los terminales de carga.'],
                "correcta": 3,
                "pista": 'Piense en si el consumo de energía <em>dentro de la propia estructura</em> de la fuente es el mismo en ambas configuraciones.',
                "ok": 'La transformación asegura que la carga conectada no note la diferencia, pero las <strong>pérdidas internas</strong> de potencia en las impedancias serie y paralelo no son iguales.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'Defina el concepto de <em>rama</em> en el contexto de la topología de circuitos.',
                "opciones": ['Es cualquier trayectoria cerrada que permite el flujo de corriente.', 'Es el punto de unión donde concurren al menos tres conductores.', 'Es el elemento que suministra la mayor caída de tensión en un lazo.', 'Es el conjunto de elementos comprendidos entre dos nodos consecutivos.'],
                "correcta": 3,
                "pista": 'Considere la parte del circuito que <em>conecta un nodo con el siguiente</em>.',
                "ok": 'Una <strong>rama</strong> representa un camino único para la corriente entre dos puntos de conexión (nodos).',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'De acuerdo con la <em>Ley de Kirchhoff de Corriente (LKC)</em>, ¿cuál es la suma algebraica de las corrientes en un nodo?',
                "opciones": ['La suma es siempre igual a la corriente de la fuente de tensión principal.', 'La suma algebraica de las corrientes que entran y salen es igual a cero.', 'Es igual al producto de la tensión del nodo por la admitancia equivalente.', 'Es proporcional al número de lazos independientes que pasan por el nodo.'],
                "correcta": 1,
                "pista": 'Recuerde lo que sucede con la <em>carga eléctrica</em> en un punto de unión donde no hay almacenamiento.',
                "ok": 'La LKC se basa en el <strong>principio de conservación de la carga</strong>: no se acumula carga neta en un nodo.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'En un <em>divisor de tensión</em> con N impedancias en serie, ¿cómo se distribuye la tensión de la fuente?',
                "opciones": ['Por igual entre todas las impedancias, independientemente de sus valores.', 'En proporción inversa a los valores de las impedancias.', 'Solo a la impedancia con mayor conductancia.', 'En proporción directa a los valores de las impedancias.'],
                "correcta": 3,
                "pista": 'Considere la relación <em>V = Z · I</em> cuando la corriente es constante para todos los elementos.',
                "ok": 'A mayor impedancia en una conexión serie, <strong>mayor es la caída de tensión</strong> requerida para mantener la misma corriente en todos los elementos.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'Si una rama de un circuito en paralelo se encuentra en condición de <em>circuito abierto</em> (Z₂→∞), ¿qué sucede con la corriente total <em>I</em>?',
                "opciones": ['La corriente total aumenta hasta alcanzar valores infinitos.', 'La fuente de tensión deja de producir corriente en todas las demás ramas.', 'El 100% de la corriente se ve obligada a pasar por las trayectorias restantes.', 'La corriente se divide equitativamente entre la rama abierta y las cerradas.'],
                "correcta": 2,
                "pista": 'Piense en la oposición total al paso de corriente que ofrece un <em>espacio vacío o conductor roto</em>.',
                "ok": 'Un circuito abierto presenta resistencia infinita, por lo que <strong>ninguna corriente circula por esa rama</strong>, derivándose toda a los caminos con menor oposición.',
                "fb": ['', '', '', ''],
            },
            {
                "q": '¿Qué representa la <em>potencia reactiva (Q)</em> en un sistema de corriente alterna?',
                "opciones": ['La energía total facturada por la compañía eléctrica en un mes.', 'El calor generado por el efecto Joule en los conductores.', 'La potencia total consumida por las resistencias del circuito.', 'Una medida del intercambio de energía sin pérdidas entre la fuente y la parte reactiva de la carga.'],
                "correcta": 3,
                "pista": "Piense en la energía que <em>'va y viene'</em> entre los campos eléctricos/magnéticos y la fuente.",
                "ok": 'Los inductores y capacitores almacenan y devuelven energía al sistema; la potencia reactiva <strong>cuantifica este flujo oscilante</strong> que no realiza trabajo útil.',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'Si un circuito tiene un <em>factor de potencia en adelanto</em>, ¿qué tipo de carga predomina en el sistema?',
                "opciones": ['Carga inductiva.', 'Carga puramente resistiva.', 'Fuente de corriente continua.', 'Carga capacitiva.'],
                "correcta": 3,
                "pista": "Recuerde cuál de los elementos almacenadores de energía hace que la corriente <em>'llegue antes'</em> que el voltaje.",
                "ok": 'En un capacitor, la corriente se adelanta a la tensión, lo que resulta en un ángulo de impedancia negativo y un <strong>factor de potencia adelantado</strong>.',
                "fb": ['', '', '', ''],
            },
            {
                "q": '¿Cómo se calcula la <em>potencia aparente (S)</em> a partir de la potencia activa (P) y la reactiva (Q)?',
                "opciones": ['S = √(P² + Q²)', 'S = P · cos(φ)', 'S = P / Q', 'S = P + Q'],
                "correcta": 0,
                "pista": "Considere la geometría del <em>'Triángulo de Potencias'</em>.",
                "ok": 'Ya que P y Q son las componentes real e imaginaria de la potencia compleja, su magnitud total se obtiene con el <strong>Teorema de Pitágoras</strong>: S = √(P² + Q²).',
                "fb": ['', '', '', ''],
            },
            {
                "q": 'En la transformación <em>Delta a Estrella (Δ→Y)</em>, ¿cómo se calcula cada impedancia de la red Y?',
                "opciones": ['Como el inverso de la suma de las impedancias del lazo exterior.', 'Como la suma de las impedancias opuestas dividida por el producto de todas las ramas.', 'Como el producto de las dos impedancias Δ adyacentes dividido por la suma de las tres impedancias Δ.', 'Como la raíz cuadrada del producto de las admitancias en paralelo.'],
                "correcta": 2,
                "pista": "Piense en la relación que involucra a las ramas que <em>'tocan' el nodo de interés</em> en la configuración original.",
                "ok": 'La regla ZY = (Z₋ · Z₌) / (Z₊+Z₋+Z₌) permite encontrar el valor equivalente visto desde los nodos para <strong>transformar una malla cerrada en una conexión con punto neutro</strong>.',
                "fb": ['', '', '', ''],
            },
            {
                "q": '¿Qué unidad se utiliza comúnmente para medir la <em>energía eléctrica</em> en los recibos de consumo doméstico?',
                "opciones": ['Ampere por segundo (A/s)', 'Ohm-metro (Ω·m)', 'Watt-hora (Wh)', 'Volt-Ampere Reactivo (VAr)'],
                "correcta": 2,
                "pista": 'Considere el <em>producto de la potencia promedio por el tiempo</em> de uso.',
                "ok": 'Aunque el Joule es la unidad del SI, las empresas eléctricas utilizan el <strong>Watt-hora (o kWh)</strong> porque es más práctica para grandes consumos de potencia en el tiempo.',
                "fb": ['', '', '', ''],
            },
            {
                "q": '¿Qué establece la <em>Ley de Kirchhoff de Tensión (LKT)</em>?',
                "opciones": ['La tensión en un elemento es siempre proporcional a la corriente que lo atraviesa.', 'La tensión de la fuente siempre debe ser mayor a la suma de las tensiones de carga.', 'La suma algebraica de todas las tensiones alrededor de una trayectoria cerrada es cero.', 'La suma de las caídas de tensión es igual al producto de la potencia por la resistencia.'],
                "correcta": 2,
                "pista": 'Recuerde lo que sucede con el <em>nivel de energía de una carga</em> al recorrer un circuito y volver al punto de partida.',
                "ok": 'Esto refleja que el potencial eléctrico en un punto es único; al volver al inicio de un camino cerrado, el <strong>cambio neto de potencial debe ser nulo</strong>.',
                "fb": ['', '', '', ''],
            },
        ],
    },
}
