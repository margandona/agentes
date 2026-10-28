# Antes de empezar

Este laboratorio es un taller. Entra un video de YouTube y sale una receta: un papel que dice qué pasos seguir para hacer algo. También entran fotos y videos para limpiarlos, agrandarlos o quitarles una marca.

La idea es simple: nada se cree porque lo dijo un video. Primero se lee, se anota y se prueba. Si no se prueba, no se usa.

El camino de un video es siempre el mismo:

- Paso 1: entra el video.
- Paso 2: se copia todo lo que se dice, con la hora exacta.
- Paso 3: se llena una ficha con lo importante.
- Paso 4: sale una receta (skill) o un plan de trabajo.

> Una skill es como una receta de cocina: dice qué hacer y en qué orden. No cocina sola. La sigue un robot, que en este caso soy yo.

# 1. Las recetas (skills)

## six-docs-before-build
**Es como** hacer los planos de una casa antes de poner los ladrillos.
**Sirve para** que el robot no improvise y sepa qué construir.
**Lo usás cuando** empezás una app, un agente o algo grande desde cero.

## agent-with-memory-and-tools
**Es como** un ayudante que anota todo en una libreta y además tiene manos para hacer cosas.
**Sirve para** que un chat no olvide la conversación y pueda mandar un mensaje o buscar un dato.
**Lo usás cuando** querés un bot de WhatsApp o Telegram que recuerde y actúe.

## resume-optimization-prompts
**Es como** un profesor que te ayuda a ordenar tu currículum para el trabajo que querés.
**Sirve para** mostrar tus logros de verdad, sin inventar nada.
**Lo usás cuando** te postulás a un trabajo y querés que te lean.

## media-metadata-sanitizer
**Es como** borrar la etiqueta con tu nombre y tu dirección de una foto antes de regalarla.
**Sirve para** que un archivo no cuente de más: dónde se sacó, con qué celular o quién lo hizo.
**Lo usás cuando** vas a publicar fotos o videos y no querés dejar datos personales.

## video-watermark-restoration
**Es como** sacar un sticker pegado en una foto, pero en un video.
**Sirve para** borrar una marca o un texto fijo que tapa parte de la imagen.
**Lo usás cuando** el video es tuyo o tenés permiso, y la marca molesta.

## video-upscale-ai
**Es como** agrandar una foto sin que se vea borrosa.
**Sirve para** pasar un video a 1080p o prepararlo para YouTube Shorts.
**Lo usás cuando** el video se ve chico o con pocos detalles.

## video-a-skill
**Es como** la receta principal del taller: agarra un video y lo convierte en apuntes y recetas.
**Sirve para** no perder lo que enseña un video y poder repetirlo cuando quieras.
**Lo usás cuando** pasás un link de YouTube y querés aprender de verdad.

## agent-reach
**Es como** los ojos y los oídos del robot en internet.
**Sirve para** buscar y leer en YouTube, X, Reddit, GitHub y páginas web.
**Lo usás cuando** hace falta un dato que no está en el repo.

# 2. Las herramientas del taller (scripts)

Son programas chiquitos que hacen una tarea aburrida y repetida. Están en la carpeta tools.

## transcript.py
**Es como** un cuaderno que copia todo lo que se dice en un video.
**Sirve para** bajar el texto y los datos del video a una carpeta.
**Lo usás cuando** empieza el camino de un video nuevo.

## triage.py
**Es como** mirar la tapa y la contratapa de un libro antes de leerlo.
**Sirve para** decidir rápido si un video vale la pena.
**Lo usás cuando** tenés muchos links y no sabés por cuál empezar.

## download-heygen.py
**Es como** pedirle el video a una página con la llave correcta.
**Sirve para** bajar un video de HeyGen que la página no deja bajar de otra forma.
**Lo usás cuando** el video que necesitás vive en HeyGen.

## doctor.ps1
**Es como** el chequeo del médico: dice qué está sano y qué falta.
**Sirve para** revisar si están Python, yt-dlp, FFmpeg, Node, Git, GitHub, Ollama y la skill agent-reach.
**Lo usás cuando** algo no funciona y no sabés por qué.

## yt-dlp.cmd
**Es como** un atajo para llamar al mismo ayudante de siempre.
**Sirve para** usar yt-dlp cuando el comando normal no aparece.
**Lo usás cuando** querés bajar un video a mano.

# 3. Las manos del robot (herramientas del agente)

Para hacer todo esto yo necesito ojos, manos y un cuaderno. Estas son mis partes.

## Ojos
**Es como** una linterna que alumbra un archivo o una palabra.
**Sirve para** leer archivos y encontrar cosas: read, glob y grep.
**Lo usás cuando** hay que mirar qué dice una ficha o dónde está un nombre.

## Manos
**Es como** un lápiz y un destornillador.
**Sirve para** crear archivos, corregirlos y apretar botones: write, edit, shell y execute.
**Lo usás cuando** hay que escribir una receta o correr un programa.

## Ventana al mundo
**Es como** un telescopio y un teléfono.
**Sirve para** mirar una página o buscar algo: webfetch y websearch.
**Lo usás cuando** hay que comprobar un dato fuera del repo.

## Ayudantes
**Es como** un manual de instrucciones, un compañero y una libreta de tareas.
**Sirve para** cargar una skill, pedir ayuda a otro agente o anotar los pasos.
**Lo usás cuando** el trabajo es largo o necesita más de una cabeza.

## image-lab
**Es como** una caja de crayones y un ayudante que dibuja lo que le pedís.
**Sirve para** hacer íconos sin internet y, si hay una clave, imágenes con IA.
**Lo usás cuando** necesitás una imagen para una guía, un video o una app.

