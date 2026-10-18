# Consentimiento y uso de voces clonadas

> Reglas del laboratorio para cualquier herramienta de clonación, doblaje o síntesis de voz (VoiceStudio, ElevenLabs, o la que venga). No es asesoramiento legal: para uso comercial, consultá a alguien con matrícula.

## Principio

**Una voz es de la persona que la habla.** Clonarla sin permiso es suplantación, aunque el audio se genere en tu propia máquina y aunque no se publique.

## Reglas

### 1. Solo voces propias o con permiso verificable

| Caso | Permitido | Requisito |
|---|---|---|
| Tu propia voz | Sí | Registro de consentimiento propio |
| Voz de otra persona | Solo con permiso | Consentimiento escrito, con alcance y fecha |
| Famosos / figuras públicas | **No** | Ni con fines humorísticos o educativos, salvo revisión legal explícita |
| Menores | **No** | Sin excepciones |
| Voces de clientes | Solo con contrato | El contrato debe cubrir síntesis y uso comercial |
| Voces de personas fallecidas | **No** | Requiere autorización de herederos y revisión legal |

### 2. Consentimiento con alcance

Un "sí" verbal no alcanza. El consentimiento tiene que decir:

- Quién autoriza (nombre y documento).
- Qué voz autoriza (clip de referencia identificado).
- Para qué se usa (interno, redes, publicidad, doblaje).
- Dónde se va a publicar (plataformas).
- Por cuánto tiempo.
- Cómo se revoca.

Si el uso cambia, se pide de nuevo.

### 3. Divulgación

- El audio sintético se declara cuando la plataforma lo exige o cuando alguien podría confundirlo con una grabación real.
- No se presenta una voz clonada como declaración real de la persona.
- En contenido público, dejar claro que la voz es generada si hay duda razonable.

### 4. Usos prohibidos

- Suplantar identidad para pedir dinero, datos o acceso.
- Contenido sexual o violento con la voz de alguien.
- Acoso, difamación, desinformación.
- Hacer pasar una opinión inventada por una declaración real.
- Clonar la voz de un cliente para usos que el contrato no cubre.

### 5. Almacenamiento de los clips

- Los clips de referencia van **fuera del repo**, en una carpeta privada (`%USERPROFILE%\voces\`).
- Nunca se commitean audios, transcripciones de referencia ni perfiles de voz.
- Se guarda el mínimo necesario: un clip limpio por voz, no diez.
- Al terminar el proyecto, se borra el clip y el perfil, y se anota la fecha.
- La transcripción exacta del clip se guarda junto al audio, no en el repo.

### 6. Seguridad

- El MCP de VoiceStudio escucha solo en loopback. No exponerlo a la red sin PIN y TLS.
- No compartir perfiles de voz ni la carpeta de datos de la app.
- Si se usa un proveedor en la nube para doblaje o traducción, el texto (y a veces el audio) sale de la máquina: eso se avisa y se elige a conciencia.

### 7. Revocación

Si alguien retira el permiso:

1. Borrar el perfil de voz y los clips.
2. Bajar de las plataformas el contenido que la use.
3. Anotar la revocación y la fecha.
4. No volver a clonar esa voz.

## Registro de consentimiento

Copiar esta tabla a un archivo privado por cada voz. No vive en el repo.

| Campo | Valor |
|---|---|
| Persona que autoriza | |
| Documento / contacto | |
| Voz (archivo de referencia) | |
| Fecha del consentimiento | |
| Uso autorizado | |
| Plataformas | |
| Vigencia | |
| Secreto / restricciones | |
| Revocación (fecha y medio) | |
| Firmante | |

## Checklist antes de generar

- [ ] La voz es mía o tengo consentimiento escrito
- [ ] El consentimiento cubre **este** uso y **esta** plataforma
- [ ] El clip de referencia está fuera del repo
- [ ] Sé dónde se va a publicar y cómo se declara
- [ ] No estoy suplantando a nadie
- [ ] Sé cómo borrar el perfil si me lo piden

## Qué debe hacer un agente

Si un pedido implica clonar una voz sin consentimiento verificable, el agente:

1. No ejecuta la clonación.
2. Explica qué falta (permiso, alcance, registro).
3. Ofrece alternativas: voz sintética genérica, voz propia, o pedir el permiso.

## Marco legal (referencia, no asesoramiento)

- **Datos personales:** la voz puede ser dato personal y, en algunos usos, dato biométrico. Aplica GDPR en la UE y leyes equivalentes en otros países.
- **Transparencia de IA:** las normas europeas de IA exigen identificar contenido sintético en ciertos casos. Verificar el estado vigente antes de publicar.
- **Derecho de imagen y voz:** muchas jurisdicciones protegen la voz como atributo de la personalidad.
- **Licencias de modelos:** los pesos de los motores TTS pueden limitar el uso comercial. Revisar cada motor.
- **AGPL-3.0 (VoiceStudio):** usar la app localmente no obliga a publicar nada; distribuir una versión modificada sí.

Ante duda legal, se frena la publicación, no la clonación... y se consulta.
