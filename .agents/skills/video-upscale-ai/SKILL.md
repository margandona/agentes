---
name: video-upscale-ai
description: >
  Upscale authorized videos with Real-ESRGAN Vulkan or fast FFmpeg Lanczos.
  Use for HeyGen 720p videos, YouTube Shorts 1080x1920 exports, resolution
  enhancement, comparison previews, adjustable sharpness, and video batches.
---

# Superresolución de video para Shorts

## Qué hace

Adaptación Python/PowerShell de `pangpang778/real-esrgan-skill`, con licencia MIT y [atribuciones conservadas](references/attribution.md). Genera MP4 H.264/yuv420p y AAC, conserva FPS y crea respaldo del original. Ofrece `fast` (Lanczos) y `quality` (Real-ESRGAN ×4, reducción exacta y mezcla conservadora con Lanczos).

## Cuándo usarlo

Cuando el usuario pide subir resolución, mejorar definición de videos de HeyGen o preparar Shorts a 1080p. El preset `youtube-shorts-1080p` lleva 720×1280 a **1080×1920**; otras proporciones se ajustan con bandas sin recortar. No elimina marcas de agua, no restaura identidades ni certifica detalle original recuperado.

## Procedimiento

1. Leer [instalación y CLI](references/usage.md). Usar el Python local `tmp/upscale-ai/.venv/Scripts/python.exe` desde la raíz del repo. Las rutas de scripts se resuelven respecto a esta skill; si está instalada, su carpeta también contiene los scripts.
2. Ejecutar `scripts/upscale.py doctor --test-engine` y `scripts/upscale.py probe ARCHIVO`. Verificar orientación, FPS racional, códecs y GPU Vulkan; CUDA por sí sola no prueba Vulkan. La detección prioriza NVIDIA sobre la integrada.
3. Antes de procesar un video completo, ejecutar `scripts/upscale.py compare ARCHIVO --output-dir CARPETA_NUEVA --seconds 2`. Genera ambos clips y comparativas `full`/`detail`. La fuente y el respaldo por SHA-256 permanecen intactos.
4. Abrir las comparativas con la herramienta de imágenes y revisar los clips cuando haya reproducción disponible. Comparar ojos, boca, cabello, contornos y letras a escala equivalente; observar diferentes instantes. No declarar mejora basándose solo en tamaño de archivo, resolución o una métrica de nitidez.
5. Registrar `selection`, `reason`, `reviewed_frames` y parámetros en `preview/comparison.json`. Si hay piel plástica, pestañas inventadas, letras deformadas o inestabilidad, elegir `fast` o bajar `--ai-strength`. No añadir suavizado facial ni grano automático. No afirmar validación visual temporal completa a partir de fotogramas aislados.
6. Para el procesamiento completo solicitado, ejecutar `scripts/upscale.py run ARCHIVO --output NUEVO.mp4 --mode quality --ai-strength 0.35 --sharpness 0`, usando la elección de la muestra; o `--mode fast`. No interpolar FPS. Usar `batch` para carpetas. Leer informe y logs; validar con FFprobe y mirar muestras del archivo exportado antes de entregar.

## Salida esperada

Video nuevo, respaldo en `originals/`, informe `.json` con hashes, parámetros, tiempos y checks, y log `.log`. `compare` agrega dos clips y PNG comparativos. Referencia de bitrate: 8 Mbps por debajo de 48 FPS (incluidos 24–30), 12 Mbps desde 48 FPS (incluidos 48–60); es objetivo VBR, no garantía de bitrate constante. El original nunca se sobrescribe.

Invocación natural: «Usá `$video-upscale-ai` para comparar este video de HeyGen y preparar una versión para Shorts a 1080p». OpenCode: «Usá video-upscale-ai para mejorar la resolución de este video». El agente ejecuta el procedimiento y explica la elección visual.

## Errores comunes

- `realesrgan-x4plus` es ×4 nativo. No usar `-s 1.5` ni `-s 2`; el ajuste a 1080 se realiza después.
- La etiqueta `quality` no garantiza que un rostro se vea mejor. El modo real usa Vulkan; si falta GPU/modelo, falla y no simula IA con Lanczos.
- No activar GFPGAN ni otro restaurador facial como paso rutinario. Nitidez cero es el valor inicial; `--sharpness` permite 0–1.
- HDR requiere otro flujo de color; aquí se rechaza. IA rechaza VFR; se conservan FPS racionales CFR como 30000/1001. Leer límites de `fast` con VFR en la guía.
- Para letras pequeñas, una mezcla IA alta puede alterar glifos. Priorizar legibilidad y conservar Lanczos cuando la comparación lo justifique.
- Se conservan etiquetas de color conocidas; si la fuente carece de ellas, no afirmar que se verificó una colorimetría desconocida. El resultado es SDR de 8 bits conforme a yuv420p.
- El trabajo ×4 puede consumir mucho disco y tiempo. El preflight estima espacio conservador; no extrapolar rendimientos de otras GPU. Los clips de prueba también generan respaldos.
