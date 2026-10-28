# agent-lab

Laboratorio personal para convertir videos de YouTube (y otras fuentes) en **skills**, **planes** y **agentes** que funcionen de verdad. También es el lugar donde probamos **IA local** (Ollama, LM Studio, llama.cpp, vLLM).

La regla del repo: **nada entra sin fuente y sin ficha**. Cada video deja un rastro: metadatos → transcripción → ficha → skill y/o plan → índice.

## Dos pistas, un solo repo

| Pista | Dónde vive | Qué produce |
|---|---|---|
| **Agentes** | `videos/`, `skills/`, `plans/`, `agents/` | procedimientos y planes para construir agentes |
| **IA local** | `local-ai/` | evaluaciones de modelos/herramientas, benchmarks, hardware |

Regla para decidir:

- Si el video enseña **un procedimiento que un agente puede repetir** → pista agentes.
- Si el video muestra **una herramienta o modelo para correr en la máquina** → pista IA local.
- Si es ambas, la ficha va en `videos/` y se parte: el procedimiento a `skills/`, la herramienta a `local-ai/herramientas/`.

Un repo y no dos porque comparten la misma ingesta (transcripción + ficha) y los mismos índices. Se separa recién si la pista de IA local crece al punto de tener su propio pipeline. Decisión registrada en `docs/decisiones.md`.

## Cuatro puertas de entrada

| Traés… | Sale… | Pedido típico |
|---|---|---|
| Un link de video | Ficha verificada + skill y/o plan | “Procesá este video: \<url\>” |
| Un video o una foto | Archivo limpio, más grande o sin marca | “Limpiá este MP4 y subilo a 1080” |
| Una idea o una app | Documentos, recon, plan, hipótesis | “Quiero clonar esta app y mejorarla” |
| Una pregunta o un dato | Respuesta con fuente | “¿MiroFish sirve para probar un lanzamiento?” |

Atajo recomendado para videos: `/video <url>`. Hace ingesta, gate, ficha y propuesta; se detiene a esperar aprobación antes de crear un skill.

## Estructura

```
agent-lab/
├─ videos/           Un folder por video: metadata.json, transcript.txt, ficha.md
├─ skills/           Skills reutilizables (formato SKILL.md compatible con OpenCode / Claude)
├─ plans/            Planes de implementación paso a paso, con criterios de aceptación
├─ local-ai/         Guías y scripts para correr modelos en tu máquina
├─ agents/           Definiciones de agentes (prompt, tools, permisos)
├─ prompts/          Prompts sueltos, versionados
├─ templates/        Plantillas: ficha de video, skill, plan, agente
├─ tools/            Scripts: ingesta, gate de videos, borrador, doctor del entorno
├─ docs/             Metodología, stack, decisiones, mapa de herramientas
├─ .opencode/skills/ Skills locales de este repo (ej: video-a-skill)
└─ .opencode/commands/ Comandos como /video
```

## Flujo de trabajo

1. **Ingesta** — Pasás un link de YouTube:
   ```powershell
   python tools/transcript.py "https://www.youtube.com/watch?v=XXXX"
   ```
   Crea `videos/<slug-del-video>/` con `metadata.json` y `transcript.txt`.

2. **Ficha** — Se completa `ficha.md` con la plantilla `templates/ficha-video.md`. Sin ficha no se avanza: es el filtro contra el hype.

3. **Extracción** — De la ficha salen una o más piezas:
   - un **skill** en `skills/<nombre>/SKILL.md` (procedimiento repetible)
   - un **plan** en `plans/<nombre>.md` (implementación con pasos y criterios)
   - una nota en `local-ai/` si es sobre modelos locales

4. **Registro** — Se agrega la fila en el `INDEX.md` correspondiente.

## Skills ya instaladas

Hay 12 skills en uso: 11 canónicas en `skills/` (espejadas en `.opencode/skills/` y `.agents/skills/`) y `video-a-skill`, que vive solo en `.opencode/skills/`.

| Familia | Skills |
|---|---|
| Videos → conocimiento | `video-a-skill`, `shorts-to-skill` |
| Archivos de video/foto | `video-upscale-ai`, `video-watermark-restoration`, `media-metadata-sanitizer` |
| Apps y productos | `six-docs-before-build`, `app-replica-recon`, `app-gap-analysis`, `synthetic-audience-test` |
| Agentes | `agent-with-memory-and-tools`, `agent-stack-audit` |
| Personas | `resume-optimization-prompts` |

Además: `agent-reach` (global) para buscar y leer en internet, el comando `/video` para procesar un video de punta a punta, y el MCP `image-lab` para íconos e imágenes.

Mapa completo, con cuándo usar cada una: [`docs/herramientas-y-skills.md`](docs/herramientas-y-skills.md).
Versión explicada fácil: [`docs/guia-facil.pdf`](docs/guia-facil.pdf) (puede no incluir las skills más nuevas).

## Convenciones

- Nombres de carpeta en `kebab-case`, sin acentos ni espacios.
- Un video = una carpeta. El slug es `<id>-<titulo-corto>` (ej: `dQw4w9WgXcQ-agentes-con-memoria`).
- Toda afirmación técnica en una ficha lleva **timestamp** del video o link a la fuente original.
- Lo que el video promete y no prueba va a la sección `## Humo / a verificar`.
- Los skills se escriben en inglés o español, pero con `name` y `description` en el frontmatter siempre en inglés (mejor matching).
- **Voz:** ninguna clonación sin leer `docs/consentimiento-voz.md`. Los clips de referencia viven fuera del repo.

## Empezar

```powershell
# estado del entorno
powershell -File tools/doctor.ps1

# panel visual de accesos
start local-ai/dashboard.html

# primer video
python tools/transcript.py "<URL>"
```

Mapa completo de servicios y puertos: `docs/acceso.md`.

## Estado

- [x] Repo base + metodología
- [x] Skill `agent-reach` instalada + yt-dlp
- [x] Ollama instalado (falta benchmark)
- [x] Primer video procesado (LTX Desktop, no-go por VRAM)
- [x] MCP `image-lab`: íconos offline; imágenes con IA a la espera de una clave
- [x] 12 skills propias documentadas y espejadas
- [x] Pipeline de video corto (`shorts_gate`, `draft_pack`) y comando `/video`
- [ ] Primer agente corriendo
