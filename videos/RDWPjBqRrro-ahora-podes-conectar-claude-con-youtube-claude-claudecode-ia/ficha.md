# Ficha de video — Conectar Claude con YouTube

## Metadatos

- **Título:** Ahora podes conectar Claude con youtube
- **Canal:** Lautaro Nievas
- **URL:** https://youtube.com/shorts/RDWPjBqRrro
- **Duración:** 1:09
- **Fecha:** 2026-10-16
- **Relevancia para el lab (1-5):** 5 (valida y describe exactamente el pipeline de este repo)

## Tesis en una frase

> Con tres piezas configuradas una sola vez, Claude puede leer videos de YouTube y convertir lo que aprende en una skill nueva o en un agente especializado en cualquier tema.

## Qué enseña

- [00:00] Se puede enseñar a Claude a mirar videos de YouTube y convertir todo lo que aprende en skills nuevas.
- [00:05] Son **tres piezas** que se configuran una única vez.
- [00:08] **Pieza 1:** una skill que le da a Claude "ojos" para ver videos de YouTube. A partir de ahí puede sacar toda la información de cualquier video: lo que se dice, los tiempos y el contenido completo.
- [00:18] **Pieza 2:** una API key de **Gemini**, gratis, desde Google AI Studio. Gemini está hecho de fábrica para entender videos de YouTube.
- [00:27] **Pieza 3:** una skill que convierte lo que Claude aprende del video en una skill nueva o en un agente especializado.
- [00:31] Con el sistema, le tirás todos los videos que quieras sobre un tema y Claude sale entrenado como experto en ese tema.
- [00:40] Se pueden armar agentes para cualquier rol: community manager, copywriter, especialista.
- [01:02] El mejor agente es el que construís vos, porque lo podés entrenar como se te dé la gana.

## Procedimiento que propone

1. Instalar la skill que da "ojos" a Claude para YouTube (extrae info, timestamps, contenido completo).
2. Obtener una API key gratuita de Gemini desde Google AI Studio.
3. Conectar Gemini con Claude (Gemini entiende videos de YouTube de fábrica).
4. Usar la skill que convierte lo aprendido en una skill nueva o un agente especializado.
5. Tirar varios videos sobre un tema para entrenar al agente.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Skill de "ojos" para YouTube | Extraer info, tiempos, contenido completo de videos | `agent-reach` (yt-dlp) + `video-a-skill` |
| Gemini API (Google AI Studio) | Entender videos de YouTube de fábrica | yt-dlp + Whisper local |
| Skill de conversión video → skill/agente | Convertir lo aprendido en artefacto | `video-a-skill` (ya existe en este lab) |

## Ideas aprovechables para mí

- **Este video describe exactamente el pipeline de este repo.** Las tres piezas son: `agent-reach` (ojos), Gemini (análisis) y `video-a-skill` (conversión a skill/agente). El lab ya tiene el equivalente.
- La idea de usar **Gemini** como backend de análisis de video es valiosa: Gemini entiende videos de YouTube de fábrica, sin descargar ni transcribir. Podría complementar o reemplazar el flujo actual (yt-dlp + Whisper).
- "El mejor agente es el que construís vos" refuerza la metodología del lab: agentes hechos a medida, no genéricos.
- La frase "le tirás todos los videos que quieras sobre un tema y del otro lado sale entrenado" es la visión del lab: acumular skills por tema.

## Humo / a verificar

- [ ] **"Gratis"** — la API de Gemini tiene tier gratuito con límites de rate y de duración de video. Verificar límites actuales.
- [ ] **"Skill que da ojos"** — no se nombra. Puede ser `agent-reach`, `yt-dlp` o un MCP de YouTube. Verificar si Gemini hace algo que yt-dlp no.
- [ ] **"Skill de conversión"** — no se nombra. Puede ser similar a `video-a-skill` de este lab.
- [ ] El video cierra con "comentá YouTube y te paso la guía": captación de leads, no review neutral.
- [ ] No se menciona el costo de tokens de Gemini para videos largos.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| plan | `transcripcion-con-gemini` | Usar Gemini como backend alternativo para analizar videos de YouTube |
| docs | `docs/decisiones.md` | Comparar flujo actual (yt-dlp) vs Gemini |
| skill | — | `video-a-skill` ya cubre la pieza 3 |

## Citas textuales

> "Le tirás todos los videos que quieras sobre un tema y del otro lado Claude sale entrenado como un experto en ese tema en específico." [00:31]

> "El mejor agente es el que construís vos porque lo podés entrenar como se te dé la gana." [01:02]