# 4. Las máquinas (software externo)

Estas no las hice yo. Son programas que ya existían y que el taller usa.

## Python y Node.js
**Es como** los dos idiomas en los que están escritas las herramientas.
**Sirve para** que los scripts y las páginas puedan funcionar.
**Lo usás cuando** corrés cualquier cosa del taller.

## Git y GitHub CLI
**Es como** una máquina del tiempo y un cartero.
**Sirve para** guardar versiones del trabajo y hablar con GitHub.
**Lo usás cuando** querés volver atrás o publicar cambios.

## yt-dlp
**Es como** el bajador oficial de videos.
**Sirve para** traer el video, los datos y los subtítulos.
**Lo usás cuando** llega un link de YouTube.

## uv
**Es como** el armador de cajas de herramientas.
**Sirve para** crear entornos limpios con la versión de Python que haga falta.
**Lo usás cuando** una herramienta necesita sus propias piezas.

## FFmpeg
**Es como** la navaja suiza del video.
**Sirve para** cortar, pegar, cambiar de formato y sacar fotos de un video.
**Lo usás cuando** hay que tocar un video de verdad.

## ExifTool
**Es como** el detective de etiquetas escondidas.
**Sirve para** leer y borrar los datos que traen las fotos y los videos.
**Lo usás cuando** hay que limpiar la privacidad de un archivo.

## Playwright
**Es como** un robot que usa un navegador igual que una persona.
**Sirve para** entrar a una página, hacer clics y bajar lo que hay.
**Lo usás cuando** una página no deja bajar las cosas de otra manera.

## Ollama
**Es como** un cerebro que vive dentro de tu computadora.
**Sirve para** hablar con modelos de IA sin internet y sin pagar por mensaje.
**Lo usás cuando** querés probar una IA local.

## Real-ESRGAN
**Es como** el agrandador mágico.
**Sirve para** hacer más grande un video y que no se vea borroso.
**Lo usás cuando** elegís la opción de calidad al agrandar.

## ProPainter
**Es como** el borrador inteligente.
**Sirve para** rellenar el hueco que deja una marca en un video.
**Lo usás cuando** la marca está sobre algo que se mueve.

## Torch, Pillow y Tkinter
**Es como** el motor, los pinceles y la ventana con botones.
**Sirve para** que la IA funcione, para dibujar máscaras y para armar la interfaz.
**Lo usás cuando** abrís Video Studio.

# 5. Los enchufes (servicios)

Son puertas que se abren en tu computadora para que dos programas se hablen.

## OpenCode
**Es como** la puerta para hablar conmigo.
**Sirve para** abrir la misma sesión en la terminal o en el navegador.
**Lo usás cuando** querés pedirme algo.

## Ollama
**Es como** la puerta del cerebro local.
**Sirve para** que otros programas le pregunten cosas a los modelos.
**Lo usás cuando** una herramienta necesita IA sin internet.

## VoiceStudio
**Es como** la puerta de la voz.
**Sirve para** clonar una voz, hablar, transcribir y escuchar.
**Lo usás cuando** la app está abierta y querés usarla desde otro programa.

# 6. La máquina grande

## Video Studio
**Es como** una máquina con botones para tres trabajos: limpiar, agrandar y borrar etiquetas.
**Sirve para** hacer todo eso con una ventana, sin escribir comandos.
**Lo usás cuando** preferís ver el video y pintar la marca con el mouse.

# 7. Lo que miramos pero no compramos

- **Gemini API**: sirve para leer videos sin bajarlos, pero todavía es solo un plan.
- **VoiceStudio por enchufe**: se puede conectar, pero todavía no está conectado.
- **Open WebUI, Continue, LM Studio, llama.cpp y vLLM**: son otras formas de usar IA local. Están anotadas, no instaladas.
- **LTX Desktop**: hace videos con IA, pero pide una placa de video mucho más grande. Acá no entra.

# 8. Tres reglas para no olvidar

- Ninguna cosa entra sin una fuente: un video, un link o una prueba.
- Si no se probó, no se cree. Va a la lista de dudas.
- Cada video deja un rastro: datos, texto, ficha y receta. Así se puede volver.

> Si algo no funciona, no adivines: primero corré doctor.ps1. Ese chequeo dice qué pieza falta.

## Cómo pedir algo
**Paso 1** decime qué querés hacer, con tus palabras.
**Paso 2** te digo qué receta o herramienta lo resuelve.
**Paso 3** lo hacemos y lo probamos antes de darlo por bueno.

# 9. La chuleta: si querés, pedí

| Quiero... | Usá... |
|---|---|
| Entender un video de YouTube | video-a-skill |
| Buscar algo en internet | agent-reach |
| Saber si un video vale la pena | triage.py |
| Bajar un video de HeyGen | download-heygen.py |
| Sacar una marca de agua | video-watermark-restoration |
| Agrandar un video | video-upscale-ai |
| Borrar etiquetas de una foto | media-metadata-sanitizer |
| Mejorar mi currículum | resume-optimization-prompts |
| Empezar una app sin improvisar | six-docs-before-build |
| Un bot que recuerde y actúe | agent-with-memory-and-tools |
| Probar una IA en mi compu | Ollama |
| Clonar una voz | VoiceStudio |
| Saber si todo anda | doctor.ps1 |
| Hacerlo con botones | Video Studio |

> Si algo de esta guía no se entiende, pedime que lo explique con otro ejemplo. La idea es que se entienda, no que suene técnico.
