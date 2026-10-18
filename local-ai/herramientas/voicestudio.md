# VoiceStudio — evaluación

- **Qué es:** app de escritorio open source para clonar voz, diseñar voces, doblar video, dictar, transcribir y crear audiolibros. Corre en local.
- **Origen:** video `videos/mmdSu0GoBtU-clon-gratis-de-elevenlabs-voice-studio-clona-tu-voz-en-tu-or/`
- **Repo:** https://github.com/debpalash/VoiceStudio
- **Web:** https://voicestudio.sh
- **Licencia:** AGPL-3.0 (la app). Pesos y voces tienen licencias aparte.
- **Estado:** activo (commit el 2026-10-18), 74.963 estrellas, 8.199 forks
- **Fecha de evaluación:** 2026-10-18

## Qué hace

| Función | Detalle |
|---|---|
| Clonar voz | Clip de referencia + transcripción; zero-shot |
| Diseñar voz | Descripción en texto → perfil de voz |
| Doblaje | Video → transcripción → traducción → TTS por segmento → mezcla |
| Dictado | Widget flotante |
| Transcripción | 646 idiomas |
| Audiolibros / historias | Capítulos, lotes, reanudación |
| API local | Puerto **3900** |
| MCP | `http://localhost:3900/mcp/` para agentes |

## Requisitos

| Plataforma | Soporte |
|---|---|
| Windows 10/11 x64 | oficial |
| macOS Apple Silicon | Metal (MPS) |
| Linux | AppImage / .deb |
| Sin GPU | **funciona en CPU**, más lento |
| Windows on ARM | experimental |

- Disco: **~10 GB** (instalación CPU: ~5 GB).
- GPU NVIDIA: acelera por CUDA; con ≤10 GB de VRAM **serializa** (1 generación a la vez).
- El instalador trae Python, FFmpeg y los pesos; no hace falta toolchain.

## Instalación (Windows)

```powershell
# opción A: instalador desde Releases
# VoiceStudio-Electron-<version>-win-x64.exe

# opción B: script oficial
irm https://voicestudio.sh/install | iex
```

Primer arranque: elegir motor y descargar modelo (el OmniVoice por defecto pesa ~2,3 GB).

## Motores

- **OmniVoice** (por defecto): 646 idiomas, clonación, calidad alta.
- **KittenTTS / Supertonic-3 / PocketTTS**: livianos, pensados para CPU.
- Otros (IndexTTS, CosyVoice, etc.): se gestionan desde el catálogo de modelos.

Regla práctica: en CPU, motor liviano; en GPU de 6 GB, OmniVoice de a uno.

## Rendimiento (según docs del proyecto)

- La primera generación después de abrir es la más lenta (~8 s de carga de pesos).
- Textos largos se parten en chunks; el tiempo crece lineal con la longitud.
- En CPU: **10-50x más lento** que en GPU.
- Aviso a partir de 1200 caracteres en CPU/MPS.
- Con 6 GB: no subir `OMNIVOICE_GPU_WORKERS`; dejar el autosizing.

## Integración con agentes (lo más interesante)

El backend monta un servidor **MCP** en `/mcp/` con estas tools:

| Tool | Qué hace |
|---|---|
| `generate_speech` | texto → audio (WAV, OGG/Opus) |
| `clone_voice` | audio de referencia → perfil de voz |
| `design_voice` | descripción → perfil de voz |
| `describe_voice` | descripción → atributos mapeados |
| `transcribe` | audio → texto (646 idiomas) |
| `list_voices` / `list_languages` | enumerar |
| `check_health` | estado del backend y device |

Config para OpenCode (MCP por HTTP):

```jsonc
{
  "mcp": {
    "voicestudio": {
      "type": "remote",
      "url": "http://localhost:3900/mcp/",
      "enabled": true
    }
  }
}
```

Notas:

- `X-OmniVoice-Client-Id` permite asignar una voz distinta por agente.
- `OMNIVOICE_MCP_OUTPUT_MODE=files` evita devolver el WAV en base64 al contexto del agente.
- `OMNIVOICE_MCP_BASE_PATH` limita qué archivos puede leer/escribir el MCP.
- El servidor escucha solo en loopback por defecto.

## Privacidad

- El flujo local no sube audio ni texto.
- Servicios remotos y telemetría son **opcionales** y requieren consentimiento.
- El doblaje puede traducir con **NLLB local** o con un proveedor LLM en la nube: si elegís nube, el texto sale de la máquina.
- La app guarda voces, proyectos y ajustes en datos locales; tratarlos como datos sensibles.

## Legal y ético

- Clonar **solo voces propias o con consentimiento explícito y verificable**.
- No usar para suplantar identidad, fraude, acoso ni contenido sexual no consentido.
- Divulgar que el audio es sintético cuando la plataforma o la ley lo exijan (normas de transparencia de IA).
- La voz puede ser dato biométrico o personal bajo GDPR y leyes equivalentes: guardar la mínima referencia necesaria y borrarla cuando no se use.
- AGPL-3.0: usar la app localmente no obliga a nada; distribuir una versión modificada sí obliga a liberar el código.
- Los pesos de los modelos pueden prohibir uso comercial: revisar la licencia de cada motor antes de monetizar.

## Veredicto

**GO.** Es la primera herramienta de la pista local que corre en esta máquina sin comprar nada, y además se integra con agentes por MCP. El costo es $0 (solo luz) y el riesgo principal no es técnico: es el uso indebido de voces.

## Costo

- App: $0.
- Luz: ~$0,03/h de GPU; en CPU, menos.
- Disco: ~10 GB.
- Tiempo: la primera configuración, ~30-45 min contando descargas.

## Cuándo revisar

- Si la calidad en español no alcanza: probar otro motor (IndexTTS, Qwen3-TTS) desde el catálogo.
- Si el doblaje necesita más idiomas o voces: evaluar nube solo para lo que no se pueda local.
- Si aparece una GPU de 16 GB+: subir a OmniVoice con paralelismo.

## Fuentes

- README: https://github.com/debpalash/VoiceStudio
- Instalación Windows: `docs/install/windows.md`
- Rendimiento: `docs/performance.md`
- MCP: `docs/mcp.md`
- Repo API (estrellas/licencia): https://api.github.com/repos/debpalash/VoiceStudio (2026-10-18)
