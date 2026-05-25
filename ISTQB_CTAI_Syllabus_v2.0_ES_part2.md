## 2 Características de Calidad para Sistemas Basados en IA – 45 minutos

**Palabras clave:** Adaptabilidad funcional, corrección funcional de IA, intervenibilidad, robustez de IA, seguridad (safety), mitigación de riesgos sociales y éticos, transparencia, controlabilidad por el usuario

**Palabras clave específicas de IA:** Ninguna

**Objetivos de Aprendizaje del Capítulo 2:**
2.1 Características de Calidad para Sistemas Basados en IA
- AI-2.1.1 (K2) Clasificar comportamientos de sistemas basados en IA según las características de calidad definidas en ISO/IEC 25059
- AI-2.1.2 (K2) Explicar las consideraciones especiales que surgen cuando se utiliza IA en sistemas relacionados con la seguridad (safety)

2.2 Criterios de Aceptación para Sistemas Basados en IA
- AI-2.2.1 (K2) Dar ejemplos de criterios de aceptación para sistemas basados en IA

### 2.1 Características de Calidad para Sistemas Basados en IA
Esta sección cubre las características de calidad específicas de IA descritas en ISO/IEC 25059, que extiende los modelos tradicionales de calidad de software para abordar aspectos únicos de los sistemas basados en IA. Introduce características nuevas y adaptadas, incluyendo la corrección funcional de IA, la adaptabilidad funcional, la controlabilidad por el usuario, la transparencia, la robustez de IA y la intervenibilidad, junto con la mitigación de riesgos sociales y éticos. También se abordan los principales desafíos de seguridad de la IA, como las especificaciones vagas, el no determinismo, el autoaprendizaje, la explicabilidad limitada y las normativas en evolución, con énfasis en su impacto en las pruebas y la regulación.

#### 2.1.1 Características de Calidad Específicas de IA
ISO/IEC 25059 extiende el modelo de calidad de ISO/IEC 25010 para abordar consideraciones específicas de IA. Esta extensión evalúa los sistemas basados en IA desde dos perspectivas: calidad del producto y calidad en uso. Desde una perspectiva de pruebas, estas características de calidad influyen directamente en cómo se definen los objetivos de prueba, cómo se formulan los criterios de aceptación y cómo se interpretan los resultados de las pruebas para sistemas basados en IA. Las características nuevas y modificadas, en comparación con ISO/IEC 25010, incluyen:

- Corrección funcional de IA (calidad del producto): Los sistemas basados en IA, especialmente aquellos que utilizan ML probabilístico, no pueden garantizar una precisión perfecta. Dado que se espera cierta tasa de error en las salidas de IA, el concepto de corrección funcional se ha ajustado en consecuencia. ISO/IEC 25059 evalúa la corrección funcional considerando tanto las salidas correctas como las incorrectas y definiendo umbrales aceptables para resultados incorrectos, reflejando la variabilidad inherente en las salidas de sistemas basados en IA (véase 3.3).
- Adaptabilidad funcional (calidad del producto): una nueva subcaracterística de la idoneidad funcional. La capacidad del sistema basado en IA para adaptarse de forma autónoma a cambios en su entorno operativo después de ser desplegado.
- Controlabilidad por el usuario (calidad del producto): una nueva subcaracterística de la capacidad de interacción (nótese que la capacidad de interacción es en sí misma un nuevo término que reemplaza a usabilidad en la versión 2023 de ISO/IEC 25010). Una propiedad de un sistema basado en IA tal que un humano u otro agente externo puede intervenir en su funcionamiento de manera oportuna.
- Transparencia (calidad del producto y calidad en uso): una nueva subcaracterística de la capacidad de interacción y una nueva subcaracterística de satisfacción. Se refiere al grado en que se comunica información apropiada sobre el sistema basado en IA a las partes interesadas (véase 6.1.2).
- Robustez de IA (calidad del producto): una nueva subcaracterística de la fiabilidad. Describe la capacidad de un sistema basado en IA para mantener su nivel de corrección funcional de IA independientemente de las circunstancias, como la presencia de datos de entrada sesgados, adversariales o inválidos, interferencias externas, condiciones ambientales adversas y uso indebido por parte del operador.
- Intervenibilidad (calidad del producto): una nueva subcaracterística de la seguridad (security). El grado en que un operador puede intervenir en el funcionamiento de un sistema basado en IA de manera oportuna para prevenir daños o peligros.
- Mitigación de riesgos sociales y éticos (calidad en uso): una nueva subcaracterística de 'Libertad frente al riesgo'. Considera muchas áreas para mitigar riesgos sociales y éticos, incluyendo la rendición de cuentas, la equidad y no discriminación, la responsabilidad profesional, la promoción de valores humanos, la privacidad, la seguridad (safety y security), el control humano de la tecnología, la participación y el desarrollo comunitario, el diseño centrado en el ser humano, el respeto al estado de derecho, el respeto a las normas internacionales de comportamiento, la sostenibilidad ambiental y las prácticas laborales.

#### 2.1.2 IA y Seguridad (Safety)
Los sistemas relacionados con la seguridad tienen el potencial de causar lesiones o daños a personas, propiedades o al medio ambiente. Desarrollar y probar sistemas relacionados con la seguridad que no utilizan IA puede requerir mucho esfuerzo, pero es viable; sin embargo, para los sistemas basados en IA, existen varios desafíos adicionales:

