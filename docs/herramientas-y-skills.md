# Skills y herramientas del laboratorio

Mapa de todo lo que usamos en `agent-lab`: skills, scripts propios, herramientas del agente y software externo. Sirve para saber **qué tenemos, para qué sirve y cuándo se usa**.

> Este documento es la vista de conjunto. La fuente de verdad de cada pieza sigue siendo su `SKILL.md`, su script o su ficha en `local-ai/herramientas/`.

## Cómo leerlo

| Nivel | Qué es | Dónde vive |
|---|---|---|
| **Skills** | Procedimientos que un agente puede repetir | `skills/`, `.opencode/skills/` |
| **Scripts del repo** | Automatizaciones propias de la ingesta | `tools/` |
| **Herramientas del agente** | Lo que yo (OpenCode) puedo ejecutar en una sesión | runtime |
| **Software externo** | Binarios y apps que sostienen todo | máquina / `tmp/` |
| **Servicios locales** | APIs que corren en esta PC | puertos locales |

---

## 1. Skills del repo (procedimientos)

Viven en `skills/` como fuente canónica y se **espejan** en `.opencode/skills/` (OpenCode las carga desde ahí) y `.agents/skills/` (otros clientes). Si editás una, sincronizá la copia.

| Skill | Qué hace | Cuándo se usa | Origen |
|---|---|---|---|
| [six-docs-before-build](../skills/six-docs-before-build/SKILL.md) | Exige los 6 documentos (PRD, TRD, flujo, brief de diseño, esquema de backend, plan) **antes** de escribir código con un agente | Arrancar una app/agente, o cuando el agente empezó a improvisar | video `UADO82Ac7bo` |
| [agent-with-memory-and-tools](../skills/agent-with-memory-and-tools/SKILL.md) | Convierte un chatbot en agente: memoria del historial + conocimiento del negocio + herramientas ejecutables | Diseñar un agente para WhatsApp, Telegram, email o web; diagnosticar por qué un bot "no recuerda" o "no hace nada" | video `vlKWMfbY9BA` |
| [resume-optimization-prompts](../skills/resume-optimization-prompts/SKILL.md) | Adapta un CV a una oferta: claridad, resultados respaldados, matriz de requisitos y propuesta de valor. No inventa credenciales | Optimizar un CV, revisar compatibilidad ATS, preparar una postulación | video `s_xr--Zp5Fg` |
| [media-metadata-sanitizer](../skills/media-metadata-sanitizer/SKILL.md) | Inspecciona, elimina selectivamente metadatos de privacidad y verifica el resultado. Protege credenciales de procedencia | Limpiar MP4/MOV/MKV/WEBM/JPEG/PNG/WEBP antes de publicar o compartir; lotes | pedido directo |
| [video-watermark-restoration](../skills/video-watermark-restoration/SKILL.md) | Quita marcas visuales con `delogo` (fondos simples) o ProPainter (reconstrucción temporal). Prueba en muestra antes del video completo | Restaurar videos autorizados con overlays fijos | repos indicados |
| [video-upscale-ai](../skills/video-upscale-ai/SKILL.md) | Sube resolución con Real-ESRGAN Vulkan (calidad) o Lanczos (rápido). Conserva FPS, audio y respaldo | Shorts 1080×1920, videos HeyGen 720p, comparativas IA vs Lanczos, lotes | adaptación MIT de `pangpang778/real-esrgan-skill` |
| [app-replica-recon](../skills/app-replica-recon/SKILL.md) | Recon clean-room de una app: pantallas, flujos, componentes, modelo de datos con evidencia y matriz de features. Portable a cualquier proyecto | Decidir si una app se puede reconstruir, antes de escribir código; clonar funcionalidad sin copiar código ni assets | video `-PItFh9VLa4` + adaptación MIT de `Jakeschincariol/replica-skill` |
| [app-gap-analysis](../skills/app-gap-analysis/SKILL.md) | Lee reseñas públicas reales y las convierte en quejas, faltantes, fixes priorizados y ángulo de venta, con citas linkeadas | Diferenciar un clon, poner precio, elegir nicho; después del recon o del parity check | video `-PItFh9VLa4` + adaptación MIT de `Jakeschincariol/replica-skill` |
| [shorts-to-skill](../skills/shorts-to-skill/SKILL.md) | Trata videos ≤3 min: recupera nombres del ASR, verifica afirmaciones y decide entre skill, ficha o descarte | El input es un Short, Reel o TikTok; hay clickbait o lista de herramientas | videos `hVlnCKQXYkk` + `-1t8wdk8O14` |
| [agent-stack-audit](../skills/agent-stack-audit/SKILL.md) | Inventaría y poda el stack: skills y espejos, MCP, permisos, memoria, riesgo de terceros y costo de contexto | Antes de instalar un plugin; cuando una skill no carga; limpieza periódica | video `hVlnCKQXYkk` + drift detectado |
| [synthetic-audience-test](../skills/synthetic-audience-test/SKILL.md) | Ensaya landing, precio o anuncio con personas sintéticas aisladas; devuelve hipótesis falsables y guion de entrevistas | Antes de publicar; para descubrir objeciones; nunca como evidencia de demanda | video `-1t8wdk8O14` |

