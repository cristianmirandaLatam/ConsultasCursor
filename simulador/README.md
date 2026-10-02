# Simulador de práctica CT-GenAI

Aplicación de un solo directorio para ensayar el examen ISTQB® Certified Tester – Testing with Generative AI.

En la pantalla de inicio se elige el modo:

- **Examen real.** 40 preguntas, sin comentarios mientras se responde. La nota y la corrección aparecen al entregar.
- **Examen de prueba.** Al confirmar cada respuesta se muestra enseguida cuál es la correcta y por qué. La respuesta queda fija después de confirmarla.

Los dos modos arman un examen de 40 preguntas y 46 puntos, con el mismo reparto de objetivos de aprendizaje, niveles K y puntos que el examen de muestra (se aprueba con 30 puntos, en 60 minutos, u 75 con el tiempo adicional). Las preguntas son formulaciones originales a partir del programa de estudios y del estilo del examen de muestra: no son los ítems oficiales y no sirven para un examen real.

Los formatos de pregunta siguen los del examen de muestra: una opción correcta entre cuatro, afirmaciones (i-v) con opciones que las combinan («i, ii y iv»), relacionar elementos (1-4 con A-D) y «elija DOS opciones» entre cinco.

Durante el examen, la barra superior tiene dos botones. **Pausar** detiene el tiempo y guarda el examen en el navegador; desde la pantalla de inicio se puede continuar después, con el tiempo que quedaba, o descartarlo. **Terminar** cierra el examen en ese momento: se corrige lo respondido y el intento queda en el historial como incompleto.

Cada intento entregado queda en el historial de la pantalla de inicio con el examen completo. Con «Revisar» se vuelve a abrir: preguntas, respuestas dadas, respuestas correctas y, en cada opción, por qué es correcta o por qué no lo es. En el examen de prueba esa misma justificación aparece al confirmar la respuesta.

## Cómo abrirlo

Desde la raíz del repositorio:

```bash
python3 -m http.server 8765
```

y entrar en `http://localhost:8765/simulador/`.

El historial de intentos y el examen en curso se guardan en el navegador (localStorage y sessionStorage).
