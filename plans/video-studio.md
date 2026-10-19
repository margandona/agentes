# Spec: Video Studio local

## 1. PRD — requisitos de producto
Aplicación de escritorio para operar las tres skills existentes sin escribir comandos. Seleccionar varios videos, dibujar o importar una máscara, elegir restauración, escalado y privacidad; probar primero un fragmento y ejecutar un lote. Conservar originales y registrar fallos por archivo. Fuera de alcance: detectar automáticamente logos o prometer una mejora visual.

## 2. TRD — requisitos técnicos
Python 3.11, Tkinter y Pillow del entorno local existente. Trabajador separado con subprocesos sin shell; reutiliza las CLI de las skills. FFmpeg, FFprobe, ExifTool y ProPainter existentes. Sin servidor ni base de datos. Cancelación del árbol de procesos propio en Windows. Orden: restauración, escalado, saneamiento.

## 3. Flujo de la app
Añadir videos → seleccionar uno y revisar fotograma → dibujar/importar máscara si corresponde → elegir operaciones y carpeta → prueba de dos segundos → abrir resultado y revisar → procesar lote. Botones para comparar Lanczos/IA, cancelar y abrir carpeta. Errores quedan visibles en registro y resumen JSON; un archivo fallido no detiene los demás. La máscara es específica de cada video y se comprueba su tamaño.

## 4. Brief de diseño
Mesa de trabajo clara: biblioteca a la izquierda, vista previa central y controles a la derecha. Paleta: fondo #E8EEF4, texto #172C43, acción #067D87, superficie #FFFFFF, secundario #61758A y aviso #D98B27. Títulos Segoe UI Semibold, cuerpo Segoe UI, registro Consolas. Evitar sobrecargar el centro: controles agrupados según el orden real del procesamiento. Verificar mediante captura de la ventana y prueba de controles.

## 5. Esquema del backend
No requiere autenticación ni tablas: archivos locales. Configuración de trabajo JSON con entradas, máscaras, opciones y salida; originales copiados antes del procesamiento; resultados nuevos en subcarpetas únicas. Registro de consola y resumen JSON por ejecución. No se envían videos a servicios externos. Cancelar conserva los parciales para diagnóstico.

## 6. Plan de implementación
1. Crear apps/video-studio con trabajador, interfaz y lanzador Windows.
2. Conectar las CLI y editor de máscaras, prueba corta, comparación y lotes.
3. Probar flujo real rápido y metadatos, editor y ventana; comprobar errores y conservación del original.
4. Documentar uso y actualizar índice. Los seis documentos están aquí reunidos según templates/spec.md. No se modifica videos/INDEX.md: esta tarea crea una aplicación, no una ficha de una fuente audiovisual.

Rollback: retirar únicamente el lanzador y apps/video-studio; ninguna skill existente necesita cambios. Duración variable de IA: mostrar actividad y registro sin porcentajes inventados. Criterio de aceptación: ventana operativa, comandos reales, salida validada por las skills y originales intactos.

### Verificación realizada
Prueba real con clip sintético de ocho cuadros y audio: escalado Lanczos 1080×1920 yuv420p y saneamiento aprobados; SHA-256 del original intacto. Se ejecutó también desde el botón de la interfaz mediante su trabajador separado. Ventana, lectura asíncrona, pincel y limpieza de máscara probados; captura revisada en tmp/video-studio/interfaz.png. Se corrigió la escala para que los botones inferiores permanezcan visibles. La prueba visual de Tk necesitó ejecución fuera del sandbox de herramientas, que impedía cargar Tcl; la aplicación se abre normalmente desde Windows. ProPainter y Real-ESRGAN reutilizan las pruebas reales previas de sus skills; no se repitió una restauración completa desde esta interfaz. Cancelación y comparación están conectadas, pero no se verificaron interactivamente en esta pasada.
