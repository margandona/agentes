# Spec: adaptar el video sobre CV a una skill local

## 1. PRD — requisitos de producto
Adaptar la skill existente para mejorar un CV respecto de una oferta, sin inventar antecedentes ni presentar simulaciones como resultados reales. La solicitud actual aprueba completar el artefacto propuesto. Fuente: transcripción completa y revisión visual de 32 fotogramas del video s_xr--Zp5Fg.

## 2. TRD — requisitos técnicos
Skill de instrucciones Markdown, sin API ni scripts de procesamiento. Fuente en skills/; copias descubribles en .agents/skills y .opencode/skills. Validar YAML, estructura y coincidencia de copias. No se requiere programación adicional.

## 3. Flujo de la app
Invocación natural → recibir CV y oferta → diagnóstico de claridad → reescritura de experiencia → correspondencia de requisitos → propuesta de valor y CV final. Si falta la oferta, ofrecer revisión general y pedirla para evaluar compatibilidad.

## 4. Brief de diseño
Salida en español, con tabla de requisitos y evidencias, ejemplos antes/después y CV final fácil de copiar. No requiere interfaz propia; usa el chat de Codex/OpenCode.

## 5. Esquema del backend
Sin backend ni almacenamiento obligatorio. Usar documentos aportados en la conversación; conservar el original si se pide escribir archivos. No enviar postulaciones ni publicar datos personales como parte de esta skill.

## 6. Plan de implementación
Corregir las instrucciones existentes, registrar fuente audiovisual y limitaciones, instalar ambas copias y validar estructura y enlaces. Los seis documentos se reúnen aquí según templates/spec.md. Conservar la extracción anterior en la ficha, aclarando qué afirmaciones pertenecen al video. No verificar externamente atribuciones promocionales innecesarias para ejecutar la skill.

Aceptación: nombres correctos, ausencia de promesas ATS o métricas inventadas, referencias válidas, copias idénticas y validación de formato aprobada. Una validación estructural no demuestra eficacia en contratación. Rollback: restaurar únicamente esta skill mediante el control de versiones; no tocar otras herramientas.
