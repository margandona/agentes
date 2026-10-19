# Video Studio

Abrir con doble clic en **Abrir Video Studio.cmd**, en la raíz del proyecto. Es una aplicación local de Windows, sin servidor ni subida de videos. Usa el entorno Python/Tkinter/Pillow y las herramientas ya instaladas para las skills. Desde PowerShell también: `& .\tmp\watermark\.venv\Scripts\python.exe .\apps\video-studio\app.py`.

1. Añadir uno o varios videos. Seleccionar un archivo muestra su primer fotograma y características.
2. Para quitar marcas, activar esa operación y pintar en naranja las marcas en la vista previa. Usar el borrador para corregir; también se puede importar una máscara PNG en blanco y negro del tamaño del video. Blanco indica la región a reconstruir. Cada video tiene su propia máscara; revisar que cubra marcas fijas durante todo el clip. No admite seguimiento de marcas móviles.
3. Elegir 1080p rápido (Lanczos) o calidad (Real-ESRGAN), y nitidez opcional. La IA puede tardar minutos por fragmento. No se aplica embellecimiento facial. Activar metadatos para sanear al final.
4. Elegir carpeta y **Probar 2 segundos** sobre el video seleccionado. **Comparar Lanczos / IA** produce dos clips y PNG comparativas en la carpeta comparacion/preview. Abrir resultados para revisarlos; no se elige automáticamente una supuesta mejora.
5. Tras revisar, **Procesar lote** aplica las opciones a todos los archivos de la lista. Cancelar detiene el árbol del trabajador y conserva parciales.

Cada ejecución tiene una carpeta nueva, copia original por video, salidas intermedias, resumen.json y registro .log junto al JSON del trabajo. Los resultados anteriores no se sobrescriben. Las limitaciones de FPS entero/CFR de ProPainter y los rechazos de HDR/VFR de la skill de calidad siguen vigentes; aparecen como errores, sin convertir silenciosamente el material.

Requisitos existentes: tmp/watermark/.venv (Python 3.11, Pillow, Torch), tmp/watermark/ProPainter con pesos, FFmpeg/FFprobe y ExifTool en tmp/media-tools; Real-ESRGAN Vulkan en tmp/upscale-ai/engine para calidad. La interfaz no instala ni descarga modelos. ProPainter conserva su licencia S-Lab no comercial: consultar las atribuciones de la skill antes de uso comercial.

La restauración genera video H.264; la operación de escalado garantiza MP4 H.264 yuv420p/AAC según su validador. El saneamiento conserva el contenido y puede bloquear archivos con procedencia protegida. Una máscara equivocada puede alterar detalles: revisar siempre la muestra.
