# Ficha de video — Agente de IA para WhatsApp en 30 minutos

## Metadatos

- **Título:** Construye Un Agente De IA Para WhatsApp En 30 Minutos Con Claude Code
- **Canal:** revolutia
- **URL:** https://youtube.com/shorts/vlKWMfbY9BA
- **Duración:** 1:43
- **Fecha:** 2026-10-14
- **Relevancia para el lab (1-5):** 5 (caso de uso completo de agente con memoria y herramientas)

## Tesis en una frase

> Un agente útil no es el que habla, es el que actúa: memoria del historial + conocimiento del negocio + herramientas (calendario) + despliegue, construido en 30 minutos con Claude Code.

## Qué enseña

- [00:00] Construir un agente de IA para WhatsApp en ~30 minutos, que hable con clientes, recuerde conversaciones, responda sobre el negocio y ejecute acciones.
- [00:05] Empezar por el **plan**: a qué se dedica el negocio, quiénes son los clientes, qué debe resolver el agente y qué acciones debe poder ejecutar. Dejar que defina la arquitectura antes de tocar código.
- [00:16] Conectar **WhatsApp**: crear la app en Meta Developers, añadir WhatsApp, configurar credenciales y el **webhook** (cómo Meta avisa a la app de un mensaje nuevo).
- [00:24] Conectar el modelo de IA a través de **OpenRouter** (varios modelos desde una sola API).
- [00:31] **Memoria del chat**: guardar el historial reciente y devolverlo al modelo con cada mensaje. Sin memoria, cada mensaje es una conversación nueva.
- [00:43] **Conocimiento del negocio**: servicios, precios, horarios, FAQ y reglas de reserva. Así el asistente no se inventa cosas.
- [00:53] **Herramientas**: conectar el calendario para consultar disponibilidad, mostrar huecos, tomar datos del cliente y cerrar la cita. Es lo que diferencia un agente de un chatbot.
- [01:01] Probar a conciencia: preguntar cosas raras, intentar reservar, intentar romperlo. Si falla, corregir prompt o código y volver a probar.
- [01:32] **Desplegar en un VPS**, porque el portátil no es un servidor: el agente debe seguir en pie aunque apagues el ordenador.

## Procedimiento que propone

1. Abrir un proyecto nuevo en Claude Code y empezar por el plan (negocio, clientes, problema, acciones).
2. Dejar que el agente defina la arquitectura antes de escribir código.
3. Crear la app en Meta Developers, añadir WhatsApp, configurar credenciales y webhook.
4. Conectar el modelo vía OpenRouter.
5. Implementar memoria: guardar historial reciente y enviarlo con cada mensaje.
6. Cargar el conocimiento del negocio (servicios, precios, horarios, FAQ, reglas).
7. Conectar herramientas (calendario: disponibilidad, huecos, datos del cliente, cierre de cita).
8. Probar exhaustivamente, incluyendo casos límite.
9. Desplegar en un VPS.

## Herramientas / stack mencionado

| Herramienta | Para qué | Alternativa que ya uso |
|---|---|---|
| Claude Code | Planificar y programar | OpenCode |
| Meta Developers + WhatsApp API | Canal de mensajería | — |
| Webhook | Recibir mensajes en tiempo real | polling (peor) |
| OpenRouter | Acceso unificado a varios modelos | proveedor directo |
| Base de datos (historial) | Memoria del chat | archivo local |
| Calendario (API) | Herramienta del agente | manual |

## Ideas aprovechables para mí

- La distinción **chatbot vs agente** es la mejor definición práctica que he visto: un chatbot habla, un agente actúa. Puede ir en el README o en `docs/metodologia.md`.
- La memoria como "guardar el historial reciente y devolverlo con cada mensaje" es exactamente el patrón que ya usamos en el lab (archivos, no bases vectoriales para proyectos chicos).
- El flujo **plan → canal → modelo → memoria → conocimiento → herramientas → prueba → despliegue** es un plan de implementación completo. Se puede convertir en `plans/agente-whatsapp.md`.
- El conocimiento del negocio como "servicios, precios, horarios, FAQ, reglas" es un bloque de especificación que se puede estandarizar (parte del PRD/TRD del video anterior).

## Humo / a verificar

- [ ] "30 minutos" — es marketing. Con Meta Developers, webhook, VPS y debugging real, la primera versión funcional lleva más.
- [ ] OpenRouter es de pago por uso. El video no menciona costos ni límites de rate.
- [ ] La app de Meta Developers requiere verificación de negocio para producción (webhook en producción). Para pruebas alcanza, pero no para clientes reales.
- [ ] Desplegar en un VPS tiene costo mensual y requiere gestión de secretos, HTTPS, logs.
- [ ] Guardar el historial de conversaciones de clientes implica responsabilidad sobre datos personales (privacidad, retención, acceso).
- [ ] El video no menciona manejo de errores, reintentos, ni qué pasa si el modelo falla a mitad de una reserva.
- [ ] "La guía completa está en nuestra bóveda" — el video no enseña el código, solo el flujo. Es captación de tráfico, como los anteriores.

## Artefactos que salen de acá

| Tipo | Nombre | Por qué |
|---|---|---|
| skill | `agent-with-memory-and-tools` | El patrón (memoria + conocimiento + herramientas) es reutilizable en cualquier canal |
| plan | `agente-whatsapp-claude-code` | Implementación concreta paso a paso para este lab |
| docs | `docs/decisiones.md` | Decidir si usar OpenRouter o proveedor directo |

## Citas textuales

> "Un chatbot habla. Un agente actúa." [01:01]

> "Sin memoria, cada mensaje es una conversación nueva." [00:31]
