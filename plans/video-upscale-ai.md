# Spec: video-upscale-ai

Base: `templates/spec.md`. Fuente: solicitud directa y repositorios indicados, no un video educativo.

## 1. PRD — requisitos de producto

Instalar una skill local para Codex y OpenCode que mejore videos autorizados de HeyGen exportados a 720p. Modos rápido Lanczos y calidad Real-ESRGAN, preset youtube-shorts-1080p, nitidez controlable, lotes, comparaciones y validación. Para 720×1280 producir exactamente 1080×1920. No prometer detalles recuperados, no usar embellecimiento facial, no interpolar FPS. Éxito: ejecutar ambos modos en un clip real, revisar el resultado y registrar la elección visual antes de cualquier procesamiento completo.

## 2. TRD — requisitos técnicos

Python >=3.11, FFmpeg/FFprobe, Pillow para comparación, ejecutable oficial Real-ESRGAN ncnn/Vulkan y sus modelos. Adaptación de `pangpang778/real-esrgan-skill` (MIT), conservando licencia/atribución; no ejecutar su instalador global ni el fallback a un proxy. Evaluar Gladgithub como referencia de mezcla con Lanczos, sin adoptar grano automático ni modelo anime para rostros reales. Video2X se evalúa como alternativa, no se incorpora su código.

Real-ESRGAN x4plus tiene factor nativo ×4; procesar ×4 y reducir con Lanczos a 1080×1920. Mezcla conservadora configurable entre Lanczos y IA para evitar aspecto plástico, nitidez cero por defecto. Conservar FPS racional, colores SDR y audio AAC existente; otros códecs de audio se convierten a AAC. H.264 yuv420p, referencia de 8 Mbps a 24–30 FPS y 12 Mbps a 48–60 FPS. Rechazar HDR o tiempos variables no soportados por el camino IA con error explícito. Detectar orientación/rotación, sin recortar contenido para llenar Shorts.

## 3. Flujo de la app

Doctor → inspección → clip corto en ambos modos → imágenes comparativas → selección visual con razón → procesamiento o lote autorizado → FFprobe/decodificación/hashes → salida nueva e informe. Fallas por archivo en lote. No fallback silencioso de IA a Lanczos. No hay publicación ni subida a YouTube.

## 4. Brief de diseño

CLI y JSON, logs por trabajo y comparativas con rótulos claros a tamaño equivalente. No se necesita interfaz gráfica, paleta ni tipografía de producto. Priorizar inspección de ojos, boca, cabello, letras y movimiento. No usar una métrica de nitidez aislada como prueba de naturalidad.

## 5. Esquema del backend

Sin servidor, cuenta ni base de datos. Archivos fuente, copia de respaldo por hash, resultado, informe JSON, log y previews PNG. Ejecutables/pesos y pruebas reales en `tmp/upscale-ai/`, ignorado por Git. Copias instalables en `.agents/skills/video-upscale-ai/` y `.opencode/skills/video-upscale-ai/`; fuente mantenida en `skills/video-upscale-ai/`. Rutas del proyecto relativas y opciones explícitas para herramientas externas.

## 6. Plan de implementación

1. Revisar fuentes/licencias y medir Vulkan con una inferencia real pequeña.
2. Implementar doctor, probe, run, compare, preview y batch en Python, más instalación PowerShell sin depender de Bash.
3. Implementar preset, conservación de tiempos/audio/color, respaldo, publicación exclusiva, logs y validación.
4. Crear pruebas de comportamiento con clips sintéticos y ejecutar ambos modos en un clip corto de Vale; revisar comparación visual y registrar selección.
5. Validar la skill, instalar las copias del proyecto y actualizar índices.

Aceptación: dimensiones exactas, FPS sin interpolación, H.264/yuv420p/AAC, entrada y respaldo intactos, errores claros, comprobación real del motor y comparación antes/después. Rollback: conservar originales y trabajos previos; retirar únicamente archivos nuevos identificados. No se promete tiempo de inferencia sin medir en esta GPU. No se procesan videos completos antes de revisar la muestra.

## Resultados medidos

Se leyeron SKILL.md, script Bash, instalador y licencia de pangpang778, más código/licencia de Gladgithub y licencia/README de Video2X. Commits y atribuciones quedan en `skills/video-upscale-ai/references/attribution.md`. El instalador upstream no se ejecutó. Se conserva MIT y los avisos completos de los componentes.

Vulkan 1.4.321 disponible; se enumeraron AMD integrada (índice 0) y RTX 4050 Laptop (índice 1). Se seleccionó NVIDIA, y `doctor --test-engine` produjo una imagen real 16×16→64×64 con x4plus. FFmpeg/FFprobe 9.0.2 detectados. Runtime propio Python 3.11.15/Pillow 12.3.0, sin PyTorch/CUDA para inferencia. ZIP oficial de 45.474.481 bytes con SHA-256 fijado y verificado; bootstrap/extracción probado también con caché nueva y el mismo ZIP.

Prueba real sobre dos segundos (50 cuadros) del video de Vale previamente restaurado: Lanczos tardó 1,39 s y Real-ESRGAN ×4 con mezcla al 35 % tardó 263,53 s. Ambos exportaron exactamente 1080×1920, 25 FPS, 50 cuadros, H.264/yuv420p y AAC. Checks de decodificación, duración, inicios, audio, respaldo y original intacto aprobados. No se procesó un video completo con superresolución en esta entrega; se cumple la prueba corta previa solicitada. Una extrapolación lineal en esta configuración sería unos 57 minutos para 652 cuadros, no una garantía de tiempo.

Se inspeccionaron los cuadros 0, 25 y 49 a escala equivalente, incluyendo recortes del rostro. Selección para esta muestra: `quality`, 35 % IA y 65 % Lanczos, nitidez extra 0. Se aprecia algo más de definición en gafas/cabello/contornos, con ligero alisado de piel; no se observa una deformación facial evidente en esas muestras. Es una valoración visual local, no una validación de todos los cuadros ni prueba de recuperación de detalle verdadero. No se afirma que se haya visto toda la secuencia en reproducción continua.

Prueba sintética adicional con títulos, texto pequeño de 18 px, símbolos 0/O/1/I y barras de color: ambos métodos mantienen los rótulos legibles en la imagen comparada. Se elige Lanczos para esa placa por fidelidad suficiente y menor coste; no se generaliza a toda tipografía. Los PNG y clips de ambas comparaciones quedan en `tmp/upscale-ai/vale-compare/` y `tmp/upscale-ai/text-compare/`, ignorados por Git. Las decisiones se registran en sus `preview/comparison.json`.

Suite: 10 pruebas aprobadas, incluida inferencia Vulkan real con color etiquetado y timestamps no nulos, FPS 30000/1001, audio idéntico cuando se copia, respaldos, Unicode, sobrescritura, archivo dañado, rechazo HDR/VFR no soportado en IA, lotes con errores y previews. El validador oficial de skills aprobó nombre/frontmatter. Se instala la skill en `.agents/skills/video-upscale-ai/` y `.opencode/skills/video-upscale-ai/` del proyecto; el entorno de ejecución protege esas carpetas y requirió permiso de escritura para la instalación, sin cambios globales.

No se actualiza `videos/INDEX.md`: los repos se usan como fuente técnica y los clips como material de prueba, no como videos educativos para transcribir/fichar. Se actualizan los índices de skills y planes.
