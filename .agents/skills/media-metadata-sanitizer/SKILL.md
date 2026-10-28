---
name: media-metadata-sanitizer
description: >
  Inspect, selectively remove ordinary privacy metadata, and verify authorized
  video and image files. Use for metadata reports, privacy cleanup, or local
  batch distribution preparation while protecting detected provenance credentials.
---

# Saneamiento de metadatos multimedia

## Qué hace

Inspecciona y clasifica metadatos; elimina categorías ordinarias seleccionadas en una salida nueva y verifica su contenido. Admite MP4, MOV, MKV, WEBM, JPEG, PNG y WEBP según el contenido real.

## Cuándo usarlo

Para preparar multimedia propia o autorizada para distribución, inspeccionar ubicación/software/fechas/datos personales o comparar dos archivos. La ausencia de metadatos de HeyGen, Synthesia, Runway u otra herramienta no demuestra origen humano.

## Procedimiento

1. Usar Python >=3.11 con `ffmpeg`, `ffprobe` y `exiftool` en PATH. Leer [campos y limitaciones](references/metadata-fields.md) para instalar, elegir categorías o interpretar credenciales.
2. Desde la carpeta de la skill, ejecutar `python scripts/inspect.py archivo.mp4`. Elegir categorías con el usuario según su solicitud; las cuatro categorías ordinarias son el valor predeterminado.
3. Revisar la selección con `python scripts/sanitize.py archivo.mp4 --output limpio.mp4 --categories personal location --dry-run`.
4. Ejecutar el mismo comando sin `--dry-run`. Si detecta procedencia protegida o no puede verificar la remoción e integridad, detenerse con el error informado. No retirar credenciales para poder continuar.
5. Comparar con `python scripts/verify.py archivo.mp4 limpio.mp4` o procesar un directorio con `python scripts/batch.py ./entrada --output ./procesados --categories software`.

## Salida esperada

JSON en stdout, errores en stderr y código 1 si falla. El saneamiento publica solo tras verificar; los informes incluyen hashes SHA-256, diferencias y campos restantes. Batch conserva la estructura relativa y registra cada error. Puede guardarse stdout en un informe JSON.

## Errores comunes

- No usar la misma ruta ni una salida existente; no se sobrescribe ningún destino.
- No cambiar la extensión para convertir el formato. El formato de salida coincide con el real.
- No interpretar hashes de archivo distintos como pérdida de calidad: se comparan también hashes audiovisuales decodificados.
- Un campo no reconocido queda intacto. La remoción no cubre marcas de agua ni identificadores dentro del contenido.
- Un remux puede afectar firmas; los indicios detectados bloquean la operación, pero su ausencia no garantiza que no haya credenciales.

## Instalación e invocación

La carpeta completa es autocontenida. Para instalar en el proyecto, desde la raíz del repo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File skills/media-metadata-sanitizer/scripts/install.ps1 -Target OpenCode
powershell -NoProfile -ExecutionPolicy Bypass -File skills/media-metadata-sanitizer/scripts/install.ps1 -Target Codex
```

Se copia a `.opencode/skills/media-metadata-sanitizer/` o `.agents/skills/media-metadata-sanitizer/`. El instalador rechaza destinos existentes. OpenCode descubre `SKILL.md` y carga la skill mediante su herramienta `skill`; pedir «usá media-metadata-sanitizer para inspeccionar este archivo». En Codex: `$media-metadata-sanitizer inspeccioná este archivo`. Los scripts también funcionan sin agente.

Pruebas: `python -m unittest discover -s skills/media-metadata-sanitizer/tests -v`, desde la raíz del repo.
