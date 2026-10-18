---
name: video-a-skill
description: >
  Process a YouTube video into this repo's artifacts: transcript, ficha (analysis sheet),
  reusable skill and implementation plan. Use when the user shares a YouTube URL and asks
  to learn from it, extract skills, build an agent from it, or add it to agent-lab.
  Triggers: "procesá este video", "mira este video", "sacá un skill de esto",
  "convertí este video en un plan", "youtube.com/watch", "youtu.be".
---

# Video → skill / plan

## Qué hace

Convierte un video de YouTube en artefactos verificables dentro de `agent-lab`.

## Cuándo usarlo

- El usuario pasa un link de YouTube y quiere aprender, replicar o extraer ideas.
- Hay que decidir si un video merece un skill o un plan.

## Procedimiento

1. **Ingesta**
   ```powershell
   python tools/transcript.py "<URL>"
   ```
   Verificar que existan `videos/<slug>/metadata.json` y `transcript.txt`.

   **Alternativa con Gemini (pieza 2 del video RDWPjBqRrro):** Gemini entiende videos de YouTube de fábrica, sin descargar ni transcribir. Si se usa, el flujo cambia: en lugar de `transcript.py`, se consulta la API de Gemini con el link del video y se obtiene un resumen estructurado. Ver `plans/transcripcion-con-gemini.md`. Por ahora el flujo por defecto sigue siendo yt-dlp + Whisper local.

2. **Lectura**
   Leer la transcripción completa. Si es muy larga, leer por bloques y anotar timestamps.

3. **Ficha**
   Copiar `templates/ficha-video.md` a `videos/<slug>/ficha.md` y completarla.
   Reglas:
   - Cada bullet con `[mm:ss]`.
   - "Humo / a verificar" es obligatorio, aunque esté vacío con justificación.
   - No resumir el video: extraer lo accionable.

4. **Propuesta**
   Antes de escribir artefactos, listar en el chat:
   ```
   skill: <nombre> — <una línea>
   plan:  <nombre> — <una línea>
   ninguno — <por qué no vale la pena>
   ```
   Esperar aprobación.

5. **Escritura**
   - Skill → `skills/<nombre>/SKILL.md` desde `templates/SKILL.md`
   - Plan → `plans/<nombre>.md` desde `templates/plan.md`
   - Ambos referencian el video y los timestamps.

6. **Registro**
   Actualizar `videos/INDEX.md` y el índice que corresponda.

## Salida esperada

```
videos/<slug>/
  metadata.json
  transcript.txt
  ficha.md
skills/<nombre>/SKILL.md     (opcional)
plans/<nombre>.md            (opcional)
```

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| No hay subtítulos | `transcript.txt` vacío | Probar `--sub-lang es,en` o usar whisper local |
| Video muy largo | lectura incompleta | Procesar por capítulos y anotar qué falta |
| Skill genérico | "usar buenas prácticas" | Reescribir con pasos verificables |
| Duplicado | dos skills iguales | Buscar en `skills/INDEX.md` antes de crear |

## Origen

Pipeline definido en `docs/metodologia.md`.