### Skills de plataforma

| Skill | Qué hace | Dónde vive |
|---|---|---|
| [video-a-skill](../.opencode/skills/video-a-skill/SKILL.md) | Orquesta el pipeline del repo: transcripción → ficha con timestamps → propuesta → skill/plan → índices | Solo local, `.opencode/skills/` |
| `agent-reach` | Acceso a YouTube, X, Reddit, GitHub, Bilibili, Xiaohongshu, Douyin, WeChat, LinkedIn, Boss直聘, RSS y web en general. Busca, lee e interactúa | Global, `~/.config/opencode/skills/agent-reach` |

**Cuándo uso una y cuándo la otra:** si el input es un video de YouTube que hay que convertir en artefactos del repo, `video-a-skill`. Si hay que **buscar o leer** algo en internet, `agent-reach`.

---

## 2. Scripts propios (`tools/`)

| Script | Qué hace | Uso típico |
|---|---|---|
| [transcript.py](../tools/transcript.py) | Baja metadatos y subtítulos con yt-dlp y crea `videos/<slug>/metadata.json` + `transcript.txt` | `python tools/transcript.py "<URL>"` · flags `--langs "es,en"`, `--slug` |
| [triage.py](../tools/triage.py) | Solo metadatos (sin transcripción). Devuelve una línea JSON por video para decidir si merece ficha | `python tools/triage.py "URL1" "URL2"` · `--file urls.txt` |
| [shorts_gate.py](../tools/shorts_gate.py) | Señales de un video corto: CTA, cifras, pasos, fuentes y nombres dudosos; veredicto preliminar | `python tools/shorts_gate.py "<URL>"` · `--json` · `--langs` |
| [draft_pack.py](../tools/draft_pack.py) | Ingesta + gate + `draft.md` con nombres a confirmar, afirmaciones candidatas y propuesta en blanco | `python tools/draft_pack.py "<URL>"` · `--force` |
| [download-heygen.py](../tools/download-heygen.py) | Descarga el MP4 de HeyGen con Playwright. Necesario porque la URL de CloudFront está firmada y `curl`/yt-dlp reciben 403 | `python tools/download-heygen.py "<URL>" --out salida.mp4` |
| [doctor.ps1](../tools/doctor.ps1) | Chequeo del entorno: python, yt-dlp, ffmpeg, node, git, gh, ollama y skill `agent-reach` | `powershell -File tools/doctor.ps1` |
| [yt-dlp.cmd](../tools/yt-dlp.cmd) | Atajo de `python -m yt_dlp %*` para cuando el entry point no está en PATH | `.\tools\yt-dlp.cmd -F "<URL>"` |

Regla del repo: todo script corre en **Windows/PowerShell** y falla con mensaje claro.

---

## 3. Herramientas del agente (OpenCode)

Lo que puedo ejecutar en una sesión de este repo, y para qué lo uso:

| Herramienta | Para qué |
|---|---|
| `read` / `write` / `edit` | Leer fichas y transcripciones, crear skills y planes, hacer cambios puntuales |
| `glob` / `grep` | Ubicar archivos y buscar texto (slug, nombre de skill, timestamps) sin abrir todo |
| `shell` (PowerShell) | Correr `transcript.py`, `doctor.ps1`, git, pruebas de las skills |
| `webfetch` / `websearch` | Verificar una fuente original o un dato que el video no prueba |
| `skill` | Cargar una skill (por ejemplo `video-a-skill`) y seguir su procedimiento |
| `subagent` | Delegar exploración o trabajo paralelo (explore / general) |
| `question` | Pedir una decisión antes de escribir artefactos o tocar algo destructivo |
| `execute` (Code Mode) | Scriptear varias llamadas a herramientas en una sola corrida |
| `todowrite` | Plan de tareas en trabajos de varios pasos |
| `opencode.*` (sesiones, worktrees, modelos, recursos MCP) | Mover/renombrar sesiones, aislar trabajo en un worktree, consultar modelos y recursos MCP |

### Comando `/video`

`.opencode/commands/video.md` fuerza el protocolo completo con una sola invocación:

```
/video <URL>
```

Hace el paquete de borrador, exige verificar nombres y afirmaciones, escribe la ficha, decide el gate y **se detiene** a esperar aprobación antes de crear un skill. Es la forma recomendada de arrancar: evita olvidarse un paso.

