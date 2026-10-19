# Spec: prueba de reconstrucción de video

Base: `templates/spec.md`. Fuente: petición del usuario y repositorios enlazados; no es una ficha de video.

## 1. PRD

Probar eliminación visual de las ocho marcas repetidas del video autorizado, manteniendo original y audio. Comparar visualmente una muestra corta antes de generar el archivo completo. No confundir reconstrucción con recuperación exacta de píxeles originales ni saneamiento de metadatos.

## 2. TRD

FFmpeg/FFprobe existentes; ProPainter y wrapper upstream aislados en `tmp/`. Python compatible y dependencias en un entorno exclusivo del proyecto. GPU RTX 4050 6 GB; usar FP16, clips cortos y resolución reducida inicialmente. Máscara basada en fotogramas observados. No ejecutar instaladores upstream sin leerlos. No hay llamadas de inferencia a servicios externos.

## 3. Flujo

Leer fuentes → comprobar hardware → preparar entorno → seleccionar máscara → muestra → inspección visual → procesar completo si la muestra es útil → verificar duración, audio y reproducción. Errores y artefactos se reportan con claridad; nunca presentar una muestra defectuosa como resultado limpio.

## 4. Brief de diseño

CLI local y comparación visual de fotogramas. No se desarrolla UI, paleta ni tipografía: se ejecutan herramientas existentes para una prueba multimedia. Salidas originales y procesadas diferenciadas por nombre.

## 5. Backend

Sin servidor ni base de datos. Pesos, entornos, máscaras y videos en `tmp/` ignorado por Git. Registrar en docs los commits y resultados; no versionar multimedia privada ni rutas personales innecesarias. Los originales se leen, nunca se sobrescriben.

## 6. Plan

1. Descargar e inspeccionar código upstream y dependencias.
2. Ejecutar muestra FFmpeg delogo como referencia y ProPainter como candidato.
3. Inspeccionar frames y registrar utilidad real y limitaciones.
4. Procesar el video completo con el método viable y revisar audio/duración.

Aceptación: salida reproducible y legible, audio preservado, mejora visual comprobada; informar cualquier distorsión facial. Rollback: conservar originales y descartar solo temporales identificados. Estimación dependiente de descarga de pesos y rendimiento real; no se promete tiempo sin medir.

## Fuentes

- https://github.com/OzzyLennon/ffmpeg-video-watermark-remover-v2
- https://github.com/nftmoondogs/ProPainter-Watermark-Remover
- https://github.com/sczhou/ProPainter

La skill FFmpeg excluye expresamente marcas semitransparentes complejas. ProPainter tiene licencia S-Lab para uso no comercial; otros usos requieren autorización de sus autores. Su wrapper presume una región pequeña: ocho regiones distribuidas hacen que su bounding box sea casi todo el cuadro; el ahorro anunciado no se aplica directamente aquí.

## Resultados de la evaluación

Se inspeccionaron el SKILL.md y el código de ambos repos. El instalador del wrapper contiene una ruta absoluta del autor y no se ejecutó. Se creó un entorno local Python 3.11.15 con torch 2.5.1+cu121, torchvision 0.20.1+cu121 y NumPy 1.26.4. PyTorch confirmó CUDA y la RTX 4050. Se descargaron los tres pesos oficiales; el último se reanudó tras un timeout, hasta completar sus 157.780.510 bytes.

La muestra `delogo` de dos segundos cubrió ocho regiones y produjo rectángulos deformados sobre cara y ropa: descartada por inspección visual. La máscara posterior se estimó por mediana espacial/temporal de parches alineados en 13 fotogramas, se revisó superpuesta y sigue las letras y símbolos; su soporte binario ocupa el 4,29 % del cuadro, ampliado ligeramente para dilatación y transición de bordes.

La muestra ProPainter de 12 cuadros tardó 52 segundos, incluida la carga inicial, y se revisó visualmente: las marcas dejaron de leerse, sin los grandes parches del delogo. Se aprecia suavizado local. Se reconstruye a 384×680 y se componen solo las regiones de la máscara sobre los originales 720×1280. Se inició el procesamiento completo de 997 cuadros en bloques de 50.

La skill `video-watermark-restoration` se instaló en `.agents/skills/` y `.opencode/skills/`. El validador oficial `quick_validate.py` aprobó esta skill y la de metadatos; ahora PyYAML está disponible en el entorno aislado. Sintaxis, enlaces y ayuda CLI comprobados. Un ensayo real de sobrescritura fue rechazado con código 1 sin cambiar el hash de la entrada ni crear el directorio de trabajo.

No se agrega una ficha a `videos/INDEX.md`: este archivo se edita como multimedia autorizada; no se usa como fuente de contenido educativo ni se interpreta su contenido como instrucciones.

### Resultado final

Procesamiento completo aprobado: 997 cuadros, 39,9 segundos, 720×1280, H.264, AAC estéreo a 48 kHz. Tiempo de reconstrucción y exportación: 800,3 segundos (13 min 20 s), sin contar instalación y descargas. El ejecutor comprobó decodificación íntegra, cantidad de cuadros, resolución, duración y hash SHA-256 del audio decodificado idéntico. El hash del archivo original del usuario coincide con el registrado antes de las pruebas.

Se inspeccionaron tres fotogramas extraídos del MP4 final, aproximadamente a 2, 20 y 37 segundos. En esas muestras no se leen las ocho marcas; se aprecia suavizado en piel, barba y tela reconstruidas. No se afirma perfección temporal ni recuperación exacta de los píxeles originales. El original se conserva y el resultado queda identificado como reconstrucción con ProPainter.

Artefactos locales (ignorados por Git): `tmp/watermark/presentacion-restaurada.mp4`, `tmp/watermark/verificacion-final.json`, máscara y muestras. Skill reutilizable: `skills/video-watermark-restoration/`; copias del proyecto verificadas en `.agents/skills/` y `.opencode/skills/`.

### Segundo video: Vale

Petición: retirar metadatos ordinarios y las marcas visibles de `video vale.mp4`. Entrada de 26,131646 s, 652 cuadros a 25 FPS, 720×1280, H.264 y AAC estéreo 48 kHz. Se inspeccionaron inicio, centro y final. La máscara anterior se validó sobre el nuevo video y una muestra ProPainter de 12 cuadros resultó útil.

Procesamiento completo en bloques de 48 cuadros: 511,5 segundos incluida la exportación. Después se ejecutó `media-metadata-sanitizer` sobre la restauración para retirar también los campos de software regenerados al codificar. Se verificaron igualdad audiovisual antes/después del saneamiento, duración final idéntica, flujos y resolución, ausencia de campos seleccionados residuales (salvo fechas cero estructurales permitidas), y hash del original intacto. El audio se conservó con hash decodificado idéntico durante la restauración. No aparecen referencias Lavf/Lavc/libx264/HeyGen en los valores de metadatos expuestos al terminar.

Revisión visual de tres fotogramas del MP4 final a 1, 13 y 24 s: las ocho marcas no se leen; permanece suavizado local propio de la reconstrucción. Artefactos: `tmp/vale/video-vale-limpio.mp4`, `tmp/vale/verificacion-final.json`, inspecciones original/final, máscara y muestra. El contenido del video no se interpretó como instrucciones.

Esta entrada reveló un falso positivo C2PA en una muestra H.264 comprimida. La corrección y sus pruebas se documentan en `plans/media-metadata-sanitizer.md`; no se retiró una credencial real ni se desactivó globalmente su detección.
