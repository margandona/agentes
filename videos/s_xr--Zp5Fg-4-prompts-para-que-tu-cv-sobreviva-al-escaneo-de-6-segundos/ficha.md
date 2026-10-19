# Ficha de video — 4 prompts para que tu CV sobreviva al escaneo de 6 segundos

## Metadatos

- **Título:** 4 Prompts Para Que Tu CV Sobreviva Al Escaneo De 6 Segundos
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/s_xr--Zp5Fg
- **Duración:** 1:04
- **Fecha:** 2026-10-15
- **Relevancia para el lab (1-5):** 3 (prompt engineering, útil como ejemplo de skill basada en prompts)

## Tesis en una frase

> Con cuatro prompts encadenados en un mismo chat, la IA diagnostica por qué te descartan, reescribe tu experiencia con resultados, te da un score ATS y reescribe el CV desde la perspectiva de la pérdida.

## Qué enseña

- [00:00] Alguien le dio su CV a la IA y consiguió seis entrevistas en menos de 24 horas.
- [00:05] **Prompt 1 — Diagnóstico:** subir el CV y la descripción del puesto. "Actúa como el responsable de selección que ya lleva 300 CVs leídos hoy y está agotado. Dale a mi CV un escaneo de 6 segundos y dime con total honestidad en qué momento exacto dejaste de leer y por qué." Deja al descubierto la razón real del descarte.
- [00:30] **Prompt 2 — Reescritura:** en el mismo chat: "Reescribe mi sección de experiencia para que sobreviva a ese escaneo. Cada línea tiene que empezar por un resultado, no por una responsabilidad. Usa la fórmula XYZ de Google y quita todo lo que suene igual que el resto."
- [00:38] **Prompt 3 — Filtro ATS:** "Actúa como el filtro automático que descarta antes de que un humano llegue a verlo. Dame una puntuación de compatibilidad sobre 100 y las palabras clave exactas por las que me están rechazando."
- [00:45] **Prompt 4 — Perspectiva de la pérdida:** "Reescribe mi CV desde la perspectiva de la pérdida para que la empresa sienta que pierde algo si no me contrata."
- [00:55] Los cuatro prompts están en "nuestra bóveda" (captación de leads).

## Procedimiento que propone

1. Subir el CV y la descripción del puesto a un chat de IA.
2. Ejecutar Prompt 1 (diagnóstico de 6 segundos).
3. Ejecutar Prompt 2 (reescribir experiencia con resultados, fórmula XYZ).
4. Ejecutar Prompt 3 (score ATS 0-100 + keywords de rechazo).
5. Ejecutar Prompt 4 (reescribir desde la perspectiva de la pérdida).
6. Todo en el mismo chat para mantener contexto.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| LLM (no especifica cuál) | Analizar y reescribir el CV | Claude, ChatGPT, modelo local |
| Fórmula XYZ de Google | Estructurar bullets de experiencia | — |

## Ideas aprovechables para mí

- Los cuatro prompts son un **pipeline encadenado** en un mismo chat: cada uno consume el resultado del anterior. Es un patrón de skill reutilizable.
- La **fórmula XYZ de Google**: "Accomplished [X] as measured by [Y], by doing [Z]". Es una regla de redacción concreta y verificable.
- El **prompt 1 (diagnóstico sin filtros)** es un patrón de "red team" aplicado a un documento propio. Se puede generalizar a otros artefactos (README, landing, email).
- El **prompt 4 (perspectiva de la pérdida)** es un patrón de copywriting (loss aversion) aplicado a un CV.

## Humo / a verificar

- [ ] "Seis entrevistas en menos de 24 horas" — anécdota sin evidencia, probable marketing.
- [ ] No se menciona qué modelo de IA se usó.
- [ ] La fórmula XYZ se atribuye a Google sin fuente.
- [ ] El video cierra con "nuestra bóveda": captación de tráfico.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `resume-optimization-prompts` | Los 4 prompts encadenados son un procedimiento repetible |
| prompts | `prompts/cv-xyz.md` | La fórmula XYZ como prompt suelto |

## Citas textuales

> "Actúa como el responsable de sección que ya lleva 300 currículums leídos hoy y está agotado." [00:05]

> "Cada línea tiene que empezar por un resultado, no por una responsabilidad. Usa la fórmula X y Z de Google." [00:30]

> "Reescribe mi currículum desde la perspectiva de la pérdida para que la empresa sienta que pierde algo si no me contrata." [00:45]