### MCP instalado: `image-lab`

Servidor MCP local ([`tools/mcp-image`](../tools/mcp-image/README.md)) para generar imágenes:

| Tool | Qué hace | Requisito |
|---|---|---|
| `image-lab.generate_icon` | Dibuja un PNG determinista: video, llave, cerebro, escudo, engranaje, etc. 30 estilos | Ninguno: funciona sin internet |
| `image-lab.generate_image` | Genera una imagen con IA y la guarda en disco | `OPENAI_API_KEY` o `GEMINI_API_KEY` |
| `image-lab.list_providers` | Informa qué claves hay y qué estilos existen | Ninguno |

Configurado en `~/.config/opencode/opencode.jsonc`. Verificar con `opencode mcp list` (debe decir `✓ image-lab connected`). Sin clave de API, la generación con IA devuelve un error explicado; los íconos funcionan igual.

Permisos y reglas de conducta están en [AGENTS.md](../AGENTS.md): fuente primero, no inventar, timestamps, un artefacto por pieza.

---

## 4. Software externo

### Instalado y en uso

| Herramienta | Versión / ubicación | Para qué |
|---|---|---|
| **Python** | 3.13 (base) | Scripts de ingesta y automatizaciones |
| **Node.js** | 24 | MCP y herramientas JS |
| **Git** + **GitHub CLI** | 2.55 / 2.96 | Versionado, repos, issues |
| **yt-dlp** | 2026.08.19 | Bajar videos, metadata y subtítulos |
| **uv** | en PATH | Crear entornos y bajar intérpretes aislados (`tmp/python`, `tmp/*/.venv`) |
| **FFmpeg / FFprobe** | `tmp/media-tools/ffmpeg` (no en PATH) | Cortes, muestras, encoding H.264/AAC, extracción de frames |
| **ExifTool** | `tmp/media-tools/exiftool` (no en PATH) | Leer/escribir metadatos; base del saneamiento |
| **Playwright + Chromium** | instalado | Descargar HeyGen y verificar interfaces locales |
| **Ollama** | en PATH, `127.0.0.1:11434` | Modelos locales (falta benchmark formal) |
| **OpenCode** | agente de coding | Ejecuta este repo; TUI y web (`127.0.0.1:45278`) |

### Empaquetado para las skills audiovisuales

| Herramienta | Ubicación | Para qué | Licencia / nota |
|---|---|---|---|
| **Real-ESRGAN (ncnn Vulkan)** | `tmp/upscale-ai/engine` | Superresolución x4 en la GPU, modo `quality` | MIT + atribuciones en la skill |
| **ProPainter** | `tmp/watermark/ProPainter` | Inpainting temporal para marcas difíciles | S-Lab **no comercial** |
| **Torch + Pillow** | `tmp/watermark/.venv` (Python 3.11) | Inferencia y manejo de máscaras | — |
| **Tkinter** | Python estándar | Interfaz de Video Studio | — |

### Evaluado pero no adoptado

| Herramienta | Estado | Motivo |
|---|---|---|
| **VoiceStudio** | Go con límites | Clonación de voz, TTS, doblaje y transcripción local. Corre en CPU; en 6 GB de VRAM hay restricciones |
| **LTX Desktop** | No-go | Pide NVIDIA ≥15 GiB VRAM o Mac ≥32 GiB; esta máquina tiene 6 GB |
| **LM Studio / llama.cpp / vLLM** | Documentados | Alternativas a Ollama para comparar o exprimir hardware; no instalados |
| **Open WebUI** | Documentado | Front-end tipo ChatGPT contra Ollama; no instalado |
| **Continue (VS Code)** | Documentado | Copilot local contra Ollama; no instalado |
| **Gemini API** | Plan borrador | Transcripción/análisis de videos sin descargar; el flujo por defecto sigue siendo yt-dlp + Whisper |

Detalle y veredictos: [local-ai/herramientas/INDEX.md](../local-ai/herramientas/INDEX.md).

---

## 5. Servicios locales

| Servicio | Puerto / URL | Qué da |
|---|---|---|
| OpenCode | `http://127.0.0.1:45278` | Web UI + TUI de la misma sesión |
| Ollama | `http://127.0.0.1:11434` | API de modelos locales (`/api/tags`) |
| VoiceStudio | `http://127.0.0.1:3900` | Backend de voz: `generate_speech`, `clone_voice`, `transcribe`, `list_voices`, `check_health` |
| VoiceStudio MCP | `http://127.0.0.1:3900/mcp/` | Las mismas tools para agentes. **No** está configurado en `opencode.jsonc` todavía |

