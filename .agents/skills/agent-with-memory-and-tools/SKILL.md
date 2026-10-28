---
name: agent-with-memory-and-tools
description: >
  Build an agent that remembers conversations and takes actions, not just a
  chatbot. Use when designing or reviewing an agent for WhatsApp, Telegram,
  email, or any channel where the bot must recall context and execute tools.
  Triggers: "agente", "chatbot vs agente", "memoria del chat", "herramientas
  del agente", "ejecutar acciones", "recordar conversaciones".
---

# Agent with memory and tools

## Qué hace

Convierte un chatbot en un agente: añade memoria del historial, conocimiento del negocio y herramientas ejecutables. Sin memoria, cada mensaje es una conversación nueva. Sin herramientas, solo conversa. Con las dos, tenés algo que trabaja por vos.

Origen: video `videos/vlKWMfbY9BA-construye-un-agente-de-ia-para-whatsapp-en-30-minutos-con-cl/` [00:31] y [01:01].

## Cuándo usarlo

- Vas a construir un agente para un canal (WhatsApp, Telegram, email, web).
- Un bot existente "no recuerda" o "no hace nada".
- Estás diseñando la arquitectura de un agente nuevo.
- Revisás por qué un agente no converge.

## Cuándo NO usarlo

- Un chatbot de una sola respuesta (FAQ estático).
- Un asistente sin estado (cada pregunta es independiente).
- Prototipo de un día que se va a tirar.

## Procedimiento

Seguir este orden. Cada bloque desbloquea al siguiente.

1. **Plan** (antes de tocar código)
   - A qué se dedica el negocio.
   - Quiénes son los clientes.
   - Qué debe resolver el agente.
   - Qué acciones debe poder ejecutar.
   - Dejar que el agente defina la arquitectura.

2. **Canal** (cómo entra el mensaje)
   - Crear la app en el proveedor (Meta Developers para WhatsApp).
   - Configurar credenciales y webhook.
   - El webhook es cómo el proveedor avisa a tu app de un mensaje nuevo.

3. **Modelo** (cómo piensa)
   - Conectar el modelo vía proveedor directo o agregador (OpenRouter).
   - Elegir modelo según costo, latencia y calidad.

4. **Memoria** (lo que casi todos se salvan)
   - Guardar el historial reciente por conversación.
   - Devolverlo al modelo con cada mensaje.
   - Sin esto, cada mensaje es un desconocido.

5. **Conocimiento del negocio** (para que no se invente)
   - Servicios, precios, horarios.
   - FAQ.
   - Reglas de reserva / operación.
   - Formato: un bloque de texto o un archivo que se inyecta en el prompt.

6. **Herramientas** (lo que lo vuelve agente)
   - Conectar APIs externas (calendario, base de datos, CRM).
   - Definir qué puede consultar, crear, modificar.
   - El agente decide cuándo usarlas.

7. **Prueba** (intentar romperlo)
   - Preguntas raras, casos límite, intentar reservar, intentar romperlo.
   - Si falla, corregir prompt o código y volver a probar.

8. **Despliegue** (para que siga en pie)
   - Subir a un VPS o servicio de hosting.
   - El portátil no es un servidor.
   - Configurar secretos, HTTPS, logs, monitoreo.

## Salida esperada

Un agente que:
- Recibe mensajes por un canal.
- Recuerda la conversación.
- Responde según el negocio.
- Ejecuta acciones (reservas, consultas, etc.).
- Sigue en pie aunque apagues tu máquina.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| Sin memoria | El agente repite preguntas ya respondidas | Guardar y enviar historial reciente |
| Sin conocimiento | El agente se inventa precios o servicios | Inyectar bloque de negocio en el prompt |
| Sin herramientas | El agente solo conversa, no actúa | Conectar al menos una API (calendario, DB) |
| Probar solo el happy path | Falla en producción con clientes reales | Intentar romperlo antes de desplegar |
| Desplegar en el portátil | El agente cae cuando apagás la máquina | Subir a un VPS |
| Guardar datos de clientes sin política | Riesgo de privacidad y legal | Definir retención y acceso antes de guardar |

## Origen

- Video: `videos/vlKWMfbY9BA-construye-un-agente-de-ia-para-whatsapp-en-30-minutos-con-cl/` [00:05], [00:31], [00:43], [00:53], [01:01], [01:32]
- Definición: "Un chatbot habla. Un agente actúa." (video [01:01])
- Metodología del lab: `docs/metodologia.md` → "Chatbot vs agente"