- Especificaciones: En los sistemas tradicionales relacionados con la seguridad, los requisitos se definen para el sistema completo y se refinan hasta que el desarrollador pueda transformarlos en código. Los requisitos para muchos sistemas basados en IA a menudo comienzan con objetivos vagos y luego se proporcionan implícitamente a través de los datos de entrenamiento que codifican patrones, reglas y objetivos, sin formalizar completamente cada detalle de antemano. Esto puede significar que la trazabilidad necesaria desde los requisitos hasta la implementación es inadecuada para los sistemas basados en IA.
- No determinismo: Esta característica de muchos sistemas basados en IA hace que sea inherentemente difícil garantizar el comportamiento preciso de estos sistemas. Incluso los modelos rigurosamente probados pueden exhibir comportamientos inesperados debido a factores como la generación de números aleatorios o ligeras variaciones en los valores de entrada.
- Autoaprendizaje: Las pruebas rigurosas se utilizan para demostrar la integridad de seguridad de un sistema antes de su despliegue. Para los sistemas basados en IA con autoaprendizaje, esto se ve socavado ya que el comportamiento del sistema se aleja progresivamente del comportamiento originalmente probado. Gestionar cómo aprende el modelo y los datos que utiliza puede ayudar a veces a evitar la aparición de nuevos comportamientos problemáticos. Alternativamente, se pueden implementar salvaguardas de seguridad para ayudar a prevenir que el modelo aprenda o tome decisiones que puedan comprometer la seguridad (por ejemplo, un componente de moderación de contenido para filtrar prompts).
- Explicabilidad y Transparencia: Para los sistemas relacionados con la seguridad, es esencial comprender cómo y por qué el sistema toma decisiones. Sin embargo, los procesos de toma de decisiones de los sistemas basados en IA a menudo no son transparentes. Las técnicas de IA explicable, como LIME (Local interpretable model-agnostic explanations), pueden proporcionar información sobre el razonamiento del sistema basado en IA; sin embargo, no están ampliamente disponibles y pueden comprometer el rendimiento del sistema.
- Regulaciones en evolución: El panorama regulatorio para los sistemas basados en IA relacionados con la seguridad está en constante evolución. El uso de IA actualmente no está incluido en las normas internacionales maduras de seguridad funcional, y algunas de estas normas incluso prohíben su uso en dichos sistemas. El EU AI Act [EU AI Act] (véase 1.1.8) clasifica los sistemas de IA utilizados como componentes de seguridad (como en aviación, dispositivos médicos o automoción) como de alto riesgo e impone requisitos estrictos sobre su desarrollo y pruebas.

### 2.2 Criterios de Aceptación para Sistemas Basados en IA
Esta sección describe los criterios de aceptación relacionados con las características de calidad especificadas en la norma ISO/IEC 25059, así como con la seguridad (safety). Para los sistemas basados en IA, los criterios de aceptación a menudo necesitan ser estadísticos, probabilísticos o basados en umbrales en lugar de binarios, lo que introduce desafíos adicionales en las pruebas.

#### 2.2.1 Criterios de Aceptación para Sistemas Basados en IA
Al evaluar la calidad de un sistema basado en IA, es esencial considerar tanto las características de calidad funcionales como las no funcionales. Esto ayuda a confirmar que el sistema basado en IA funciona según lo previsto y satisface requisitos de calidad más amplios. Las normas ISO/IEC 25010 e ISO/IEC 25059 proporcionan un marco integral para definir la calidad del software. En esta sección, el enfoque se centra en los criterios de aceptación asociados con las características de calidad específicas de IA (es decir, las definidas en ISO/IEC 25059) y la seguridad (véase 2.1.2).

La siguiente tabla enumera ejemplos de criterios de aceptación para la seguridad y cada una de las características de calidad definidas en la norma ISO/IEC 25059.

| Característica | Ejemplos de Criterios de Aceptación |
|---|---|
| Corrección funcional de IA (véase 3.3) | Precisión del 95% para un sistema de reconocimiento de imágenes. Recall del 90% para un sistema de predicción de defectos. |
| Adaptabilidad funcional | Un máximo de 20 segundos para que el sistema de gestión del motor se adapte cuando cruza un umbral de altitud especificado. Un servicio de streaming de vídeo debe ajustar su página de inicio para recomendar al menos un 40% de documentales después de que un usuario vea tres documentales completos en una sola sesión. |
| Controlabilidad por el usuario | Un supervisor puede tomar el control de un dron autónomo en 0,5 segundos cuando este envía una señal de socorro debido a la pérdida de su ubicación GPS. El sistema de control agrícola notifica al agricultor cuando el rendimiento visual del sensor se degrada en más del 30%, permitiendo una anulación manual inmediata; se desactiva completamente si la degradación supera el 50% sin respuesta del usuario. |
| Transparencia | Se proporciona información suficiente sobre el modelo de ML de terceros y la procedencia de sus datos de entrenamiento para cumplir con los requisitos de la norma empresarial correspondiente. El panel de operaciones del sistema y la API deben proporcionar un endpoint que devuelva el identificador de versión único del modelo de predicción actualmente desplegado y un enlace a su documentación correspondiente. |
| Robustez de IA | El tiempo de respuesta para las predicciones del sistema de alertas de penetración de seguridad basado en IA se mantiene por debajo de 1 segundo cuando el acceso a la base de datos central de vulnerabilidades se interrumpe durante 30 segundos. El dispositivo de IA en el borde (edge) debe hacer una transición automática a un modo de inferencia de menor fidelidad y menor consumo de energía (en lugar de fallar) cuando su temperatura interna de operación excede los 85°C durante un período continuo de 10 segundos. |
| Intervenibilidad | Si un robot traspasa su zona de seguridad, la línea de producción puede ser detenida en 0,5 segundos después de que se inicie el apagado. Para prevenir posibles apagones, el sistema de gestión de la red eléctrica debe proporcionar una ventana de confirmación de 30 segundos, durante la cual un ingeniero puede vetar cualquier acción propuesta por la IA clasificada como 'crítica' antes de que se ejecute automáticamente. |
| Mitigación de riesgos sociales y éticos | El sistema automatizado de sentencias carcelarias no discrimina entre grupos raciales según la métrica de equidad especificada. El chatbot debe superar una evaluación interna de "red teaming" con una puntuación del 95% o superior, demostrando su rechazo a generar contenido que promueva la violencia, la autolesión o el discurso de odio. |
| Seguridad (Safety) | Los componentes no basados en IA del sistema de control de dirección basado en IA cumplen con ISO 26262-6 en el nivel ASIL C. El 100% de las relaciones entre entradas y salidas del modelo de ML en el sistema de control de la central nuclear pueden ser mapeadas con una precisión promedio no inferior al 99,9% mediante una herramienta de explicabilidad. Las señales de control que exceden los límites de seguridad especificados en más del 10% son analizadas y reguladas en 0,15 segundos después de ser detectadas por el subsistema de monitorización de seguridad. |

