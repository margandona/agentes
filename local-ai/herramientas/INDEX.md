# Herramientas de IA local evaluadas

| Herramienta | Qué hace | Requisito clave | Veredicto | Fecha |
|---|---|---|---|---|
| [VoiceStudio](voicestudio.md) | Clonar voz, TTS, doblaje, transcripción, audiolibros | CPU alcanza; ~10 GB disco | **Go** (con límites en 6 GB) | 2026-10-18 |
| [LTX Desktop](ltx-desktop.md) | Video/imagen local con modelos LTX | NVIDIA ≥15 GiB VRAM o Mac ≥32 GiB | No-go (6 GB VRAM) | 2026-10-18 |
| [HeyGen descarga](heygen-descarga.md) | Descarga MP4 de videos de HeyGen vía Playwright | Playwright + Chromium | **Go** | 2026-10-18 |
| [Internet access](internet-access.md) | Comparación de repos de acceso a plataformas | No identificado | A verificar | 2026-10-18 |
| [Web-to-video skill](web-to-video-skill.md) | Patrón: skill que lee el proyecto y genera un artefacto | No identificado | Patrón documentado | 2026-10-18 |
| [Frontend tools](frontend-tools.md) | 5 herramientas de diseño/verificación para apps de agentes | No identificado | Patrón documentado | 2026-10-18 |

## Criterio

Cada herramienta se evalúa con la misma grilla:

1. Qué problema resuelve.
2. Requisito de hardware real (verificado en la fuente, no en el video).
3. Si entra en esta máquina.
4. Costo oculto (API, modelos gated, licencias).
5. Veredicto: **go**, **no-go** o **revisar cuando…**
