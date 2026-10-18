# Herramientas frontend para apps construidas por agentes

- **Origen:** video `videos/FNQ8WJa786M-5-herramientas-para-que-tu-app-de-claude-code-no-parezca-de/`
- **Fecha de evaluación:** 2026-10-18

## Las 5 herramientas del video

| # | Herramienta | Qué hace | Equivalente en el lab |
|---|---|---|---|
| 1 | **Taste Skill** | Ayuda a Claude a desarrollar criterio estético (qué significa "premium") | — |
| 2 | **Guías de diseño web** | Auditan la UI contra guías reales de diseño | `code-review` (parcial) |
| 3 | **Awesome Design** | Referencias de sistemas de diseño (tipografía, colores, espaciado, componentes) | — |
| 4 | **Image to Code** | Captura de un diseño → código recreado | — |
| 5 | **Playwright CLI** | Claude abre el navegador, interactúa, hace capturas y verifica lo que construyó | `webapp-testing` (Playwright) |

## Lo que no se sabe

- Ninguna de las 5 herramientas está nombrada con su repositorio. No se pueden instalar sin buscarlas.
- No se muestra ningún ejemplo real en acción.

## El principio valioso: construye, abre, mira

La idea central no es ninguna herramienta específica, sino el **loop de verificación**:

```
el agente construye → abre el navegador → interactúa → captura → comprueba
```

Esto es lo que el lab ya hace parcialmente con `webapp-testing`, pero el video lo eleva a regla: **un agente que no verifica su propio trabajo en el navegador no sabe si lo que construyó funciona**.

## Acción

1. Buscar los repositorios reales de las 5 herramientas (especialmente Taste Skill y Awesome Design).
2. Si se encuentran, evaluar cada una con la grilla de `local-ai/herramientas/`.
3. Mientras tanto, el principio "construye, abre, mira" se agrega a `docs/metodologia.md`.

## Equivalencias ya instaladas

- Playwright CLI ≈ `webapp-testing` (skill local).
- Guías de diseño ≈ `code-review` (skill local, aunque enfocado en código, no en UI).

## Regla del lab

Un agente que construye UI debe verificar su trabajo en el navegador antes de darlo por terminado. Sin capturas ni interacción, no hay evidencia de que funcione.
