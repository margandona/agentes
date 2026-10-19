# Instalación, comandos y límites

## Instalación del proyecto en Windows

Desde la raíz de `agent-lab`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File skills/video-upscale-ai/scripts/install.ps1 -DownloadEngine
```

El instalador usa uv si está disponible, prepara Python 3.11 y Pillow en `tmp/upscale-ai/.venv/`, descarga el paquete oficial verificado si falta y prueba una inferencia Vulkan real. Si ya existe Python >=3.11, puede pasarse `-Python RUTA_PYTHON`. No modifica instalaciones globales ni elimina skills previas. Una instalación idéntica se conserva; si difiere, falla para evitar sobrescribir trabajo. La excepción de PowerShell se limita a esa invocación.

Instala copias autocontenidas de instrucciones y scripts en `.agents/skills/video-upscale-ai/` y `.opencode/skills/video-upscale-ai/`. La fuente mantenida está en `skills/video-upscale-ai/`. La nueva skill estará disponible para descubrimiento en el siguiente turno/sesión. El directorio `tmp/` contiene runtime y artefactos, no se versiona; si se elimina, repetir instalación.

FFmpeg y FFprobe se buscan en PATH o en la caché previa del proyecto `tmp/media-tools/ffmpeg/`. Si faltan, instalar una compilación oficial/enlazada desde https://ffmpeg.org/download.html (en Windows también `winget install Gyan.FFmpeg`) o pasar `--ffmpeg RUTA --ffprobe RUTA`. No se instalan globalmente de forma automática. Usar una versión reciente con `-fps_mode` y `force_divisible_by`.

Motor: paquete Windows v0.2.5.0/20220424 de Real-ESRGAN, SHA-256 `abc02804e17982a3be33675e4d471e91ea374e65b70167abc09e31acb412802d`, obtenido del release oficial y fijado para reproducibilidad. No se usan proxies ni ejecutables de los forks. Mantener `models/` junto al `.exe`. También se admiten `FFMPEG_BIN`, `FFPROBE_BIN`, `REALESRGAN_BIN` o `--engine RUTA`.

El procesamiento Python usa la biblioteca estándar; Pillow se carga para pruebas de motor y previews. No se requieren CUDA, PyTorch ni Bash. El bootstrap PowerShell está probado en Windows; otros sistemas pueden ejecutar Python con FFmpeg y el motor oficial de su plataforma instalado manualmente, pero no se probaron en esta entrega.

## Comandos

Los ejemplos parten de la raíz del repo. En PowerShell:

```powershell
$upscalePython = 'tmp/upscale-ai/.venv/Scripts/python.exe'
$upscaleScript = 'skills/video-upscale-ai/scripts/upscale.py'
& $upscalePython $upscaleScript doctor --test-engine
& $upscalePython $upscaleScript probe 'entrada.mp4'
& $upscalePython $upscaleScript compare 'entrada.mp4' --output-dir 'tmp/comparacion-nueva' --seconds 2
& $upscalePython $upscaleScript run 'entrada.mp4' --output 'tmp/rapido.mp4' --mode fast
& $upscalePython $upscaleScript run 'entrada.mp4' --output 'tmp/ia.mp4' --mode quality --ai-strength 0.35 --sharpness 0
& $upscalePython $upscaleScript batch './entrada' --output-dir './salida' --mode fast
```

`--help` en cada operación. `--verbose` muestra comandos en stderr. `--seconds` limita a una muestra de cuadros completos (puede durar una fracción menos que lo pedido); omitirlo procesa el archivo completo. `--keep-work` conserva PNG intermedios para diagnóstico. `--work-dir` cambia el disco de temporales; las rutas de fuente/salida deben ser distintas. Lote mantiene subdirectorios y nombres con extensión original para evitar colisiones entre MP4/MOV del mismo nombre. Procesa MP4, MOV, MKV y WEBM y registra errores por archivo; salida separada, sin anidamiento.

Si los clips ya existen: `preview ENTRADA --fast RAPIDO.mp4 --quality IA.mp4 --output-dir PREVIEW_NUEVO`. `full-*.png` muestra el cuadro completo; `detail-*.png` es un recorte central superior fijo. Si el rostro/texto está en otra zona, inspeccionar el PNG completo a tamaño original. La columna original está ampliada por vecino cercano solo para visualización, claramente rotulada; las otras columnas son los MP4 realmente codificados a 1080p.

## Calidad y conservación

`fast`: Lanczos, sin inferencia. `quality`: Real-ESRGAN x4plus ×4, Lanczos a geometría final, mezcla **65 % Lanczos + 35 % IA** por defecto. `--ai-strength 1` permite IA sin mezcla; no es el valor recomendado sin revisión. No se añade grano. `--sharpness 0` no aplica nitidez extra; valores mayores usan unsharp solo de luminancia.

No se fuerza `-r` ni se añaden cuadros. El preset conserva FPS racionales, número de cuadros y tiempos de comienzo; valida H.264, yuv420p, AAC, duración, color declarado y sincronía por timestamps. Audio AAC-LC se copia; otros códecs se convierten a AAC-LC conservando tasa/canales cuando el codificador puede representarlos. No se usa `-shortest`, que podría cortar audio. Los perfiles/channel layouts no admitidos fallan en lugar de silenciarse.

Se rechaza HDR para no introducir tone mapping inadvertido y SAR distinto de 1:1 para no deformar geometría. Se detecta rotación; el escalado autorrota al extraer/filtrar. El preset siempre produce 1080×1920, con bandas para otras proporciones. No recorta caras para llenar pantalla. El camino IA requiere CFR; para VFR usar `fast` y comprobar la validación de tiempos antes de entregar. No se afirma compatibilidad universal con contenedores dañados, pistas auxiliares o metadatos privados.

El respaldo se deduplica por SHA-256 y se verifica. La salida y su informe/log deben tener nombres nuevos. Los errores de ejecución quedan en `.log`, los de preflight en stderr y los de lote también en su resumen JSON. Tras verificar, la publicación usa creación exclusiva. Los temporales propios se eliminan comprobando su ruta absoluta; usar `--keep-work` para retenerlos.

La IA no conoce la identidad ni la grafía original. Puede alisar piel, cambiar ojos/letras o introducir variaciones entre cuadros. Una comparación de tres imágenes no certifica todo el movimiento. Los aumentos de resolución no revierten defectos de una restauración previa.

## Pruebas

```powershell
& tmp/upscale-ai/.venv/Scripts/python.exe -m unittest discover -s skills/video-upscale-ai/tests -v
```

Las pruebas de integración necesitan FFmpeg/FFprobe. La prueba real de GPU se ejecuta con `doctor --test-engine`. Los resultados medidos y la selección de la muestra están en `plans/video-upscale-ai.md`.
