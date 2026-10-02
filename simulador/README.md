# Simulador de práctica CT-GenAI

Aplicación de un solo directorio para ensayar el examen ISTQB® Certified Tester – Testing with Generative AI.

Cada intento construye un examen de 40 preguntas y 46 puntos, con el mismo reparto de objetivos de aprendizaje, niveles K y puntos que el examen de muestra (se aprueba con 30 puntos, en 60 minutos, u 75 con el tiempo adicional). Las preguntas son formulaciones originales a partir del programa de estudios y del estilo del examen de muestra: no son los ítems oficiales y no sirven para un examen real.

## Cómo abrirlo

Desde la raíz del repositorio:

```bash
python3 -m http.server 8765
```

y entrar en `http://localhost:8765/simulador/`.

El historial de intentos y el examen en curso se guardan en el navegador (localStorage y sessionStorage).