Mapa completo y cómo levantar cada cosa: [docs/acceso.md](acceso.md). Panel visual: [local-ai/dashboard.html](../local-ai/dashboard.html).

---

## 6. Apps propias

| App | Qué hace | Cómo se abre |
|---|---|---|
| [Video Studio](../apps/video-studio/README.md) | Interfaz Windows (Tkinter) para restaurar marcas, escalar a 1080p, comparar Lanczos/IA y sanear metadatos. Todo local, sin subir videos | Doble clic en `Abrir Video Studio.cmd` |

Cada ejecución crea su propia carpeta con copia del original, intermedios, `resumen.json` y `.log`. No sobrescribe resultados anteriores.

---

## 7. Plantillas

| Plantilla | Para qué |
|---|---|
| [ficha-video.md](../templates/ficha-video.md) | Ficha de análisis de un video, con timestamps y sección "Humo / a verificar" |
| [ficha-short.md](../templates/ficha-short.md) | Ficha para videos ≤3 min: gate, nombres recuperados del ASR y tabla de afirmaciones |
| [SKILL.md](../templates/SKILL.md) | Estructura de una skill nueva |
| [plan.md](../templates/plan.md) | Plan de implementación con criterios de aceptación |
| [agente.md](../templates/agente.md) | Definición de agente (prompt, modelo, tools, permisos, límites) |
| [spec.md](../templates/spec.md) | Base de los 6 documentos previos |

---

## 8. Mapa rápido: quiero… → usá…

| Quiero… | Usá… |
|---|---|
| Convertir un video de YouTube en ficha + skill + plan | `/video <URL>` o `video-a-skill` + `tools/transcript.py` |
| Procesar un Short, Reel o TikTok (≤3 min) | `python tools/shorts_gate.py "<URL>"` → `shorts-to-skill` + `templates/ficha-short.md` |
| Auditar qué skills, MCP y permisos tenemos de verdad | `agent-stack-audit` |
| Probar una landing, precio o anuncio antes de lanzar | `synthetic-audience-test` |
| Decidir si un video merece ficha | `tools/triage.py` |
| Buscar o leer algo en X, Reddit, YouTube, GitHub, web | skill `agent-reach` |
| Bajar un video de HeyGen | `tools/download-heygen.py` |
| Quitar una marca de agua de un video propio | `video-watermark-restoration` o Video Studio |
| Subir un video a 1080×1920 | `video-upscale-ai` o Video Studio |
| Limpiar metadatos antes de publicar | `media-metadata-sanitizer` o Video Studio |
| Adaptar el CV a una oferta | `resume-optimization-prompts` |
| Empezar una app o un agente sin que improvise | `six-docs-before-build` |
| Clonar una app, estudiarla y vender una versión mejor | `app-replica-recon` → plan [`replica-app-mejorada`](../plans/replica-app-mejorada.md) → `app-gap-analysis` |
| Diseñar un agente que recuerde y ejecute acciones | `agent-with-memory-and-tools` |
| Correr un modelo en esta PC | Ollama; ver [plans/ia-local-rtx-4050.md](../plans/ia-local-rtx-4050.md) |
| Clonar una voz o transcribir audio | VoiceStudio (app abierta + puerto 3900) |
| Generar un ícono o una imagen | MCP `image-lab` (`generate_icon` / `generate_image`) |
| Verificar que el entorno está sano | `tools/doctor.ps1` |

---

## 9. Lo que **no** está en uso (para no confundir)

- **Gemini API**: sigue como plan para transcripción; `image-lab` la usa solo para imágenes y solo si hay `GEMINI_API_KEY`.
- **`image-lab`**: instalado como MCP. Los íconos funcionan offline; `generate_image` queda inactivo hasta configurar una clave.
- **VoiceStudio por MCP**: documentado, no configurado en `opencode.jsonc`.
- **Open WebUI, Continue, LM Studio, llama.cpp, vLLM**: documentados como opciones, no instalados.
- **LTX Desktop**: descartado por VRAM.
- **FFmpeg y ExifTool**: funcionan, pero **no están en PATH**; las skills los resuelven desde `tmp/media-tools`.

---

## 10. Mantenimiento

Al sumar o retirar una pieza:

1. Actualizar la tabla correspondiente en este archivo.
2. Actualizar [skills/INDEX.md](../skills/INDEX.md), [plans/INDEX.md](../plans/INDEX.md) o [local-ai/herramientas/INDEX.md](../local-ai/herramientas/INDEX.md) según el caso.
3. Si es una skill, sincronizar `skills/`, `.opencode/skills/` y `.agents/skills/`.
4. Si es una herramienta nueva, aplicar el criterio de [docs/stack.md](stack.md): resuelve algo manual, corre acá, se puede medir y se puede abandonar sin perder datos.
