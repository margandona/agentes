# Campos, instalación y limitaciones

## Dependencias

Python >=3.11, FFmpeg con FFprobe y ExifTool en PATH. No se requieren paquetes Python para ejecutar los scripts.

- Windows: `winget install Python.Python.3.13`, `winget install Gyan.FFmpeg`; descargar ExifTool desde https://exiftool.org/ e instalar según sus instrucciones de Windows (conservar sus archivos auxiliares y renombrar el ejecutable a `exiftool.exe`). Abrir otra consola y comprobar `python --version`, `ffmpeg -version`, `ffprobe -version`, `exiftool -ver`.
- macOS con Homebrew: `brew install python ffmpeg exiftool`.
- Debian/Ubuntu: `sudo apt install python3 ffmpeg libimage-exiftool-perl`; usar `python3` >=3.11.

## Categorías

| Categoría | Ejemplos reconocidos | Tratamiento |
|---|---|---|
| personal | Artist, Author, Creator, OwnerName, SerialNumber, Email | Eliminación seleccionable |
| location | GPS*, Location, City, Country | Eliminación seleccionable |
| software | Software, Encoder, CreatorTool, WritingApp, MuxingApp | Eliminación seleccionable; valores pueden mencionar herramientas de IA |
| dates | CreateDate, ModifyDate, DateTimeOriginal, creation_time | Eliminación seleccionable; no altera fechas del sistema de archivos |
| provenance | Copyright, Rights, C2PA, JUMBF, Manifest, firmas | Bloquea saneamiento, no se altera |
| structural / other | Dimensiones, códecs, perfiles, orientación, campos desconocidos | Se conservan cuando el procesador puede representarlos |

No hay borrado global `-all=` ni `-map_metadata -1`. FFmpeg elimina tags expuestos seleccionados; ExifTool elimina campos concretos en imágenes. El verificador rechaza metadatos seleccionados que permanecen, salvo fechas cero estructurales. Un muxer puede regenerar software o fechas; se informa la falla y se descarta el temporal.

## Integridad y procedencia

Se comprueba formato real, duración (tolerancia 0,1 s), flujos, códecs, dimensiones, audio, disposiciones y hashes audiovisuales decodificados con FFmpeg `-xerror`. No es una auditoría forense exhaustiva del contenedor. Un remux puede perder campos privados, índices, adjuntos no representables o firmas no detectadas; los informes muestran diferencias de campos visibles. Se rechaza cambiar de formato.

ExifTool y FFprobe no exponen todos los campos. El escaneo incremental de marcadores C2PA/JUMBF es conservador y puede producir falsos positivos. No autentica credenciales, no descubre todas las firmas ni certifica ausencia de IA. Copyright/autoría protegida detectada bloquea también el saneamiento. No se editan marcas visuales, patrones internos ni contenido audiovisual.

En MP4/MOV con estructura BMFF válida y `ftyp` inicial, se escanean las cajas fuera de `mdat`, donde están las muestras comprimidas. Se reconoce también el UUID binario C2PA `d8fec3d6-1b0e-483c-9297-5828877ec481`, incluso sin texto legible. Si la estructura es irregular, se vuelve al escaneo conservador de todos los bytes. Esto evita confundir coincidencias aleatorias en H.264 con credenciales. No valida referencias remotas ni constituye una validación criptográfica. Fuente: [C2PA 2.2, apéndice A.5](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html).

Las imágenes se editan con ExifTool sin recomprimir; su soporte de escritura por tag/formato puede variar. Una operación no soportada falla o deja campos residuales: no se publica en ese caso. Datos originales con advertencias o estructuras no estándar requieren revisión individual.

Procesamiento local con timeout de cinco minutos por comando; archivos grandes pueden requerir más tiempo y fallarán claramente. Batch procesa todos los archivos regulares del árbol y registra formatos incompatibles como fallas. No sigue enlaces simbólicos de archivos. No se admite un directorio de salida dentro del de entrada ni a la inversa.

Los informes contienen datos originales potencialmente sensibles. `--verbose` muestra comandos y rutas en stderr. No distribuir informes sin revisarlos.

## Fuentes oficiales consultadas

- [FFmpeg](https://ffmpeg.org/ffmpeg.html): streamcopy, selección explícita de flujos y tags.
- [ExifTool](https://exiftool.org/): instalación, lectura y escritura de metadatos (el acceso automatizado al manual devolvió 403 durante esta tarea).
- [OpenCode Agent Skills](https://opencode.ai/docs/skills/): formato y descubrimiento en `.opencode/skills/`.