---

## 3 Machine Learning – 375 minutos

**Palabras clave:** Cobertura de neuronas por k-multisección, criterios de rendimiento funcional de ML, métrica de rendimiento funcional de ML, modelo de ML, cobertura de límites de neuronas, cobertura de neuronas, perceptrón

**Palabras clave específicas de IA:** Asociación, clasificación, clustering, preparación de datos, machine learning, algoritmo de ML, framework de desarrollo de ML, flujo de trabajo de ML, modelo preentrenado, regresión de ML, aprendizaje por refuerzo, aprendizaje supervisado, aprendizaje no supervisado

**Objetivos de Aprendizaje del Capítulo 3:**
3.1 Introducción al Machine Learning
- AI-3.1.1 (K2) Distinguir entre las diferentes formas de ML
- AI-3.1.2 (K2) Resumir el flujo de trabajo utilizado para crear un sistema de ML
- HO-3.1.3 (H2) Crear un modelo de ML
- AI-3.1.4 (K2) Resumir el uso de modelos preentrenados, el ajuste fino (fine-tuning) y la generación aumentada por recuperación (RAG)

3.2 Datos para Machine Learning
- AI-3.2.1 (K2) Explicar las actividades relacionadas con la preparación de datos
- HO-3.2.2 (H2) Realizar la preparación de datos para apoyar la creación de un modelo de ML
- AI-3.2.3 (K2) Contrastar el uso de conjuntos de datos de entrenamiento, validación y prueba en el desarrollo de un modelo de ML

3.3 Métricas de Rendimiento Funcional de ML para Clasificación
- AI-3.3.1 (K3) Calcular métricas comunes de rendimiento funcional de ML a partir de un conjunto dado de datos de matriz de confusión
- HO-3.3.2 (H2) Evaluar un modelo de ML utilizando métricas de rendimiento funcional de ML seleccionadas
- HO-3.3.3 (H2) Mostrar el impacto de diferentes combinaciones de modelos de ML y conjuntos de datos en el entrenamiento y comportamiento de los modelos

3.4 Redes Neuronales
- AI-3.4.1 (K2) Explicar la estructura y el funcionamiento de una red neuronal profunda
- HO-3.4.2 (H1) Experimentar la implementación de un perceptrón
- AI-3.4.3 (K2) Describir las diferentes medidas de cobertura para redes neuronales

### 3.1 Introducción al Machine Learning
Esta sección presenta las principales categorías de algoritmos de ML: aprendizaje supervisado, no supervisado y por refuerzo, distinguiendo sus respectivos tipos de problemas y aplicaciones típicas. Describe el flujo de trabajo estándar para el desarrollo de modelos de ML, desde la definición de objetivos y la preparación de datos hasta el entrenamiento, la evaluación y el despliegue de modelos, con atención a la iteración y la integración del sistema. También se cubren aspectos prácticos como la creación práctica de modelos, el uso de modelos preentrenados, el ajuste fino (fine-tuning) y la generación aumentada por recuperación (RAG), destacando enfoques para adaptar y mejorar eficientemente los modelos de IA para nuevas tareas mientras se gestionan las limitaciones heredadas.

Comprender este flujo de trabajo es esencial para los testers, ya que diferentes actividades de prueba se aplican en diferentes etapas, y las fallas a menudo se originan en pasos anteriores como la preparación de datos o la selección del modelo.

#### 3.1.1 Diferentes Formas de Machine Learning
Los algoritmos de ML se clasifican en aprendizaje supervisado, aprendizaje no supervisado y aprendizaje por refuerzo.

En el aprendizaje supervisado, los algoritmos entrenan modelos utilizando datos etiquetados, donde cada conjunto de entradas tiene una etiqueta de salida correspondiente (por ejemplo, imágenes etiquetadas como "perro" o "gato"). El modelo aprende a mapear entradas a salidas identificando patrones en los datos de entrenamiento. El aprendizaje supervisado se divide típicamente en:
- Clasificación: Consiste en asignar entradas a clases predefinidas, como clasificar correos electrónicos como spam o no spam, o el reconocimiento de imágenes.
- Regresión de ML: Consiste en predecir valores numéricos continuos, como estimar la edad de una persona basándose en datos de estilo de vida o pronosticar precios de acciones.

