# Plan: transcripción y análisis de videos con Gemini

- **Origen:** video `videos/RDWPjBqRrro-ahora-podes-conectar-claude-con-youtube-claude-claudecode-ia/` [00:08] y [00:27]
- **Objetivo:** usar la API de Gemini como backend alternativo para analizar videos de YouTube, sin descargar ni transcribir
- **No-objetivo:** reemplazar el flujo actual (yt-dlp + Whisper) de golpe
- **Riesgo principal:** depender de un servicio en la nube para una tarea que hoy es local y gratis

## Precondiciones

- [ ] API key de Gemini obtenida en Google AI Studio (gratis)
- [ ] `agent-reach` instalado (ya lo está)
- [ ] Un video de prueba para comparar resultados

## Por qué considerarlo

El video `RDWPjBqRrro` propone tres piezas:

1. Skill que da "ojos" a Claude para YouTube (extrae info, timestamps, contenido).
2. API key de Gemini (gratis) — Gemini entiende videos de YouTube de fábrica.
3. Skill que convierte lo aprendido en una skill nueva o un agente.

Las piezas 1 y 3 ya existen en este lab (`agent-reach` + `video-a-skill`). La pieza 2 es la novedad: usar Gemini como backend de análisis, sin yt-dlp ni Whisper.

## Comparación de flujos

| Aspecto | Flujo actual (yt-dlp + Whisper) | Flujo Gemini |
|---|---|---|
| Descarga de video | Sí (subtítulos) | No |
| Transcripción local | Sí (Whisper) | No (Gemini lo hace) |
| Timestamps precisos | Sí (del VTT) | Depende del prompt |
| Costo | $0 (local) | Tier gratuito con límites |
| Privacidad | Total (local) | El link del video va a Google |
| Offline | Sí | No |
| Calidad de análisis | Texto literal | Puede resumir y estructurar |

## Pasos

1. **Obtener API key** en https://aistudio.google.com/apikey (gratis).
2. **Probar con un video corto** (el mismo que ya procesamos) usando la API de Gemini con un prompt estructurado:
   - "Resumí este video en 5 puntos con timestamps. Extraé las herramientas mencionadas. Identificá claims sin evidencia."
3. **Comparar resultados** contra la ficha hecha con yt-dlp + Whisper.
4. **Decidir**:
   - Si Gemini da timestamps precisos y mejor análisis → integrarlo como opción en `video-a-skill`.
   - Si no → mantener el flujo actual y descartar.
5. **Si se integra**, agregar un flag `--backend gemini` a `tools/transcript.py` o un script aparte `tools/analyze-gemini.py`.

## Criterios de aceptación

- [ ] La prueba con un video ya procesado da resultados comparables o mejores
- [ ] Los timestamps son precisos (verificables contra el video)
- [ ] El costo real (tokens) está documentado
- [ ] La decisión queda en `docs/decisiones.md`

## Cómo saber si falló

- Gemini no puede acceder al video (privado, sin subtítulos, bloqueado).
- Los timestamps son inventados o imprecisos.
- El tier gratuito no alcanza para videos de más de unos minutos.
- La calidad del análisis es inferior a la ficha manual.

## Rollback

- Borrar la API key si no se usa.
- Mantener el flujo actual sin cambios.

## Notas

- Gemini tiene un tier gratuito con límites de rate y duración de video. Verificar antes de depender de él.
- El video cierra con "comentá YouTube y te paso la guía": es captación de leads, no documentación técnica.
- Si se implementa, conviene que `video-a-skill` ofrezca ambos backends y elija según disponibilidad.
