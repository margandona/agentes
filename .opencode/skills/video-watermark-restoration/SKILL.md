---
name: video-watermark-restoration
description: >
  Evaluate and restore authorized videos with visible overlays using local
  FFmpeg delogo or ProPainter video inpainting. Use when a user requests visual
  watermark removal; inspect a short sample before processing a full video.
---

# Restauración visual de video

## Qué hace

Separa eliminación visual de metadatos. Usa visión sobre fotogramas para ubicar regiones, selecciona `delogo` para fondos simples o ProPainter para reconstrucción temporal y comprueba el resultado visual. La reconstrucción infiere detalles; no recupera con certeza la imagen original.

## Cuándo usarlo

Cuando el usuario pide editar superposiciones visibles de un video propio o autorizado. No aplicar `media-metadata-sanitizer` esperando cambiar píxeles. No retirar credenciales ni prometer una procedencia distinta.

## Procedimiento

1. Inspeccionar fotogramas del principio, medio y final con la herramienta de imágenes; comprobar posición y movimiento de las marcas.
2. Consultar [fuentes y límites](references/backends.md). Evaluar las dependencias en un entorno aislado; no ejecutar `setup.bat` upstream: contiene una ruta absoluta ajena al proyecto.
3. Probar primero un fragmento de 12–25 fotogramas. `delogo` admite varias regiones en una cadena de filtros, pero rellena rectángulos y no reconstruye caras.
4. Para ProPainter, preparar una máscara binaria con blanco en píxeles a reconstruir, preservando ojos, boca y contornos siempre que sea posible. Inspeccionar la máscara superpuesta antes de inferir. Usar `--fp16`, resolución y ventanas temporales acordes a la VRAM medida.
5. Invocar el backend oficial: `python inference_propainter.py --video CARPETA_DE_FRAMES --mask MASCARA.png --output SALIDA --save_fps 25 --fp16 --neighbor_length 4 --subvideo_length 20 --ref_stride 10 --save_frames`. Ajustar FPS al original, sin asumir 25 para todos los videos. Ejecutar desde el directorio de ProPainter.
6. Mirar el resultado con visión. Si destruye detalles faciales o deja marcas, ajustar la máscara o documentar el fallo; no declararlo limpio. Solo extender el procesamiento si la muestra resulta útil.
7. Conservar resolución final y audio del original cuando sea viable; verificar número de cuadros, tiempos, resolución, decodificación y sincronía. Los hashes de video cambiarán porque se modifican píxeles.

## Salida esperada

Un video nuevo, muestra comparativa y registro de parámetros, límites y controles. Nunca sobrescribir originales. Mantener pesos, videos y entornos en `tmp/` del proyecto, fuera de Git.

El ejecutor [scripts/restore.py](scripts/restore.py) admite videos de FPS enteros constantes y conserva el audio en la ejecución completa. Ejecutarlo con el Python que tenga las dependencias de ProPainter:

```powershell
python scripts/restore.py --input entrada.mp4 --output muestra.mp4 --mask mascara.png --model RUTA_PROPAINTER --work TRABAJO_NUEVO --limit-frames 12
```

Tras revisar la muestra, omitir `--limit-frames` y usar otras rutas nuevas de trabajo/salida. Si FFmpeg no está en PATH, pasar `--ffmpeg RUTA_FFMPEG --ffprobe RUTA_FFPROBE`. Reconstruye a 384×680 por defecto; ajustar `--width` y `--height` al aspecto del material, en múltiplos de 8. Componer solo las regiones enmascaradas sobre los originales. Los cortes entre ventanas pueden producir variaciones; revisar antes de entregar.

## Errores comunes

- ProPainter no es una skill de metadatos ni una garantía de eliminación perfecta.
- La optimización ROI del wrapper pierde utilidad si las marcas cubren todo el cuadro.
- Reducir resolución ahorra memoria pero puede introducir detalle blando: componer solo regiones enmascaradas sobre cuadros originales.
- No adoptar rutas Linux, comandos de mensajería ni sobrescrituras del skill externo; esta ejecución es local en Windows.
- Conservar el aviso de reconstrucción: no atribuir origen humano al resultado.