Nótese que el término regresión de ML, cuando se usa en el contexto de ML, difiere de su uso en otros syllabi de ISTQB®, donde regresión describe el problema de que las modificaciones de software causen defectos relacionados con cambios.

En el aprendizaje no supervisado, el algoritmo entrena modelos utilizando datos no etiquetados, infiriendo patrones o estructuras sin etiquetas de salida explícitas. El modelo agrupa entradas similares basándose en características compartidas. El aprendizaje no supervisado se categoriza típicamente en:
- Clustering: Consiste en agrupar puntos de datos basándose en similitudes, como segmentar clientes en diferentes grupos para marketing dirigido.
- Asociación: Consiste en identificar relaciones o dependencias entre atributos de datos, como encontrar patrones en el comportamiento de compra de clientes para recomendar productos.

En el aprendizaje por refuerzo, el sistema basado en IA (un "agente inteligente") aprende interactuando con su entorno. El agente recibe retroalimentación positiva (recompensas) o retroalimentación negativa (penalizaciones) basada en el resultado de sus acciones, lo que le permite aprender de la experiencia en lugar de hacerlo a partir de un conjunto de datos. Los desafíos en el aprendizaje por refuerzo incluyen la configuración del entorno, el diseño de la función de recompensa y la selección de la mejor estrategia para alcanzar el objetivo deseado. Las aplicaciones incluyen robótica, vehículos autónomos y sistemas adaptativos como chatbots.

Cada enfoque de ML aborda diferentes tipos de problemas, y la elección depende de la naturaleza de los datos disponibles y de la tarea específica en cuestión.

#### 3.1.2 Flujo de Trabajo de Machine Learning
Las actividades en el flujo de trabajo de ML, mostradas en la Figura 1, son:

**Comprender los Objetivos:** El propósito del modelo de ML es comprendido y acordado por las partes interesadas para verificar la alineación con las prioridades del negocio. Se definen los criterios de aceptación (incluyendo las métricas de rendimiento funcional de ML – véase 3.3) para el modelo desarrollado.

**Seleccionar un Framework:** Se selecciona un framework de desarrollo de ML adecuado (véase 1.1.7 para detalles sobre la funcionalidad proporcionada) basándose en los objetivos, los criterios de aceptación (véase 2.2) y las prioridades del negocio.

**Seleccionar y Construir el Algoritmo:** Se selecciona un algoritmo de ML basándose en diversos factores, incluyendo los objetivos, los criterios de aceptación y los datos disponibles (véase 3.2). El algoritmo puede ser codificado manualmente, pero a menudo se obtiene de una biblioteca de software. El algoritmo se compila posteriormente, si es necesario.

**Preparar y Probar los Datos:** La preparación de datos (véase 3.2) comprende la adquisición de datos, el preprocesamiento de datos y la ingeniería de características. El análisis exploratorio de datos (EDA) puede realizarse junto con estas actividades. Los datos utilizados por el algoritmo y el modelo se basan en los objetivos y son utilizados por todas las actividades en el recuadro de 'generación y prueba del modelo' mostrado en la Figura 1. Los datos utilizados para entrenar, evaluar, ajustar y probar el modelo deben ser representativos de los datos que serán utilizados por el modelo en operación. Se realizan pruebas de los datos y de cualquier paso automatizado de preparación de datos (véase Capítulo 5).

**Entrenar el Modelo:** El algoritmo de ML seleccionado utiliza datos de entrenamiento para entrenar el modelo. Los parámetros que definen la estructura del modelo (por ejemplo, el número de capas de una red neuronal o la profundidad de un árbol de decisión) se pasan al algoritmo. Estos parámetros se conocen como hiperparámetros del modelo. Los parámetros que controlan el entrenamiento (por ejemplo, el número de iteraciones a utilizar cuando se entrena una red neuronal) también se pasan al algoritmo. Estos parámetros se conocen como hiperparámetros del algoritmo.

**Evaluar el Modelo:** El modelo se evalúa contra las métricas de rendimiento funcional de ML acordadas (véase 3.3), utilizando el conjunto de datos de validación, y los resultados se utilizan para mejorar el modelo en la actividad de 'ajustar el modelo'. En la práctica, típicamente se crean y entrenan varios modelos utilizando diferentes algoritmos (por ejemplo, random forests, SVM y redes neuronales) y varios conjuntos de datos de entrenamiento, y se elige la mejor combinación basándose en los resultados de la evaluación.

**Ajustar el Modelo:** Los resultados de la evaluación se utilizan para ajustar los hiperparámetros del modelo y los hiperparámetros del algoritmo. El modelo se vuelve a entrenar con estos ajustes para mejorar su rendimiento funcional de ML. Las tres actividades de entrenamiento, evaluación y ajuste comprenden la 'generación del modelo', como se muestra en la Figura 1.

**Probar el Modelo:** Una vez que se ha generado un modelo aceptable mediante las actividades de 'generación del modelo', se prueba utilizando un conjunto de datos de prueba independiente para verificar que se cumplen los criterios de rendimiento funcional de ML acordados. Los resultados de las pruebas también se comparan con los de la evaluación. Si el rendimiento del modelo con datos de prueba independientes es significativamente inferior al obtenido durante la evaluación, puede ser necesario regresar a las actividades de 'generación del modelo', o incluso a la actividad de 'preparar y probar los datos' para entrenar un nuevo modelo. Además de las pruebas de rendimiento funcional de ML, también pueden realizarse pruebas no funcionales, como el tiempo para proporcionar una predicción. Típicamente, las pruebas en esta actividad son realizadas por ingenieros o científicos de datos; sin embargo, los testers con suficiente conocimiento del dominio y acceso a los recursos relevantes también pueden realizar estas pruebas.

