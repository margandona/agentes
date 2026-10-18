# Plan: agente de WhatsApp con Claude Code / OpenCode

- **Origen:** video `videos/vlKWMfbY9BA-construye-un-agente-de-ia-para-whatsapp-en-30-minutos-con-cl/` [00:05]
- **Objetivo:** construir un agente de WhatsApp que hable con clientes, recuerde conversaciones, responda sobre el negocio y ejecute acciones (reservas)
- **No-objetivo:** producción a escala, multi-idioma, pagos dentro del chat
- **Riesgo principal:** datos de clientes sin política de privacidad, y costos de OpenRouter + VPS que se disparan
- **Costo esperado:** $5-20/mes (modelo + hosting), variable según volumen

## Precondiciones

- [ ] Los seis documentos de `skills/six-docs-before-build/` completos (PRD, TRD, flujo, diseño, backend, plan)
- [ ] Cuenta de Meta Developers con app creada
- [ ] Cuenta de OpenRouter con crédito
- [ ] VPS o servicio de hosting
- [ ] Número de WhatsApp Business disponible

## Pasos

### 1. Plan (antes de código)

1. Definir el negocio: qué vende, a quién, qué resuelve el agente.
2. Listar las acciones: consultar disponibilidad, tomar datos, cerrar cita.
3. Dejar que el agente defina la arquitectura.
4. Completar `templates/spec.md`.

**Verificación:** los seis documentos existen y están cerrados.

### 2. Conectar WhatsApp

1. Crear app en Meta Developers.
2. Añadir producto "WhatsApp".
3. Configurar credenciales (token, phone number ID).
4. Configurar webhook (URL pública, verify token).
5. Probar recepción de un mensaje de prueba.

**Verificación:** un mensaje de WhatsApp llega a tu app y se loguea.

**Si falla:** revisar que el webhook sea HTTPS y que el verify token coincida.

### 3. Conectar el modelo

1. Crear cuenta en OpenRouter.
2. Elegir modelo (ej. Claude Haiku o un modelo barato para chat).
3. Configurar la API key como variable de entorno.
4. Probar una llamada simple desde el código.

**Verificación:** el modelo responde a un prompt de prueba.

**Alternativa local:** si el volumen es bajo, usar Ollama con un modelo 7B. Pero la latencia de WhatsApp exige respuesta en <5s; un 7B en 6 GB puede no darla.

### 4. Memoria del chat

1. Crear tabla `conversations` (id, phone, timestamp, role, content).
2. Al recibir un mensaje: guardar el mensaje del usuario.
3. Recuperar los últimos N mensajes (ej. 20).
4. Enviarlos al modelo junto con el nuevo mensaje.
5. Guardar la respuesta del modelo.

**Verificación:** el agente recuerda el nombre del cliente en el segundo mensaje.

### 5. Conocimiento del negocio

1. Crear un bloque de texto (o archivo) con: servicios, precios, horarios, FAQ, reglas de reserva.
2. Inyectarlo en el system prompt.
3. Probar preguntas sobre el negocio: "¿cuánto cuesta X?", "¿abren los domingos?".

**Verificación:** el agente responde según el negocio, no inventa.

### 6. Herramientas (calendario)

1. Conectar la API del calendario (Google Calendar o similar).
2. Dar al agente tres herramientas: consultar disponibilidad, crear evento, cancelar evento.
3. Definir el flujo: el agente pregunta fecha/hora, consulta, confirma, crea.
4. Probar una reserva completa de punta a punta.

**Verificación:** una reserva real aparece en el calendario.

### 7. Prueba exhaustiva

1. Preguntas raras: "¿venden pizzas?", "¿cuánto cuesta un vuelo a Marte?".
2. Intentar romper: mensajes vacíos, emojis, audios, imágenes.
3. Intentar reservar con datos incompletos.
4. Verificar que el agente no se invente disponibilidad.

**Verificación:** lista de casos de prueba con resultado (pass/fail).

### 8. Despliegue

1. Subir a un VPS (ej. Hetzner, DigitalOcean, ~$5/mes).
2. Configurar HTTPS (Let's Encrypt).
3. Configurar variables de entorno (tokens, API keys).
4. Configurar logs y monitoreo.
5. Actualizar el webhook de Meta con la URL pública.

**Verificación:** el agente responde con el portátil apagado.

## Criterios de aceptación

- [ ] Un mensaje de WhatsApp recibe respuesta en <5s
- [ ] El agente recuerda el nombre del cliente en el segundo mensaje
- [ ] Responde correctamente a 5 preguntas sobre el negocio
- [ ] Una reserva real aparece en el calendario
- [ ] El agente sigue en pie con el portátil apagado
- [ ] Los datos de clientes se guardan con política de retención

## Cómo saber si falló

- El webhook no recibe mensajes (problema de HTTPS o verify token).
- El modelo tarda >10s en responder (modelo muy grande o VPS lento).
- El agente se inventa disponibilidad (herramienta mal definida).
- Los mensajes de clientes se pierden (sin logs ni reintentos).
- El costo de OpenRouter supera el presupuesto.

## Rollback

1. Desactivar el webhook en Meta Developers.
2. Apagar el VPS.
3. Volver a probar localmente.
4. Borrar los datos de prueba de la base de datos.

## Costos estimados

| Concepto | Costo mensual |
|---|---|
| VPS (Hetzner CX11) | ~$4 |
| OpenRouter (1000 mensajes/mes, modelo barato) | ~$2-5 |
| Meta WhatsApp API | gratis hasta 1000 conversaciones/mes |
| Total | ~$6-9/mes |

## Después de este plan

- Skill candidato: `agent-with-memory-and-tools` (ya creado).
- Skill candidato: `whatsapp-webhook-setup` (setup de Meta Developers).
- Evaluar si el canal WhatsApp justifica un agente dedicado o si conviene un canal genérico.
