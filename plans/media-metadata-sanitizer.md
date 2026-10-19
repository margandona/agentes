# Spec: media-metadata-sanitizer

Base: `templates/spec.md`. Fuente: solicitud adjunta del usuario; no deriva de un video.

## 1. PRD — requisitos de producto

Inspeccionar, sanear categorías elegidas, verificar y procesar lotes de multimedia autorizada. Mantener originales y producir JSON. Admitir MP4, MOV, MKV, WEBM, JPEG, PNG y WEBP según contenido real. Éxito: remoción comprobable de campos seleccionados sin recomprimir y sin publicar salidas inválidas.

Fuera de alcance: atribución de origen humano, detección universal de IA, eliminación de marcas visuales, edición de credenciales y conversión entre contenedores.

## 2. TRD — requisitos técnicos

Python >=3.11, biblioteca estándar, FFprobe/FFmpeg y ExifTool en PATH. Subprocess sin shell, timeout y errores legibles. ExifTool determina tipo real; FFprobe informa estructura. Videos: copia de flujos y borrado explícito de tags seleccionados. Imágenes: edición selectiva con ExifTool sobre copia temporal. Rechazar indicios de procedencia protegida antes de editar. Publicación exclusiva sin sobrescritura; verificación previa a publicar.

## 3. Flujo de la app

CLI: entrada → inspección → selección de categorías → temporal → verificación → salida nueva + JSON. `--dry-run` inspecciona sin escribir. VERIFY devuelve estado fallido ante pérdida de estructura o errores de decodificación. BATCH recorre un listado inicial y registra fallas por archivo; salida fuera del árbol de entrada.

## 4. Brief de diseño

Interfaz de consola: JSON UTF-8 en stdout, diagnósticos en stderr y códigos 0/1. No hay pantallas, colores ni tipografías: son inaplicables a esta herramienta CLI. Argumentos comunes y ayuda en español.

## 5. Esquema del backend

No requiere servidor, autenticación ni base de datos: procesamiento local. Informes con ruta, SHA-256, formato, metadatos clasificados, estructura y diferencias. Los informes pueden contener datos personales; el usuario decide dónde guardarlos. Solo se leen archivos explícitos o del directorio solicitado.

## 6. Plan de implementación

1. Crear núcleo común y cuatro CLI independientes.
2. Documentar categorías, límites, dependencias e instalación Codex/OpenCode.
3. Crear pruebas unitarias y fixtures sintéticos con FFmpeg/ExifTool; saltar integración explícitamente si faltan binarios.
4. Ejecutar validación disponible, actualizar índices y registrar resultados reales.

Criterios: originales intactos, selección explícita de campos, Unicode, JSON consistente, rechazo de credenciales detectadas, archivos dañados y salidas existentes. Rollback: retirar únicamente archivos nuevos de esta entrega; no tocar multimedia del usuario. Sin estimación temporal contractual.

## Fuentes técnicas

- https://ffmpeg.org/ffmpeg.html — streamcopy, map y metadata.
- https://exiftool.org/ExifTool.html — lectura y escritura de tags.
- https://opencode.ai/docs/skills/ — descubrimiento de skills del proyecto.

## Resultados

Validación en Windows (2026-10-18): Python 3.14.6 disponible mediante instalación uv, fuera del PATH habitual. Seis pruebas unitarias aprobadas; cuatro pruebas de integración omitidas explícitamente porque faltan FFmpeg, FFprobe y ExifTool en PATH. Las cuatro pruebas de integración cubren los siete formatos, archivos dañados, extensión engañosa, Unicode, integridad y cambios de contenido.

El validador oficial `quick_validate.py` se intentó ejecutar y no pudo iniciarse por falta del paquete PyYAML. No se atribuye una aprobación a ese validador. Se comprueban localmente nombre, frontmatter, archivos requeridos y enlaces. La descarga local de FFmpeg se intentó, pero la red del entorno no permitió conectar con el servidor; no se instalaron binarios del sistema.

No se agrega una ficha ni entrada en `videos/INDEX.md`: no se recibió ningún video. Los índices de skills y planes sí se actualizan. La copia instalable OpenCode se prepara con el instalador local; no se modifica configuración global.

Copia OpenCode instalada y comparada byte a byte con la fuente (excluyendo cachés). Sintaxis de todos los scripts, frontmatter básico y enlaces relativos verificados. `git diff --check` sin errores. La política de PowerShell requiere `-ExecutionPolicy Bypass` para esta invocación puntual del instalador; no se cambia la política permanente del equipo.

### Corrección detectada con el video de Vale

El escaneo de bytes encontró `C2PA` en el offset 1.708.101, dentro de un NAL H.264 tipo 1 del paquete de video situado en 1.706.332. No era una caja de credenciales: las cajas principales eran `ftyp`, `free`, `mdat`, `moov`, sin campos de procedencia expuestos por ExifTool. Se reprodujo el falso positivo con una prueba sintética antes de corregirlo.

Ahora se escanean cajas fuera de `mdat` en archivos BMFF de estructura íntegra y se reconoce el UUID binario oficial C2PA. Estructuras desconocidas o dañadas mantienen el escaneo conservador. La regresión comprueba coincidencias aleatorias en media, texto en metadatos, UUID C2PA real y fallback para cajas dañadas. Suite completa: 12 pruebas aprobadas, con FFmpeg/FFprobe/ExifTool disponibles.

### Prueba posterior con video autorizado

Se descargaron FFmpeg/FFprobe y ExifTool 13.59 en `tmp/media-tools/`, sin instalación global. Ejecutadas 11 pruebas: todas aprobadas, incluidas las integraciones de siete formatos y una nueva regresión de AAC con inicio distinto de cero.

La prueba real usó el video «Presentación de Marcos Argandoña en Conciencia Educativa»: MP4, 39,9 s, 720×1280, H.264 + AAC estéreo a 48 kHz. Se detectaron los campos de software `Lavf61.7.100` y `Lavc62.11.100 libx264`, y fechas estructurales en cero. No se detectaron indicios de credenciales protegidas.

El primer intento se descartó correctamente: el reajuste de timestamps durante remux alteraba el audio decodificado. La reproducción sintética confirmó la falla. Se corrigió conservando timestamps con `-copyts`; los hashes de audio y video coinciden. También se normaliza `Extended WEBP`, nombre real informado por ExifTool. Se sincroniza la copia OpenCode.

Salida e informes locales en `tmp/prueba-marcos/` (ignorados por Git). No se transcribe ni se ficha este video: se usa como entrada multimedia para probar saneamiento, no como fuente de conocimiento para el repo. El contenido del video no se interpreta como instrucciones.