**Desplegar el Modelo:** Una vez completada la 'generación y prueba del modelo', el modelo ajustado se reingeniería típicamente para su despliegue junto con su pipeline de datos. Esto generalmente se logra a través del framework de desarrollo de ML. Las plataformas objetivo pueden incluir sistemas embebidos y la nube, donde el modelo puede ser accedido a través de una API web. El modelo desplegado reingenierizado se prueba para verificar que aún cumple con sus criterios de aceptación.

**Usar el Modelo:** Una vez desplegado, el modelo se integra típicamente en un sistema operativo basado en IA más amplio. Los modelos pueden realizar predicciones por lotes programadas a intervalos de tiempo establecidos o ejecutarse en tiempo real bajo demanda.

**Monitorizar y Ajustar el Modelo:** Mientras el modelo está en uso, su situación puede evolucionar y el modelo puede desviarse de su rendimiento previsto (véase 6.1.7). Para verificar que cualquier desviación sea identificada y gestionada, el modelo operativo se evalúa regularmente contra sus criterios de aceptación. Puede considerarse necesario crear un nuevo modelo mediante reentrenamiento con nuevos datos, reentrenamiento con nuevos hiperparámetros, o ambos. El modelo más reciente puede entonces compararse con el modelo existente utilizando una forma de pruebas A/B (véase 6.1.9).

El flujo de trabajo de ML mostrado en la Figura 1 es una secuencia lógica; sin embargo, en la práctica, el flujo de trabajo se aplica de forma iterativa, con pasos que se repiten. Los pasos mostrados en la Figura 1 no incluyen la integración del modelo de ML con las partes no basadas en ML del sistema general. Típicamente, los modelos de ML no pueden desplegarse de forma aislada y deben integrarse con componentes no basados en ML (por ejemplo, en aplicaciones de visión, se utiliza un pipeline de datos para limpiar y modificar los datos antes de enviarlos al modelo de ML). Cuando el modelo es parte de un sistema mayor, debe integrarse en este sistema antes del despliegue. En este caso, pueden realizarse pruebas a nivel de integración, sistema y aceptación.

*Figura 1: Flujo de Trabajo de ML*

#### 3.1.3 Ejercicio Práctico: Crear un Modelo de Machine Learning
Seleccionar, entrenar y probar un modelo de clasificación utilizando aprendizaje supervisado. Explicar la diferencia entre evaluación/ajuste y pruebas comparando la precisión obtenida con los conjuntos de datos de validación y prueba.

#### 3.1.4 Modelos Preentrenados, Ajuste Fino (Fine-Tuning) y Generación Aumentada por Recuperación (RAG)
Entrenar un nuevo modelo de IA desde cero es costoso y requiere mucho tiempo. Para abordar esto, una solución común es el ajuste fino (fine-tuning), que consiste en tomar una red neuronal preentrenada y adaptarla para realizar una tarea nueva y diferente. Uno de los beneficios clave es que requiere muchos menos datos de entrenamiento (y esfuerzo de entrenamiento) en comparación con la construcción de un modelo desde cero.

El modelo preentrenado se ajusta finamente realizando entrenamiento adicional con datos específicos de la nueva tarea. El ajuste puede aplicarse a toda la red neuronal, solo a capas específicas (típicamente cerca del extremo de salida de la red neuronal) o a capas adicionales. Después del entrenamiento, se evalúa el rendimiento funcional de ML del modelo y, basándose en estos resultados, puede realizarse un ajuste fino adicional hasta que el modelo cumpla con los criterios de aceptación necesarios.

El éxito del ajuste fino depende de la similitud entre la tarea original y la nueva. Las diferencias pequeñas pueden conducir a un ajuste fino muy efectivo. Por ejemplo, adaptar un clasificador de imágenes de razas de gatos para identificar razas de perros probablemente funcionará bien. Sin embargo, adaptarlo para acentos hablados es menos efectivo debido a la mayor diferencia. De manera similar, el ajuste fino de un LLM para el análisis de valores límite definido por ISTQB requiere un cambio pequeño para el LLM y es fácilmente alcanzable con buenos datos de entrenamiento.

Una alternativa al ajuste fino es la Generación Aumentada por Recuperación (RAG), que consiste en proporcionar fuentes de datos al LLM que son específicas para la tarea requerida. Estas fuentes de datos se transforman en un formato consultable que permite compararlas con el tema del prompt. Una vez que se identifican documentos relevantes, estos se incorporan en un prompt mejorado que se pasa al LLM. Como ahora se proporciona más información pertinente al LLM, su respuesta correspondiente probablemente será más precisa. Con RAG, no se realiza ningún cambio en el modelo preentrenado.

Un modelo preentrenado puede utilizar RAG, ajuste fino, o ambos conjuntamente para mejorar el rendimiento. Típicamente, cualquier sesgo o vulnerabilidad del modelo preentrenado se trasladará al nuevo modelo, por lo que es necesario realizar pruebas para confirmar que funciona de manera fiable y equitativa en la nueva tarea.

