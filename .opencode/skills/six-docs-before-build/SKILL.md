---
name: six-docs-before-build
description: >
  Produce the six planning documents (PRD, TRD, app flow, design brief, backend
  schema, implementation plan) before writing code with an AI agent. Use when
  starting a new app or agent project, before the first commit, or when an
  agent is guessing instead of building. Triggers: "armar una app", "planear un
  proyecto", "PRD", "TRD", "antes de programar", "documentos previos", "specs",
  "six docs", "plan de implementacion".
---

# Six docs before build

## Qué hace

Obliga a tener los seis documentos de especificación **antes** de escribir código con un agente. El agente deja de adivinar y empieza a construir sobre un plano.

Origen: video `videos/UADO82Ac7bo-no-programes-con-ia-sin-estos-6-documentos-prd-trd-y-plan-de/` [00:00] y [01:03].

## Cuándo usarlo

- Vas a arrancar un proyecto nuevo (app, agente, automatización).
- Un agente empezó a improvisar y el resultado no converge.
- Vas a pasar un proyecto a otra persona o a otro agente.
- Antes del primer commit de una feature grande.

## Cuándo NO usarlo

- Fix de un bug o tarea de un solo archivo.
- Refactor acotado con criterio de aceptación claro.
- Prototipo de menos de un día que se va a tirar.

En esos casos, una línea en el plan alcanza.

## Procedimiento

Trabajar en este orden. Cada documento bloquea al siguiente: no se avanza si el anterior no está cerrado.

1. **PRD** — qué y por qué.
   - Funcionalidades principales (lista).
   - Qué NO hace (fuera de alcance).
   - Idea general en 3-5 frases.
   - Criterio de éxito del proyecto.

2. **TRD** — cómo, a nivel técnico.
   - Stack (lenguajes, frameworks, runtime).
   - Herramientas y APIs externas.
   - Decisiones técnicas con su motivo.
   - Lo que se descartó y por qué.

3. **Flujo de la app** — pantallas y navegación.
   - Lista de pantallas / vistas.
   - Qué pasa cuando el usuario pulsa cada botón.
   - Recorrido principal (happy path) paso a paso.
   - Estados de error y vacíos.

4. **Brief de diseño** — cómo se ve y se siente.
   - Paleta de color y tipografía.
   - Componentes base.
   - Estilo general.
   - Referencia visual (link o captura).

5. **Esquema del backend** — cómo se guardan los datos.
   - Tablas / colecciones con columnas y tipos.
   - Relaciones.
   - Flujo de autenticación y autorización.
   - Qué datos son sensibles y cómo se protegen.

6. **Plan de implementación** — en qué orden se construye.
   - Pasos numerados, cada uno con archivos y verificación.
   - Criterios de aceptación.
   - Qué hacer si falla (rollback).
   - Estimación de tiempo.

## Salida esperada

Un archivo `spec.md` (o equivalente) con los seis bloques completos. En este repo, usar `templates/spec.md`.

## Errores comunes

| Error | Síntoma | Fix |
|---|---|---|
| PRD que es una lista de features sin prioridad | El agente hace todo a la vez | Marcar "fuera de alcance" y "primero" |
| TRD que dice "usar lo mejor" | El agente cambia de stack a mitad | Fijar versiones y justificar |
| Flujo sin pantallas de error | El agente solo construye el happy path | Agregar "qué pasa si falla" por pantalla |
| Brief de diseño vacío | La UI se ve genérica | Al menos paleta + tipografía + un referente |
| Esquema backend sin relaciones | El agente improvisa las tablas | Dibujar el modelo antes de codear |
| Plan sin verificación | No se sabe cuándo terminó | Cada paso con criterio de éxito |

## Origen

- Video: `videos/UADO82Ac7bo-no-programes-con-ia-sin-estos-6-documentos-prd-trd-y-plan-de/` [00:00], [01:03]
- Regla del repo: `AGENTS.md` → "Documentos previos"