### 3.2 Datos para Machine Learning
La preparación de datos es reconocida como una de las actividades más cruciales e intensivas en recursos del flujo de trabajo de ML. Si los datos operativos difieren significativamente de los datos de entrenamiento, las suposiciones sobre el rendimiento funcional de ML y la seguridad pueden dejar de ser válidas. La preparación de datos típicamente consume una proporción significativamente mayor del esfuerzo total en comparación con otras etapas, como la selección y construcción del modelo. La preparación de datos está intrínsecamente vinculada al pipeline de datos, que procesa los datos en bruto y los transforma en un formato utilizable tanto para el entrenamiento como para la predicción por parte de los modelos de ML.

#### 3.2.1 Actividades en la Preparación de Datos
La preparación de datos apoya el logro de la calidad e idoneidad de los datos para el entrenamiento del modelo. Involucra varias actividades clave:

- Adquisición de datos:
  - Identificación de tipos de datos relevantes (por ejemplo, numéricos, categóricos, imágenes, texto).
  - Recopilación de datos de diversas fuentes, como bases de datos, APIs o sensores en tiempo real.
  - Etiquetado de datos para tareas de aprendizaje supervisado, verificando la precisión y consistencia.
  Los datos adquiridos pueden adoptar diversas formas (por ejemplo, numéricos, categóricos, imágenes, tabulares, texto, series temporales, sensores, geoespaciales, vídeo y audio).

- Preprocesamiento de datos:
  - Limpieza de datos, incluyendo: eliminación de defectos, duplicados y valores atípicos para verificar la precisión y consistencia de los datos; imputación de valores faltantes utilizando técnicas como la media, la mediana o la moda para mantener la completitud de los datos; anonimización o eliminación de información personal para proteger la privacidad y cumplir con las regulaciones.
  - Transformación de formatos de datos, escalado y normalización para lograr consistencia.
  - Aumento de datos para incrementar el tamaño de la muestra, incorporación de ejemplos adversariales para mejorar la robustez contra ataques adversariales y generación de datos sintéticos.
  - Muestreo de subconjuntos para reducir los tiempos de entrenamiento y los costos computacionales.

- Ingeniería de características:
  - Selección de características relevantes basándose en su contribución al rendimiento del modelo de ML.
  - Extracción de un subconjunto de características informativas y no redundantes a partir de las características existentes para reducir los tiempos de entrenamiento y los costos computacionales.

En paralelo a estas actividades de preparación de datos, también se lleva a cabo típicamente un análisis exploratorio de datos (EDA) para proporcionar información sobre los datos. Esto incluye:
- descubrir tendencias, patrones y anomalías en los datos;
- visualizar datos mediante gráficos y diagramas para una mejor comprensión.

La preparación de datos de entrenamiento es típicamente un proceso iterativo, a menudo realizado manualmente, y las actividades individuales de preparación de datos pueden reordenarse u omitirse según los requisitos específicos del proyecto. Los datos operativos deben coincidir con las características de los datos de entrenamiento (por ejemplo, distribuciones de datos y rangos de características) para que el modelo funcione como se espera en producción. Sin embargo, los pasos de preparación en sí pueden ajustarse para eficiencia y escalabilidad en producción.

#### 3.2.2 Ejercicio Práctico: Preparación de Datos como Apoyo a la Creación de un Modelo de Machine Learning
Para un conjunto de datos dado, realizar los pasos de preparación de datos aplicables como se describe en la Sección 3.2.1 para producir un conjunto de datos que se utilizará para crear un modelo de clasificación mediante aprendizaje supervisado.

#### 3.2.3 Conjuntos de Datos de Entrenamiento, Validación y Prueba
Lógicamente, se requieren tres conjuntos de datos equivalentes (por ejemplo, seleccionados aleatoriamente de un único conjunto de datos representativo) para desarrollar un modelo de ML:
- Un conjunto de datos de entrenamiento se utiliza para entrenar el modelo.
- Un conjunto de datos de validación se utiliza para evaluar y posteriormente ajustar el modelo.
- Un conjunto de datos de prueba, también conocido como conjunto de datos de reserva (holdout), se utiliza para probar el modelo ajustado.

Si hay abundancia de datos adecuados, la cantidad de datos utilizada en el flujo de trabajo de ML para entrenamiento, evaluación y pruebas típicamente depende de los siguientes factores:
- La complejidad esperada del modelo.
- El algoritmo utilizado para entrenar el modelo.
- La disponibilidad de recursos, como RAM, espacio en disco, potencia de cómputo, ancho de banda de red y el tiempo disponible.
- La confianza deseada en el modelo resultante.

Cuando los datos son limitados, una división en tres partes (entrenamiento, validación y prueba) puede resultar en datos insuficientes para un entrenamiento efectivo del modelo, aumentando así el riesgo de subajuste (underfitting). Para abordar esto, una estrategia común es reservar un pequeño conjunto de prueba final de reserva (hold-out) si es factible. Los datos restantes (el conjunto combinado de entrenamiento y validación) se utilizan entonces para técnicas como la validación cruzada de k pliegues (k-fold cross-validation) (donde k es un entero especificado por el usuario, comúnmente 5 o 10).

En la validación cruzada de k pliegues, estos datos se dividen en k 'pliegues' (folds). Para cada pliegue, el modelo se entrena con k-1 pliegues y se valida con el pliegue reservado. Este proceso se repite k veces, con cada pliegue sirviendo como conjunto de validación una vez. Esto permite un ajuste robusto de hiperparámetros y una estimación del rendimiento funcional de ML. Los datos se asignan típicamente de forma aleatoria a los pliegues, a menudo utilizando muestreo estratificado para hacer que cada pliegue sea representativo, especialmente con datos desequilibrados o conjuntos de datos pequeños.

Las métricas de rendimiento (por ejemplo, accuracy, F1-score – véase 3.3.1) de la validación de cada pliegue se promedian entonces para proporcionar una estimación más fiable de la capacidad de generalización del modelo. Después de identificar los hiperparámetros óptimos mediante la validación cruzada, típicamente se entrena un modelo final con todo el conjunto de entrenamiento y validación (todos los datos excepto el conjunto de prueba de reserva) utilizando estos hiperparámetros. Este modelo final se evalúa entonces una vez con el conjunto de prueba de reserva para una evaluación final e imparcial del rendimiento. Si un conjunto de prueba de reserva no es factible debido a una escasez extrema de datos, el rendimiento promedio de la validación cruzada está sesgado de manera optimista y no puede servir como una estimación imparcial.

Otros métodos de remuestreo para datos limitados incluyen la validación cruzada dejando uno fuera (leave-one-out cross-validation, un caso especial de k-fold donde k es igual al número de muestras) y técnicas de bootstrap.

### 3.3 Métricas de Rendimiento Funcional de ML para Clasificación
En tareas de clasificación (véase 3.1.1), se puede utilizar una matriz de confusión para evaluar las predicciones de un modelo, categorizándolas como verdaderos positivos, verdaderos negativos, falsos positivos o falsos negativos. De esta se derivan métricas clave como accuracy, precision, recall y F1-score. Estas métricas miden la calidad de la clasificación, destacando las fortalezas y debilidades del modelo de ML. Esta sección explora el cálculo y la interpretación de estas métricas para evaluar el rendimiento funcional de ML.

#### 3.3.1 Cálculo de Métricas de Rendimiento Funcional de Machine Learning
En un problema de clasificación, un modelo rara vez predecirá los resultados correctamente todo el tiempo, en parte debido a la naturaleza probabilística de los modelos de ML y al ruido en los datos. Para cualquier problema de este tipo, se puede crear una matriz de confusión con las siguientes posibilidades:

|  | Positivo Real | Negativo Real |
|---|---|---|
| Predicción Positiva | Verdadero Positivo (TP) | Falso Positivo (FP) |
| Predicción Negativa | Falso Negativo (FN) | Verdadero Negativo (TN) |

*Figura 2: Matriz de Confusión*

Nótese que la matriz de confusión mostrada en la Figura 2 puede presentarse de forma diferente (por ejemplo, con predicción y real intercambiados), pero siempre proporcionará valores para las cuatro situaciones posibles de verdadero positivo (TP), verdadero negativo (TN), falso positivo (FP) y falso negativo (FN).

Basándose en la matriz de confusión, se definen las siguientes métricas:
- Accuracy = (TP + TN) / (TP + TN + FP + FN) * 100%
  Accuracy mide el porcentaje de todas las clasificaciones correctas.
- Precision = TP / (TP + FP) * 100%
  Precision mide la proporción de positivos que fueron predichos correctamente. Es una medida de cuán seguro se puede estar acerca de las predicciones positivas.
- Recall = TP / (TP + FN) * 100%
  Recall (también conocido como sensibilidad) mide la proporción de positivos reales que se predicen correctamente. Es una medida de cuán seguro se puede estar de que no se omitirá ningún positivo.
- F1-score = 2 * (Precision * Recall) / (Precision + Recall)
  El F1-score se calcula como la media armónica de precision y recall, con valores que van de 0 a 100. Una puntuación cercana a 100 significa que el modelo logra tanto alta precision como alto recall, indicando que los errores de clasificación (falsos positivos y falsos negativos) tienen un impacto mínimo. Por el contrario, un F1-score bajo indica que el modelo tiene dificultades para identificar positivos con precisión, ya sea omitiendo casos verdaderos o generando muchas falsas alarmas.

#### 3.3.2 Ejercicio Práctico: Evaluar un Modelo de Machine Learning utilizando Métricas de Rendimiento Funcional de ML Seleccionadas
Utilizando el modelo de clasificación entrenado en el ejercicio anterior, calcular y mostrar los valores de accuracy, precision, recall y F1-score. Cuando sea aplicable, utilizar las funciones de biblioteca proporcionadas por su framework de desarrollo de ML para realizar los cálculos.

#### 3.3.3 Ejercicio Práctico: Mostrar el Impacto de Diferentes Combinaciones de Modelos de Machine Learning y Conjuntos de Datos
Siguiendo el ejercicio anterior, utilizar diferentes combinaciones de modelos de ML y conjuntos de datos para observar su efecto en el entrenamiento del modelo de ML, así como en el comportamiento final del modelo. Observar los tiempos de entrenamiento y las métricas de rendimiento funcional de ML.

### 3.4 Redes Neuronales
Las redes neuronales artificiales fueron diseñadas inicialmente para imitar el funcionamiento del cerebro humano, que puede considerarse como una red de neuronas biológicas interconectadas.

El perceptrón de capa única es uno de los primeros ejemplos de implementación de una red neuronal artificial, compuesto por una sola capa. Puede utilizarse para el aprendizaje supervisado de clasificadores binarios para problemas linealmente separables, que determinan si una entrada pertenece a una clase específica o no. Por ejemplo, un perceptrón puede distinguir entre correos electrónicos que son spam y los que no lo son, aprendiendo a separar las características de las dos categorías con una línea recta en el espacio de entrada.

La mayoría de las redes neuronales actuales se consideran redes neuronales profundas (deep neural networks) porque están compuestas por varias capas. Las redes completamente conectadas pueden considerarse como perceptrones multicapa (véase la Figura 3).

*Figura 3: Estructura de una red neuronal profunda*

#### 3.4.1 Estructura y Funcionamiento de una Red Neuronal Profunda
Una red neuronal profunda se describe típicamente como compuesta por tres tipos principales de capas. La capa de entrada recibe las entradas, por ejemplo, valores de píxeles de una cámara. La capa de salida proporciona resultados al mundo exterior. Esto podría ser, por ejemplo, un valor que indica la probabilidad de que la imagen de entrada sea de un gato. Entre las capas de entrada y salida se encuentran las capas ocultas compuestas por neuronas artificiales, también conocidas como nodos. En muchas arquitecturas comunes, como las redes completamente conectadas, las neuronas de una capa están conectadas a cada una de las neuronas de la capa siguiente, y puede haber diferentes números de neuronas en cada capa sucesiva.

Las neuronas realizan cálculos y transmiten información a través de la red desde las neuronas de entrada hasta las neuronas de salida, transformando gradualmente los datos de entrada en representaciones cada vez más abstractas hasta alcanzar la salida.

El cálculo realizado por cada neurona (después de las de la capa de entrada) genera lo que se conoce como el valor de activación. Este valor se calcula primero computando una suma ponderada de los valores de activación de todas las neuronas conectadas en la capa anterior, donde cada conexión tiene su propio peso independiente, y sumando el sesgo (bias) individual de la neurona. Esta suma se pasa luego a través de una fórmula no lineal llamada función de activación. Nótese que este sesgo (bias) no está relacionado con el sesgo considerado en 5.1.2. El uso de diferentes funciones de activación produce diferentes valores de activación.

*Figura 4: Cálculo realizado por cada neurona*

Los pesos que conectan las neuronas y el valor de sesgo (bias) de cada neurona se inicializan típicamente con valores aleatorios pequeños (los sesgos a veces con cero) al inicio del entrenamiento. Los datos de entrenamiento se pasan a través de la red, con cada neurona ejecutando la función de activación, para generar una salida en última instancia. La salida generada se compara entonces con el resultado correcto conocido. El error (o pérdida) resultante, que cuantifica esta diferencia, se retroalimenta a través de la red para ajustar los valores de los pesos y sesgos, minimizando así esta diferencia. A medida que más datos de entrenamiento se alimentan a través de la red (cada pasada a través del conjunto de datos de entrenamiento se denomina una época o epoch), los valores de los pesos y sesgos se ajustan gradualmente mientras la red aprende. Después de cierto tiempo, idealmente, la salida producida se considera suficientemente buena para finalizar el entrenamiento.

#### 3.4.2 Ejercicio Práctico: Experimentar la Implementación de un Perceptrón
Los estudiantes serán guiados a través de un ejercicio que demuestra cómo un Perceptrón aprende una función simple, como una función AND. El ejercicio debe cubrir cómo un Perceptrón aprende modificando sus pesos y valores de sesgo (bias) a lo largo de múltiples épocas (epochs) hasta que el error se minimiza a cero. Pueden utilizarse diversos mecanismos (por ejemplo, hoja de cálculo, simulación) para esta actividad.

#### 3.4.3 Medidas de Cobertura para Redes Neuronales
Las métricas de cobertura estructural de redes neuronales han surgido para evaluar cuán exhaustivamente las entradas de prueba ejercitan los mecanismos internos de un modelo. Como las redes neuronales no siguen caminos explícitamente codificados, sino que su comportamiento está dictado por los pesos aprendidos, los valores de sesgo (bias) y las activaciones, esto crea la necesidad de medidas de cobertura especializadas para evaluar en qué medida diferentes partes de la red han sido activadas bajo condiciones de prueba.

Los enfoques típicos incluyen [COV_REF]:
- Cobertura de Neuronas (Neuron Coverage): Mide la proporción de neuronas en la red cuya salida excede un umbral especificado durante las pruebas.
- Cobertura de Neuronas por k-Multisección (k-Multisection Neuron Coverage, kMNC): El rango de salida posible de cada neurona se divide en k secciones. kMNC es la proporción de estas secciones activadas durante las pruebas.
- Cobertura de Límites de Neuronas (Neuron Boundary Coverage, NBC): Mide la proporción de neuronas en la red cuya salida excede el máximo alcanzado durante el entrenamiento o es inferior al mínimo alcanzado durante el entrenamiento en las pruebas.

Estas métricas de cobertura pueden ser útiles en las pruebas de IA, principalmente al revelar áreas del modelo que permanecen sin probar, las cuales pueden potencialmente ocultar defectos o comportamientos no aprendidos. Por ejemplo, si ciertas neuronas o capas nunca se activan durante las pruebas, el rendimiento del modelo en las fronteras de decisión relacionadas podría ser cuestionable. Tales perspectivas ayudan a los testers a diseñar entradas de prueba o condiciones de prueba adicionales para ejercitar partes poco exploradas de la red. En la actualidad, las herramientas comerciales que soportan estas medidas de cobertura específicas son limitadas.

Sin embargo, la cobertura estructural por sí sola no garantiza que una red neuronal generalice bien o maneje variaciones del mundo real. Las redes neuronales pueden aprender correlaciones espurias, lo que lleva a activaciones correctas por razones incorrectas. En consecuencia, los testers también deben utilizar otras técnicas de prueba, como las pruebas adversariales y las pruebas metamórficas, como se describe en los capítulos 5, 6 y 7.
